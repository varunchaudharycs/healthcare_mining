
import scrapy
import os
import json
import re
import urllib.parse as url_parser

from webmd_drug_crawler.items import DrugReviewItem

CURRENT_DIR = os.path.dirname(__file__)
WEBMD_HOME_PAGE_URL = 'https://www.webmd.com'


# Totally crawled reviews - 3,63,916
#  Run using the following command:
#  scrapy crawl webmd_drug_review_crawler -t json -o webmd_drugs_reviews.json
class WebMDDrugReviewSpider(scrapy.Spider):
    name = 'webmd_drug_review_crawler'
    allowed_domains = ['webmd.com']

    # load all review pages from json file
    start_urls = []
    drug_review_url_to_drug_details_map = {}
    with open(CURRENT_DIR + '/../../webmd_drug_review_urls.json') as f:
        drugs = json.load(f)
        for drug in drugs:
            start_urls.append(drug['review_page_url'])
            drug_details = []
            drug_details.append(drug['name'])
            drug_details.append(drug['detail_page_redirected_url'])
            review_page_url = drug['review_page_url']
            drug_details.append(review_page_url)
            if '?drugid=' in review_page_url:
                review_page_url = review_page_url[0: review_page_url.find('?drugid=')]
            drug_review_url_to_drug_details_map[review_page_url] = drug_details

    def parse(self, response):
        print("Processing: " + response.url)

        count = 1
        for review in response.css('#ratings_fmt > div.userPost'):
            review_page_url = response.url
            if '?drugid=' in review_page_url:
                review_page_url = review_page_url[0: review_page_url.find('?drugid=')]
            drug_details = self.drug_review_url_to_drug_details_map[review_page_url]

            drug_review_item = DrugReviewItem()
            drug_review_item['drug_name'] = drug_details[0]
            drug_review_item['drug_detail_page'] = drug_details[1]
            drug_review_item['drug_review_page'] = drug_details[2]
            condition_name = review.css('div.postHeading.clearfix > div.conditionInfo::text').extract_first().strip()
            condition_name = re.sub(r'\s+', ' ', condition_name)
            condition_name = condition_name[len('Condition: '):]
            drug_review_item['health_condition_name'] = condition_name
            review_ts = review.css('div.postHeading.clearfix > div.date::text').extract_first().strip()
            drug_review_item['timestamp'] = review_ts
            reviewer_details = review.css('p.reviewerInfo::text').extract_first().strip()
            reviewer_details = re.sub(r'\s+', ' ', reviewer_details)
            # saving full reviewer details line as during crawling if some error happens it will create issue
            drug_review_item['reviewer_full_det'] = reviewer_details

            if reviewer_details.find('Reviewer: ') != -1:
                reviewer_details = reviewer_details[len('Reviewer: '):]

                # Reviewer:

                reviewer_name = 'unknown'
                if reviewer_details.find(', ') != -1:
                    reviewer_name = reviewer_details[0: reviewer_details.find(',')]
                    reviewer_details = reviewer_details[reviewer_details.find(', ') + 2:]
                    reviewer_details = reviewer_details.strip()
                drug_review_item['reviewer_name'] = reviewer_name

                # Reviewer: 55-64 Male on Treatment for 1 to 6 months (Patient)
                # Reviewer: soumen, 25-34 Male on Treatment for less than 1 month (Patient)

                age_range = 'unknown'
                # if the reviewer details also contains the age details
                if reviewer_details[0].isdigit() and '-' in reviewer_details:
                    start = reviewer_details[0: reviewer_details.find('-')].strip()
                    reviewer_details = reviewer_details[reviewer_details.find('-')+1:].strip()
                    end = reviewer_details[0: reviewer_details.find(' ')]
                    age_range = str(start) + '-' + str(end)
                drug_review_item['patient_age_range'] = age_range

                gender = 'unknown'
                if reviewer_details.find('Female') != -1:
                    gender = 'Female'
                elif reviewer_details.find('Male') != -1:
                    gender = 'Male'
                drug_review_item['patient_gender'] = gender

                duration = 'unknown'
                if reviewer_details.find('on Treatment for ') != -1:
                    start_idx = reviewer_details.find('on Treatment for ')
                    end_idx = reviewer_details.find(' (')
                    duration = reviewer_details[start_idx + len('on Treatment for '): end_idx]
                drug_review_item['treatment_duration'] = duration

                category = 'unknown'
                if reviewer_details.find('(Patient)') != -1:
                    category = 'Patient'
                if reviewer_details.find('(Caregiver)') != -1:
                    category = 'Caregiver'
                drug_review_item['reviewer_category'] = category
            else:
                drug_review_item['reviewer_name'] = 'unknown'
                drug_review_item['patient_age_range'] = 'unknown'
                drug_review_item['patient_gender'] = 'unknown'
                drug_review_item['treatment_duration'] = 'unknown'
                drug_review_item['reviewer_category'] = 'unknown'

            comment = review.xpath('// *[ @ id = "comFull' + str(count) + '"] / text()').extract_first()
            if comment:
                comment = re.sub(r'\s+', ' ', comment)
            else:
                comment = ''
            drug_review_item['review_comment'] = comment

            num_people_found_useful = 0
            found_helpful = review.css('div > p.helpful::text').extract_first().strip()
            found_helpful = re.sub(r'\s+', ' ', found_helpful)
            if found_helpful[0].isdigit():
                num_people_found_useful = int(found_helpful[0: found_helpful.find(' ')])
            drug_review_item['num_of_people_found_useful'] = num_people_found_useful

            effectiveness = review.css(
                '#ctnStars > div.catRatings.firstEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip()
            effectiveness = effectiveness[len('Current Rating: '):]
            drug_review_item['effectiveness_rating'] = effectiveness

            ease_of_use = review.css(
                '#ctnStars > div:nth-child(2) > p.inlineRating.starRating > span::text').extract_first().strip()
            ease_of_use = ease_of_use[len('Current Rating: '):]
            drug_review_item['ease_of_use_rating'] = ease_of_use

            satisfaction = review.css(
                '#ctnStars > div.catRatings.lastEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip()
            satisfaction = satisfaction[len('Current Rating: '):]
            drug_review_item['satisfaction_rating'] = satisfaction

            count += 1
            yield drug_review_item

            # print(review.css('div.postHeading.clearfix > div.conditionInfo::text').extract_first().strip())
            # print(review.css('div.postHeading.clearfix > div.date::text').extract_first().strip())
            # print(review.css('p.reviewerInfo::text').extract_first().strip())
            # # some review might not have comment - it will be None
            # print(review.xpath('// *[ @ id = "comFull' + str(count) + '"] / text()').extract_first())
            # found_helpful = review.css('div > p.helpful::text').extract_first().strip()
            # found_helpful = re.sub(r'\s+', ' ', found_helpful)
            # print(found_helpful)
            #
            # print(review.css(
            #     '#ctnStars > div.catRatings.firstEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip())
            # print(review.css(
            #     '#ctnStars > div:nth-child(2) > p.inlineRating.starRating > span::text').extract_first().strip())
            # print(review.css(
            #     '#ctnStars > div.catRatings.lastEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip())

        if response.xpath('//*[@id="ratings_fmt"]/div/div/a[contains(text(), "Next")]'):
            # creates issue as adds + in the URL and map lookup fails as review page base url is used to reverse lookup
            # next_page_url = response.xpath(
            #     '//*[@id="ratings_fmt"]/div/div/a[contains(text(), "Next")]/@href').extract_first()
            # next_page_url = WEBMD_HOME_PAGE_URL + next_page_url
            current_page_url = response.url
            print('Current Page: '+current_page_url)
            #             # page_idx = int(current_page_url[current_page_url.find('&pageIndex=') + len('&pageIndex='): current_page_url.find('&sortby=')])
            #             # next_page_url = current_page_url.replace('pageIndex=' + str(page_idx), 'pageIndex=' + str(++page_idx))

            url_parts = url_parser.urlsplit(current_page_url)
            params = url_parser.parse_qs(url_parts.query)
            last_page_idx = int(params['pageIndex'][0])
            last_page_idx = last_page_idx + 1
            params['pageIndex'] = [str(last_page_idx)]
            new_query = ''
            count = 0
            for param_key in params:
                if count != 0:
                    new_query = new_query + '&'
                new_query = new_query + param_key + '=' + params[param_key][0]
                count += 1

            next_page_url = url_parser.urlunsplit((url_parts[0], url_parts[1], url_parts[2], new_query, url_parts.fragment))
            print('Next Page: ' + next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)

# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=1&sortby=3&conditionFilter=1455
# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=1&sortby=3&conditionFilter=3079
# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=0&sortby=3&conditionFilter=3079
# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=2&sortby=3&conditionFilter=3079

# https://www.webmd.com/drugs/2/drug-57708/bc-oral/details - drug details page
# https://www.webmd.com/drugs/drugreview-57708-BC-oral.aspx?drugid=57708&drugname=BC-oral
# &pageIndex=0&sortby=3&conditionFilter=1455

# INFO: Crawled 15685 pages (at 42 pages/min), scraped 62283 items (at 172 items/min)

import scrapy
import re
import os

CURRENT_DIR = os.path.dirname(__file__)


#  Run using the following command:
#  scrapy crawl webmd_drug_review_crawler -t json -o patient_info_forums.json
class WebMDDrugReviewSpider(scrapy.Spider):
    name = 'webmd_drug_review_crawler'
    allowed_domains = ['webmd.com']

    # all these letters totally has 1363 unique forums/groups
    start_urls = [
        'https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx'
    ]

    def parse(self, response):
        print("Processing: " + response.url)
        # all_reviews = response.xpath('//*[@id="ratings_fmt"]/div').getall()
        # all_reviews = response.css('#ratings_fmt > div.userPost').getall()
        # //*[@id="comTrunc1"]/text()
        # //*[@id="ratings_fmt"]/div[4]
        # #ratings_fmt > div:nth-child(5)
        # print(len(all_reviews))
        # //*[@id="comTrunc1"]/text()

        count = 1
        for review in response.css('#ratings_fmt > div.userPost'):
            print('\n')
            print(review.css('div.postHeading.clearfix > div.conditionInfo::text').extract_first().strip())
            print(review.css('div.postHeading.clearfix > div.date::text').extract_first().strip())
            print(review.css('p.reviewerInfo::text').extract_first().strip())
            # some review might not have comment - it will be None
            print(review.xpath('// *[ @ id = "comFull' + str(count) +'"] / text()').extract_first())
            found_helpful = review.css('div > p.helpful::text').extract_first().strip()
            found_helpful = re.sub(r'\s+', ' ', found_helpful)
            print(found_helpful)

            print(review.css('#ctnStars > div.catRatings.firstEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip())
            print(review.css('#ctnStars > div:nth-child(2) > p.inlineRating.starRating > span::text').extract_first().strip())
            print(review.css('#ctnStars > div.catRatings.lastEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip())

            # #ctnStars > div.catRatings.firstEl.clearfix > p.inlineRating.starRating > span
            # #ctnStars > div:nth-child(2) > p.inlineRating.starRating > span
            # #ctnStars > div.catRatings.lastEl.clearfix > p.inlineRating.starRating > span

            # #ratings_fmt > div:nth-child(5) > div > p.helpful
            count += 1


# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=1&sortby=3&conditionFilter=1455
# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=1&sortby=3&conditionFilter=3079
# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=0&sortby=3&conditionFilter=3079
# https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=2&sortby=3&conditionFilter=3079
# https://www.webmd.com/drugs/2/alpha/a/
# https://www.webmd.com/drugs/2/alpha/a/aa
# https://www.webmd.com/drugs/2/alpha/a/ab

# https://www.webmd.com/drugs/2/alpha/b/ba
# https://www.webmd.com/drugs/2/alpha/b/bb - no drugs
# https://www.webmd.com/drugs/2/alpha/b/bc

# https://www.webmd.com/drugs/2/drug-57708/bc-oral/details - drug details page
# https://www.webmd.com/drugs/drugreview-57708-BC-oral.aspx?drugid=57708&drugname=BC-oral

# 2020-04-09 02:40:33 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
# {'downloader/request_bytes': 28351434,
#  'downloader/request_count': 37077,
#  'downloader/request_method_count/GET': 37077,
#  'downloader/response_bytes': 651522720,
#  'downloader/response_count': 37077,
#  'downloader/response_status_count/200': 18568,
#  'downloader/response_status_count/301': 18508,
#  'downloader/response_status_count/504': 1,
#  'elapsed_time_seconds': 22728.084061,
#  'finish_reason': 'finished',
#  'finish_time': datetime.datetime(2020, 4, 9, 9, 40, 33, 725903),
#  'item_scraped_count': 18433,
#  'log_count/DEBUG': 55510,
#  'log_count/INFO': 389,
#  'memusage/max': 122273792,
#  'memusage/startup': 67325952,
#  'response_received_count': 18568,
#  'retry/count': 1,
#  'retry/reason_count/504 Gateway Time-out': 1,
#  'scheduler/dequeued': 37077,
#  'scheduler/dequeued/memory': 37077,
#  'scheduler/enqueued': 37077,
#  'scheduler/enqueued/memory': 37077,
#  'start_time': datetime.datetime(2020, 4, 9, 3, 21, 45, 641842)}
# 2020-04-09 02:40:33 [scrapy.core.engine] INFO: Spider closed (finished)
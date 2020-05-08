import scrapy
import os
import json

from webmd_drug_crawler.items import DrugReviewPageLinkItem

CURRENT_DIR = os.path.dirname(__file__)
WEBMD_HOME_PAGE_URL = 'https://www.webmd.com'


#  scrapy crawl webmd_drug_review_page_crawler -t json -o webmd_drug_review_urls.json
class WebMDDrugReviewPageLinkSpider(scrapy.Spider):
    name = 'webmd_drug_review_page_crawler'
    allowed_domains = ['webmd.com']

    # read the json file for list of drug detail page and extract review page link.
    start_urls = []
    drug_url_to_drug_name_map = {}
    with open(CURRENT_DIR + '/../../webmd_drug_detail_urls.json') as f:
        drugs = json.load(f)
        for drug in drugs:
            start_urls.append(drug['detail_page_url'])
            drug_url_to_drug_name_map[drug['detail_page_url']] = drug['name']

    def parse(self, response):
        # redirection?
        print("Processing: " + response.request.url)
        redirected_url = response.request.url
        # redirected_url = response.url
        if response.request.meta.get('redirect_urls'):
            requested_url = response.request.meta['redirect_urls'][0]
        else:
            requested_url = response.request.url

        # print('Requested: ' + requested_url)
        # print('Redirected: ' + redirected_url)

        # two types of drug details page:
        # https://www.webmd.com/drugs/2/drug-408/caffeine-oral/details - most of the pages
        # https://www.webmd.com/drugs/2/drug-64439/abilify-oral/details  - only a few pages
        # #ContentPane29 > div.drug-monograph-container > div.drug-information > div.drug-names > div > a.drug-review
        review_page_url = response.css('#ContentPane29 > div.drug-monograph-container > div.drug-information > div.drug-names > div > a.drug-review::attr(href)').extract_first()
        if review_page_url is not None and review_page_url != '':
            # review_page_url = review_page_element.xpath('@href').extract_first()
            review_page_url = WEBMD_HOME_PAGE_URL + review_page_url
            drug_review_link_item = DrugReviewPageLinkItem()
            drug_review_link_item['name'] = self.drug_url_to_drug_name_map[requested_url]
            drug_review_link_item['detail_page_url'] = requested_url
            drug_review_link_item['detail_page_redirected_url'] = redirected_url
            drug_review_link_item['review_page_url'] = review_page_url + '&pageIndex=0&sortby=3&conditionFilter=-1'

            return drug_review_link_item
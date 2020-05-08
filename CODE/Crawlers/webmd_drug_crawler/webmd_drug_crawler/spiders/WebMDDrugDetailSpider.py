
import scrapy
import os
from string import ascii_lowercase

from webmd_drug_crawler.items import DrugDetailPageLinkItem

CURRENT_DIR = os.path.dirname(__file__)
DRUG_INDEX_PREFIX = 'https://www.webmd.com/drugs/2/alpha/'
WEBMD_HOME_PAGE_URL = 'https://www.webmd.com'


#  scrapy crawl webmd_drug_detail_page_crawler -t json -o webmd_drug_detail_urls.json
class WebMDDrugDetailSpider(scrapy.Spider):
    name = 'webmd_drug_detail_page_crawler'
    allowed_domains = ['webmd.com']

    # URL patterns
    # https://www.webmd.com/drugs/2/alpha/0
    # https://www.webmd.com/drugs/2/alpha/a/
    # https://www.webmd.com/drugs/2/alpha/a/aa
    # https://www.webmd.com/drugs/2/alpha/a/ab
    # https://www.webmd.com/drugs/2/alpha/b/ba
    # https://www.webmd.com/drugs/2/alpha/b/bb

    start_urls = []
    # append the only numeric drug index 0
    start_urls.append(DRUG_INDEX_PREFIX + '0')
    for c in ascii_lowercase:
        url_suffix = c
        for c2 in ascii_lowercase:
            start_urls.append(DRUG_INDEX_PREFIX + url_suffix + '/' + url_suffix + c2)

    print(start_urls)

    def parse(self, response):
        print("Processing: " + response.url)

        # ContentPane30 > div.drug-list-container > ul > li
        drug_items = []
        # if the page has this container listing drugs then only iterate and collect drug detail page url
        for drug in response.css('#ContentPane30 > div.drug-list-container > ul > li'):
            drug_link_item = DrugDetailPageLinkItem()
            drug_link_item['name'] = drug.xpath('a/text()').extract_first().strip()
            drug_link_item['detail_page_url'] = WEBMD_HOME_PAGE_URL + drug.xpath('a/@href').extract_first().strip()
            drug_items.append(drug_link_item)

        return drug_items
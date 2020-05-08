import scrapy

from patient_info_crawler.items import PIForumLinkItem

URL_PREFIX = "https://patient.info"


#  Run using the following command:
#  scrapy crawl pi_forums_crawler -t json -o patient_info_forums.json
class PatientInfoForumsSpider(scrapy.Spider):
    name = 'pi_forums_crawler'
    allowed_domains = ['patient.info']

    # all these letters totally has 1363 unique forums/groups
    start_urls = [
        'https://patient.info/forums/index-a',
        'https://patient.info/forums/index-b',
        'https://patient.info/forums/index-c',
        'https://patient.info/forums/index-d',
        'https://patient.info/forums/index-e',
        'https://patient.info/forums/index-f',
        'https://patient.info/forums/index-g',
        'https://patient.info/forums/index-h',
        'https://patient.info/forums/index-i',
        'https://patient.info/forums/index-j',
        'https://patient.info/forums/index-k',
        'https://patient.info/forums/index-l',
        'https://patient.info/forums/index-m',
        'https://patient.info/forums/index-n',
        'https://patient.info/forums/index-o',
        'https://patient.info/forums/index-p',
        'https://patient.info/forums/index-q',
        'https://patient.info/forums/index-r',
        'https://patient.info/forums/index-s',
        'https://patient.info/forums/index-t',
        'https://patient.info/forums/index-u',
        'https://patient.info/forums/index-v',
        'https://patient.info/forums/index-w',
        'https://patient.info/forums/index-x',
        'https://patient.info/forums/index-y',
        'https://patient.info/forums/index-z'
    ]

    def parse(self, response):
        # print("Processing: " + response.url)
        # all_groups = response.xpath('//*[@id="main-section"]/div/div/div/table/tbody/tr/td/a').getall()
        forum_items = []
        for group in response.xpath('//*[@id="main-section"]/div/div/div/table/tbody/tr/td/a'):
            forum_item = PIForumLinkItem()
            forum_item['forum_name'] = group.xpath('text()').extract_first()
            forum_item['forum_url'] = URL_PREFIX + group.xpath('@href').extract_first()
            forum_items.append(forum_item)

        return forum_items

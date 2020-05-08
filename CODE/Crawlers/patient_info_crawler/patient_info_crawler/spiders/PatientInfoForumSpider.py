import scrapy
import json
import os

from patient_info_crawler.items import PIForumPostLinkItem

URL_PREFIX = "https://patient.info"
CURRENT_DIR = os.path.dirname(__file__)

# intentionally crawling different community in the same json file to avoid having more than 1000 json files
# scrapy crawl pi_forum_posts_crawler  -t json -o patient_info_forum_posts.json
# Uses group links json file crawled by PatientInfoForumsSpider
# PatientInfoForumPostsLinkSpider
class PatientInfoForumSpider(scrapy.Spider):
    name = 'pi_forum_posts_crawler'
    allowed_domains = ['patient.info']
    # debug with single forum
    # start_urls = [
    #     'https://patient.info/forums/discuss/browse/abdominal-disorders-3321',
    # ]
    # group_url_to_group_name_map = {
    #     'https://patient.info/forums/discuss/browse/abdominal-disorders-3321' : 'Abdominal Disorders'
    # }

    crawled_urls = set()
    start_urls = []
    group_url_to_group_name_map = {}
    with open(CURRENT_DIR + '/../../patient_info_forums.json') as f:
        forums = json.load(f)
        for forum in forums:
            start_urls.append(forum['forum_url'])
            group_url_to_group_name_map[forum['forum_url']] = forum['forum_name']

    def parse(self, response):
        print("Processing: " + response.url)
        # this link has already been crawled - prevent duplicate forum posts
        if response.url in self.crawled_urls:
            return

        self.crawled_urls.add(response.url)

        for post in response.xpath('//*[@id="group-discussions"]/ul/li'):
            # to ensure we don't crawl advertisement post embedded in the list
            if post.xpath('div/div/article/h3/a/text()'):
                base_url = response.url
                if '?page=' in response.url:
                    base_url = base_url[0: base_url.find('?page=')]

                post_item = PIForumPostLinkItem()
                post_item['group_name'] = self.group_url_to_group_name_map[base_url]
                post_item['post_title'] = post.xpath('div/div/article/h3/a/text()').extract_first()
                post_item['post_url'] = URL_PREFIX + post.xpath('div/div/article/h3/a/@href').extract_first()
                yield post_item

        # if response.xpath('//*[@id="group-discussions"]/div[2]/form/a/@href'):
        if response.css('#group-discussions > div.group-discussions__paginate_bottom > form > a'):
            next_page_url = ''
            # first page next is different than the first page next
            if "page=" not in response.url:
                # next_page_url = response.css('#group-discussions > div.group-discussions__paginate_bottom > form > a::attr(href)').extract_first()
                next_page_url = response.css(
                    '#group-discussions > div.group-discussions__paginate_bottom > form > a.reply__control.reply-ctrl-last.link::attr(href)').extract_first()
            else:
                if response.css('#group-discussions > div.group-discussions__paginate_bottom > form > a.reply__control.reply-ctrl-last.link::attr(href)'):
                    next_page_url = response.css(
                    '#group-discussions > div.group-discussions__paginate_bottom > form > a.reply__control.reply-ctrl-last.link::attr(href)').extract_first()

            if next_page_url != '' and next_page_url not in self.crawled_urls:
                print('Next Page: ' + next_page_url)
                # next_page_url = response.xpath('//*[@id="group-discussions"]/div[2]/form/a/@href').extract_first()
                # next_page_url = response.css('#group-discussions > div.group-discussions__paginate_bottom > form > a::attr(href)').extract_first()
                # #group-discussions > div.group-discussions__paginate_bottom > form > a:nth-child(2)
                # #group-discussions > div.group-discussions__paginate_bottom > form > a.reply__control.reply-ctrl-last.link
                # #group-discussions > div.group-discussions__paginate_bottom > form > a
                yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)

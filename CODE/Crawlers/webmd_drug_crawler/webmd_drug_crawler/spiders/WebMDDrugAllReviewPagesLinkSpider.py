#
# import scrapy
# import os
# import json
#
# from webmd_drug_crawler.items import DrugReviewPageLinkItem
#
# CURRENT_DIR = os.path.dirname(__file__)
# WEBMD_HOME_PAGE_URL = 'https://www.webmd.com'
#
#
# Uncommenting creates conflict
# # TODO: This crawler is not needed as we can just add this suffix which handles all conditions:
# # &pageIndex=0&sortby=3&conditionFilter=-1
# #  scrapy crawl webmd_drug_all_review_pages_crawler -t json -o webmd_drug_all_review_urls.json
# class WebMDDrugAllReviewPagesLinkSpider(scrapy.Spider):
#     name = 'notneeded_webmd_drug_all_review_pages_crawler'
#     allowed_domains = ['webmd.com']
#
#     # read the json file for review page and extract all possible reviews pages based on the drop down values
#     start_urls = []
#     drug_review_url_to_drug_details_map = {}
#     drug_review_url_to_detail_page_url_map = {}
#     drug_review_url_to_detail_red_page_url_map = {}
#     with open(CURRENT_DIR + '/../../webmd_drug_review_urls.json') as f:
#         drugs = json.load(f)
#         for drug in drugs:
#             start_urls.append(drug['review_page_url'])
#             drug_details = []
#             drug_details.append(drug['name'])
#             drug_details.append(drug['detail_page_url'])
#             drug_details.append(drug['detail_page_redirected_url'])
#             drug_review_url_to_drug_details_map[drug['review_page_url']] = drug_details
#
#     def parse(self, response):
#         # redirection?
#         print("Processing: " + response.url)
#
#         all_review_urls = []
#         # #conditionFilter > option
#         for option in response.css('#conditionFilter > option'):
#             # condition_name_element = option.css('::text').extract_first().strip()
#             # condition_name = re.sub(r'\s+', ' ', condition_name_element)
#             # print(condition_name)
#             print(option.css('::attr(value)').extract_first())
#             condition_filter_value = option.css('::attr(value)').extract_first()
#             # additionally has these parameters - &pageIndex=0&sortby=3&conditionFilter=1455
#             all_review_urls.append(response.url + '&pageIndex=0&sortby=3&conditionFilter=' + condition_filter_value)
#
#         # create drug review page item considering all the conditions drop down
#         drug_review_link_item = DrugReviewPageLinkItem()
#         drug_details = self.drug_review_url_to_drug_name_map[response.url]
#         drug_review_link_item['name'] = drug_details[0]
#         drug_review_link_item['detail_page_url'] = drug_details[1]
#         drug_review_link_item['detail_page_redirected_url'] = drug_details[2]
#         drug_review_link_item['review_page_url'] = response.url
#         drug_review_link_item['all_review_page_urls'] = all_review_urls
#
#         return drug_review_link_item
#
# # some sample url patterns
# # https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=1&sortby=3&conditionFilter=1455
# # https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=1&sortby=3&conditionFilter=3079
# # https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=0&sortby=3&conditionFilter=3079
# # https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx?drugid=1082&drugname=aspirin+oral&pageIndex=2&sortby=3&conditionFilter=3079
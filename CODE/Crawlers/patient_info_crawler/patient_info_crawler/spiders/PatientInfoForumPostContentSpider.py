import scrapy
import json
import os
import re

from patient_info_crawler.items import PIForumPostContentItem, PIForumPostCommentItem

URL_PREFIX = "https://patient.info"
CURRENT_DIR = os.path.dirname(__file__)

# About 235901 unique forum posts crawled
# scrapy crawl pi_forum_posts_content_crawler  -t json -o patient_info_forum_posts_content.json
# Uses posts links json file crawled by PatientInfoForumPostsLinkSpider
class PatientInfoForumPostContentSpider(scrapy.Spider):
    name = 'pi_forum_posts_content_crawler'
    allowed_domains = ['patient.info']

    # debugging with single forum post url
    # start_urls = ['https://patient.info/forums/discuss/abdominal-pain-right-side-under-ribs-and-back-pain-497946']
    # group_url_to_group_name_map = {'https://patient.info/forums/discuss/abdominal-pain-right-side-under-ribs-and-back-pain-497946' : 'Abdominal Disorders'}

    start_urls = []
    group_url_to_group_name_map = {}
    with open(CURRENT_DIR + '/../../patient_info_forum_posts.json') as f:
        forums = json.load(f)
        for forum in forums:
            start_urls.append(forum['post_url'])
            group_url_to_group_name_map[forum['post_url']] = forum['group_name']

    # TODO: don't forget trim some fields - .strip()
    def parse(self, response):
        print("Processing: " + response.url)
        # post meta data and content
        post_title = response.xpath('// *[ @ id = "topic"] / article / div / h1 / text()').extract_first()
        post_title = re.sub(r'\s+', ' ', post_title)
        # print(post_title)
        post_time = response.css('#topic > article > p > span:nth-child(1) > time::attr(datetime)').extract_first()
        # print(post_time)
        num_of_people_following_str = response.css('#topic > article > p > span:nth-child(2)::text').extract_first()
        follow_count_str = '0'
        if num_of_people_following_str:
            num_of_people_following_str = num_of_people_following_str.strip()
            for c in num_of_people_following_str:
                if c.isdigit():
                    follow_count_str = follow_count_str + c
                else:
                    break
        follow_count = int(follow_count_str)
        # print(follow_count)
        author_element = response.css('#topic > article > div.author > div > h5 > a')
        author_name = author_element.css('::text').extract_first().strip()
        author_profile = URL_PREFIX + author_element.css('::attr(href)').extract_first().strip()
        # print(author_name)
        # print(author_profile)
        post_content = response.css('#post_content > input::attr(value)').extract_first()
        post_content = re.sub(r'\s+', ' ', post_content)
        # print(post_content)
        like_count_element = response.css('#post_content > p.post__stats::text').extract_first()
        like_count_parts = like_count_element.split(', ')
        like_count = like_count_parts[0][0: like_count_parts[0].find(' ')]
        reply_count = like_count_parts[1][0: like_count_parts[1].find(' ')]
        if like_count is None:
            like_count = '0'
        if reply_count is None:
            reply_count = '0'

        # print('like count: ' + str(like_count))
        # print('reply count: ' + str(reply_count))

        post_item = PIForumPostContentItem()
        post_item['post_group'] = self.group_url_to_group_name_map[response.url]
        post_item['post_url'] = response.url
        post_item['post_title'] = post_title
        post_item['post_time'] = post_time
        post_item['post_follow_count'] = follow_count
        post_item['post_author'] = author_name
        post_item['post_author_profile'] = author_profile
        post_item['post_content'] = post_content
        post_item['post_like_count'] = int(like_count)
        post_item['post_reply_count'] = int(reply_count)

        post_comments = []
        # post comments
        for comment in response.xpath('//*[@id="topic-replies"]/div[@class="comment-page"]/ul/li[@class="comment"]'):
            comment_url = comment.css('::attr(itemid)').extract_first()
            # print(comment_url)
            comment_header = comment.css('article > div.post__header')
            comment_author_ele = comment_header.css('div > div.author__summary > h5.author__info > a.author__name')
            comment_author = comment_author_ele.css('::text').extract_first()
            comment_author_profile = URL_PREFIX + comment_author_ele.css('::attr(href)').extract_first()
            # print(comment_author)
            # print(comment_author_profile)
            comment_time = comment_header.css('p > span > time::attr(datetime)').extract_first()
            # print(comment_time)

            comment_cont_ele = comment.css('article > div.post__content.break-word')
            comment_content = comment_cont_ele.css('input::attr(value)').extract_first()

            # don't crawl comments under moderation (we don't want to create comment item)
            if comment_content:
                comment_content = re.sub(r'\s+', ' ', comment_content)
                # print(comment_content)
                comment_like_count = comment_cont_ele.css('div.post__actions > a.post__ctrl.post__like.link > span::text').extract_first()
                if comment_like_count is None:
                    comment_like_count = 0
                else:
                    comment_like_count = int(comment_like_count)
                # print(comment_like_count)

                post_comment_item = PIForumPostCommentItem()
                post_comment_item['comment_url'] = comment_url
                post_comment_item['comment_author'] = comment_author
                post_comment_item['comment_author_profile'] = comment_author_profile
                post_comment_item['comment_time'] = comment_time
                post_comment_item['comment_content'] = comment_content
                post_comment_item['comment_like_count'] = comment_like_count

                sub_comments = []
                for sub_comment in comment.css('article > ul.comments.comments--nested > li.comment.comment--nested'):
                    sub_comment_url = sub_comment.css('::attr(itemid)').extract_first()
                    # print(sub_comment_url)
                    sub_comment_header = sub_comment.css('article > div.post__header')
                    sub_comment_author_ele = sub_comment_header.css(
                        'div > div.author__summary > h5.author__info > a.author__name')
                    sub_comment_author = sub_comment_author_ele.css('::text').extract_first()
                    sub_comment_author_profile = URL_PREFIX + sub_comment_author_ele.css('::attr(href)').extract_first()
                    # print(sub_comment_author)
                    # print(sub_comment_author_profile)

                    sub_comment_time = sub_comment_header.css('p > span > time::attr(datetime)').extract_first()
                    # print(sub_comment_time)

                    sub_comment_cont_ele = sub_comment.css('article > div.post__content.break-word')
                    sub_comment_content = sub_comment_cont_ele.css('input::attr(value)').extract_first()

                    if sub_comment_content:
                        sub_comment_content = re.sub(r'\s+', ' ', sub_comment_content)
                        # print(sub_comment_content)
                        sub_comment_like_count = sub_comment_cont_ele.css(
                            'div.post__actions > a.post__ctrl.post__like.link > span::text').extract_first()
                        if sub_comment_like_count is None:
                            sub_comment_like_count = 0
                        else:
                            sub_comment_like_count = int(sub_comment_like_count)
                        # print(sub_comment_like_count)

                        post_sub_comment_item = PIForumPostCommentItem()
                        post_sub_comment_item['comment_url'] = sub_comment_url
                        post_sub_comment_item['comment_author'] = sub_comment_author
                        post_sub_comment_item['comment_author_profile'] = sub_comment_author_profile
                        post_sub_comment_item['comment_time'] = sub_comment_time
                        post_sub_comment_item['comment_content'] = sub_comment_content
                        post_sub_comment_item['comment_like_count'] = sub_comment_like_count

                        # add post sub comment item
                        sub_comments.append(post_sub_comment_item)

                # set sub comments if available for the comment
                if len(sub_comments) > 0:
                    post_comment_item['sub_comments'] = sub_comments

                # add post comment to list of comment items
                post_comments.append(post_comment_item)

        # set post comments if available for the post
        if len(post_comments) > 0:
            post_item['post_comments'] = post_comments

        # return post item which contains relevant crawled information
        yield post_item


# some posts have nested replies
# https://patient.info/forums/discuss/stomach-cramp-and-pain-diarrhea-and-vomiting--732943
# some posts have paginated replies
# https://patient.info/forums/discuss/abdominal-pain-right-side-under-ribs-and-back-pain-497946
# some posts have hidden comments(marked for moderation)
# https://patient.info/forums/discuss/corona-virus-spray-733013
# list element has a few advertisement elements
# https://patient.info/forums/discuss/gastritis-after-eating-feeling-fullness-dizziness-shortness-of-breath-and-lump-in-my-throat--732202
# nested comments can also have like count
# https://patient.info/forums/discuss/lpr-acid-reflux-indigestion-and-pain-under-left-ribcage-732193
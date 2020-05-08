import scrapy


class PIForumLinkItem(scrapy.Item):
    forum_name = scrapy.Field()
    forum_url = scrapy.Field()


class PIForumPostLinkItem(scrapy.Item):
    group_name = scrapy.Field()
    post_title = scrapy.Field()
    post_url = scrapy.Field()


class PIForumPostContentItem(scrapy.Item):
    post_group = scrapy.Field()
    post_url = scrapy.Field()
    post_title = scrapy.Field()
    post_time = scrapy.Field()
    post_follow_count = scrapy.Field()
    post_author = scrapy.Field()
    post_author_profile = scrapy.Field()
    post_content = scrapy.Field()
    post_like_count = scrapy.Field()
    post_reply_count = scrapy.Field()
    post_comments = scrapy.Field()


class PIForumPostCommentItem(scrapy.Item):
    comment_url = scrapy.Field()
    comment_author = scrapy.Field()
    comment_author_profile = scrapy.Field()
    comment_time = scrapy.Field()
    comment_content = scrapy.Field()
    comment_like_count = scrapy.Field()
    # for sub comment item this will not be set
    sub_comments = scrapy.Field()
import scrapy


class DrugDetailPageLinkItem(scrapy.Item):
    name = scrapy.Field()
    detail_page_url = scrapy.Field()


class DrugReviewPageLinkItem(scrapy.Item):
    name = scrapy.Field()
    detail_page_url = scrapy.Field()
    detail_page_redirected_url = scrapy.Field()
    review_page_url = scrapy.Field()
    all_review_page_urls = scrapy.Field()


class DrugReviewItem(scrapy.Item):
    drug_name = scrapy.Field()
    drug_detail_page = scrapy.Field()
    drug_review_page = scrapy.Field()
    health_condition_name = scrapy.Field()
    timestamp = scrapy.Field()
    reviewer_full_det = scrapy.Field()
    reviewer_name = scrapy.Field()
    patient_age_range = scrapy.Field()
    patient_gender = scrapy.Field()
    treatment_duration = scrapy.Field()
    # Patient or Caregiver
    reviewer_category = scrapy.Field()
    review_comment = scrapy.Field()
    num_of_people_found_useful = scrapy.Field()
    effectiveness_rating = scrapy.Field()
    ease_of_use_rating = scrapy.Field()
    satisfaction_rating = scrapy.Field()


Crawling status: completed

Steps to run WebMD drugs review crawler(Scrapy based - Python):

1. Install Scrapy using following command:
    pip3 install Scrapy

2. From this current directory run the following command to grab all drugs and details page link:
    scrapy crawl webmd_drug_detail_page_crawler -t json -o webmd_drug_detail_urls.json
This will grab all drugs detail page link and store in the passed json file name.

3. Then run the following command to grab review page links for all the drugs:
    scrapy crawl webmd_drug_review_page_crawler -t json -o webmd_drug_review_urls.json
This will grab all the drugs review page links and store in the passed json file name.    

4. Then run the following commands to crawl all the drug reviews one by one:
    scrapy crawl webmd_drug_review_crawler -t json -o webmd_drugs_reviews.json   

Library used(should be installed before running):
1. Scrapy
2. beautifulsoup4


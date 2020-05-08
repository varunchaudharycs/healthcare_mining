Crawling status: crawled 236490 unique forum posts.

Steps to run patient.info forum crawler(Scrapy based - Python):

1. Install Scrapy using following command:
    pip3 install Scrapy

2. From this current directory run the following command to grab links of all community forums:
    scrapy crawl pi_forums_crawler -t json -o patient_info_forums.json
This will grab all the community forums home page link and store in the passed json file name.

3. Then run the following command to grab links of all the forum posts from all the community
forums:
    scrapy crawl pi_forum_posts_crawler  -t json -o patient_info_forum_posts.json
This will grab all the forum post links from all the forums and store in the passed json file name.    

4. Then run the following commands to crawl all the forum posts one by one:
    scrapy crawl pi_forum_posts_content_crawler  -t json -o patient_info_forum_posts_content.json    

Library used(should be installed before running):
1. Scrapy
2. beautifulsoup4

### Handling Large JSON files:
- install git lfs if not already:
git lfs install
- if your git pull does not work properly for large files:
git lfs pull
- to track large files:
git lfs track <specific_json_file_name>

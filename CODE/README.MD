- Crawlers directory has source code for all four crawlers which we wrote. Each crawler has execution instructions to run and crawl the data.
- patient_info_crawler is Python Scrapy based crawler
- webmd_drug_crawler is also Python Scrapy based crawler
- webmd_mb_crawler is Browser automation based crawler as we were not able to crawl using Python based crawler.
- Scraping Mayo.ipynb is simple python code based crawler.

- healthcare_mining_webapp is the web application built using HTML, CSS, JavaScrip for the front-end and Java Servlets in the server end and deployed on Apache Tomcat Server. 
- solr_server is contains the solr version(8.5) which we have used to index and search and rank our search results. For convenience of setup and running we have checked in the solr version we are using, the configuration we are using and also the index which we have created.
- DataIndexer contains the Python code which we have used to preprocess, annotate using UMLS MetaMap, and then send indexing request to our Web Applications which further processes the data and ensures the data gets indexed to right Solr core and with right field configuration. This also contains a simple Python Server which we used as a way to communicate Java Web Application and MetaMeta framework, so that we can annotate/extract meaningful data during the search query processing.

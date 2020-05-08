Crawling status: completed

Steps to run WebMD Message Boards Browser Automation based crawler:

1. install node.js if not already installed on your machine.
2. move to the webmd_mb_crawler directory
3. run the following command to install the application dependency:
    npm install
4. run the application using the following command:
    npm start app.js
5. crawl the forum posts links by invoking link crawler(access the following link from your browser):
    http://localhost:8080/webmd/msgboards/crawllinks
6. crawl the forum posts by invoking posts crawler(access the following link from your browser):  
    http://localhost:8080/webmd/msgboards/crawlposts
    Before invoking this ensure that the links has been crawled and saved under links_json directory.

const puppeteer = require('puppeteer');
const fs = require("fs");
const jsdom = require("jsdom")

const { JSDOM } = jsdom
global.DOMParser = new JSDOM().window.DOMParser

const isHeadless = false

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

async function crawlForumPost(page, forum_post_url) {
    console.log(forum_post_url);
    await page.goto(forum_post_url,
        { waitUntil: 'networkidle2', timeout: 0 })

    await delay(500);

    var forumPost = await page.evaluate((forum_post_url) => {
        var postUserDetails = document.querySelectorAll('#pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.user-detail');
        var likeDetailsNodeList = document.querySelectorAll('#pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.thread-meta > div.social > span.ui-like.ui-tip > span');
        var postThreadDetailsNodeList = document.querySelectorAll('#pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.thread-detail');
        var postTagsNodeList = document.querySelectorAll('#pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.thread-tags > ul > li');
        var responseNodeList = document.querySelectorAll('#pi73-paged-content > ul.content-list.content.thread-list.margin-bottom.webmd-mb-rsp > li');
        // #pi73-paged-content > ul.content-list.content.thread-list.margin-bottom.webmd-mb-rsp > li:nth-child(1)
        // #pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd
        // #pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.user-detail
        // #pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.thread-detail
        // #pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.thread-tags > ul > li
        // #\31 13129 > div.thread-meta > div.social > span.ui-like.ui-tip > span
        // #pi73-paged-content > ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd > li > div.thread-meta > div.social > span.ui-like.ui-tip > span

        if (postUserDetails != null && postUserDetails.length > 0) {
            const postUserDetailsFields = postUserDetails[0].innerText.trim().split('\n');
            const postDetailsStr = postThreadDetailsNodeList[0].innerText.trim();
            const startIndexOfContent = postDetailsStr.indexOf('\n');

            // parse tags if there exists one
            var tags = []
            for (var t = 0; t < postTagsNodeList.length; t++) {
                tags[t] = postTagsNodeList[t].innerText.trim();
            }

            var likeCount = '0';
            if (likeDetailsNodeList.length > 0) {
                likeCount = likeDetailsNodeList[0].innerText.trim()
            }

            // create post details object
            const postDetails = {
                author: postUserDetailsFields[0].trim(),
                post_time: postUserDetailsFields[1].trim(),
                post_title: postDetailsStr.substr(0, startIndexOfContent).trim(),
                post_content: postDetailsStr.substr(startIndexOfContent).trim(),
                like_count: likeCount,
                tags: tags
            };

            // if there exists responses/reply in this forum post, index as part of the post
            var responses = [];
            for (var j = 0; j < responseNodeList.length; j++) {
                var responseText = responseNodeList[j].innerText.trim();
                var indexOfNewlineChar = responseText.indexOf('\n');
                const respAuthor = responseText.substr(0, indexOfNewlineChar);
                responseText = responseText.substr(indexOfNewlineChar + 1);
                indexOfNewlineChar = responseText.indexOf('\n');
                const respTime = responseText.substr(0, indexOfNewlineChar);
                responseText = responseText.substr(indexOfNewlineChar + 1);
                indexOfNewlineChar = responseText.indexOf('\n');
                const respTitle = responseText.substr(0, indexOfNewlineChar);
                responseText = responseText.substr(indexOfNewlineChar + 1);
                const respContent = responseText.substr(0, responseText.lastIndexOf('Reply'));

                responses[j] = {
                    author: respAuthor,
                    resp_time: respTime,
                    resp_title: respTitle,
                    resp_content: respContent
                };
            }

            // return to enclosing method
            return {
                post: postDetails,
                responses: responses
            };
        }

    });

    if (forumPost != null) {
        // add forum post url to the json
        forumPost['post_url'] = forum_post_url;

        // console.log(forumPost);
        return forumPost;
    }
}

exports.crawlForumPosts = async function () {

    pagename = "WebMD"
    const browser = await puppeteer.launch({ headless: isHeadless })
    const context = browser.defaultBrowserContext();
    const page = await browser.newPage()
    await page.setViewport({ width: 1280, height: 800 })

    // for (var i = 0; i < postLinksJSONFiles.length; i++) {
    for (var forum_name in postLinksJSONFiles) {
        const jsonFile = postLinksJSONFiles[forum_name];
        console.log('Crawling: ' + jsonFile);

        var forumLinks;
        fs.readFile(jsonFile, 'utf8', function (err, jsonString) {
            if (err) {
                console.log("Error reading file from disk:", err);
            }
            forumLinks = JSON.parse(jsonString);
        });

        // wait to finish reading and parsing link file
        await delay(500);

        try {
            forumPosts = [];
            for (var j = 0; j < forumLinks.length; j++) {
                var postDetails = await crawlForumPost(page, forumLinks[j]);
                // if some error happens for some URL we will discard that empty object
                if (postDetails != null) {
                    forumPosts[j] = postDetails;
                }
            }

            // finished crawling all posts from this json file, write crawled post as json
            fs.writeFile("./posts_json/" + forum_name + "-posts.json", JSON.stringify(forumPosts), function (err) {
                if (err) {
                    console.log("Error while writing the posts json file: ", err)
                }

                console.log("Posts saved for forum name: " + forum_name);
            });
        }
        catch (err) {
            console.log('Error parsing JSON string:', err);
        }
    }

    console.log("Finished crawling, closing the Browser!");
    console.log("Press Ctrl+C to quit.")
    await browser.close();
}

// link json files
// cancer creating issue
postLinksJSONFiles = {
    adhd: './links_json/adhd-post_links.json',
    allerrgies: './links_json/allerrgies-post_links.json',
    arthritis: './links_json/arthritis-post_links.json',
    asthma: './links_json/asthma-post_links.json',
    bnsd: './links_json/bnsd-post_links.json',
    cancer: './links_json/cancer-post_links.json',
    diabetes: './links_json/diabetes-post_links.json',
    digestive: './links_json/digestive-post_links.json',
    earnosethroat: './links_json/earnosethroat-post_links.json',
    eye: './links_json/eye-post_links.json',
    fibromyalgia: './links_json/fibromyalgia-post_links.json',
    heart: './links_json/heart-post_links.json',
    hepatitisc: './links_json/hepatitisc-post_links.json',
    hiv: './links_json/hiv-post_links.json',
    kidney: './links_json/kidney-post_links.json',
    lupus: './links_json/lupus-post_links.json',
    mental: './links_json/mental-post_links.json',
    oralhealth: './links_json/oralhealth-post_links.json',
    osteoporosis: './links_json/osteoporosis-post_links.json',
    painmanage: './links_json/painmanage-post_links.json',
    sclerosis: './links_json/sclerosis-post_links.json',
    sexhealthstd: './links_json/sexhealthstd-post_links.json',
    sleep: './links_json/sleep-post_links.json',
    stroke: './links_json/stroke-post_links.json'
};

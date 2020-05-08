const puppeteer = require('puppeteer');
const fs = require("fs");
const jsdom = require("jsdom")

const { JSDOM } = jsdom
global.DOMParser = new JSDOM().window.DOMParser

const isHeadless = false

// async function goToPage(page, post_url) {
//     await page.goto(post_url,
//         { waitUntil: 'networkidle2' })

//     post_links = [];
//     for (i = 1; i <= 10; i++) {
//         xpathExpr = '//*[@id="pi37-paged-content"]/ul/li[' + i + ']/div[2]/h3/a';
//         const [element] = await page.$x(xpathExpr);
//         post_links.push(await (await element.getProperty('href')).jsonValue());
//     }
// }

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

async function crawlLinksFromForum(page, forum_url, page_index, post_links) {
    console.log(forum_url);
    await page.goto(forum_url,
        { waitUntil: 'networkidle2' })

    await delay(3000);

    for (i = 1; i <= 10; i++) {
        xpathExpr = '//*[@id="pi37-paged-content"]/ul/li[' + i + ']/div[2]/h3/a';
        const [element] = await page.$x(xpathExpr);
        if (element != null) {
            const postLink = await (await element.getProperty('href')).jsonValue()
            if (post_links.indexOf(postLink) > -1) {
                return;
            }
            else {
                post_links.push(postLink);
                // prev_page_links.push(postLink);
            }
        }
        else {
            if (i < 10) {
                //finished crawling this forum as it reached end by doing pagination
                return;
            }
        }
    }

    page_index++;
    await crawlLinksFromForum(page, forum_url.substr(0, forum_url.indexOf("#pi37=")) + "#pi37=" + page_index, page_index, post_links);
}

exports.crawlLinksFromForums = async function () {

    pagename = "WebMD"
    const browser = await puppeteer.launch({ headless: isHeadless })
    const context = browser.defaultBrowserContext();
    const page = await browser.newPage()
    await page.setViewport({ width: 1280, height: 800 })

    for (var forum_name in forums) {
        forum_url = forums[forum_name];
        post_links = [];
        prev_page_links = [];
        await crawlLinksFromForum(page, forum_url, 1, post_links);
        console.log(post_links);

        fs.writeFile("./links_json/" + forum_name + "-post_links.json", JSON.stringify(post_links), function (err) {
            if (err) {
                console.log("Error while writing the links json file: ", err)
            }
            console.log("Links saved for forum name: " + forum_name);
        });
    }

    console.log("Finished crawling, closing the Browser!");
    console.log("Press Ctrl+C to quit.")
    await browser.close();
}

// 12,696 around these many unique posts
var forums = {
    adhd: 'https://messageboards.webmd.com/health-conditions/f/add-adhd#pi37=1',
    allerrgies: 'https://messageboards.webmd.com/health-conditions/f/allergies#pi37=1',
    arthritis: 'https://messageboards.webmd.com/health-conditions/f/arthritis#pi37=1',
    asthma: 'https://messageboards.webmd.com/health-conditions/f/asthma#pi37=1',
    bnsd: 'https://messageboards.webmd.com/health-conditions/f/brain-nervous-system-disorder#pi37=1',
    cancer: 'https://messageboards.webmd.com/health-conditions/f/cancer#pi37=1',
    diabetes: 'https://messageboards.webmd.com/health-conditions/f/diabetes#pi37=1',
    digestive: 'https://messageboards.webmd.com/health-conditions/f/digestive-health#pi37=1',
    earnosethroat: 'https://messageboards.webmd.com/health-conditions/f/ear-nose-throat#pi37=1',
    eye: 'https://messageboards.webmd.com/health-conditions/f/eye-health#pi37=1',
    fibromyalgia: 'https://messageboards.webmd.com/health-conditions/f/fibromyalgia#pi37=1',
    heart: 'https://messageboards.webmd.com/health-conditions/f/heart-health#pi37=1',
    hepatitisc: 'https://messageboards.webmd.com/health-conditions/f/hepatitis-c#pi37=1',
    hiv: 'https://messageboards.webmd.com/health-conditions/f/hiv-aids#pi37=1',
    kidney: 'https://messageboards.webmd.com/health-conditions/f/kidney-disorders#pi37=1',
    lupus: 'https://messageboards.webmd.com/health-conditions/f/lupus#pi37=1',
    mental: 'https://messageboards.webmd.com/health-conditions/f/mental-health#pi37=1',
    oralhealth: 'https://messageboards.webmd.com/health-conditions/f/oral-health#pi37=1',
    osteoporosis: 'https://messageboards.webmd.com/health-conditions/f/osteoporosis#pi37=1',
    painmanage: 'https://messageboards.webmd.com/health-conditions/f/pain-management#pi37=1',
    sclerosis: 'https://messageboards.webmd.com/health-conditions/f/multiple-sclerosis#pi37=1',
    sexhealthstd: 'https://messageboards.webmd.com/health-conditions/f/sexual-health-stds#pi37=1',
    sleep: 'https://messageboards.webmd.com/health-conditions/f/sleep#pi37=1',
    stroke: 'https://messageboards.webmd.com/health-conditions/f/stroke#pi37=1'
};
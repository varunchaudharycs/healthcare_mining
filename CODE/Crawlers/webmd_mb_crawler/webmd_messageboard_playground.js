const puppeteer = require('puppeteer');                                                                                                                                                                             
const jsdom = require("jsdom")
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
var fs = require("fs");

const {JSDOM} = jsdom
global.DOMParser = new JSDOM().window.DOMParser


const csvWriter = createCsvWriter({
    path: './stroke.csv',
    header: [
        {id: 'url', title: 'URL'}
    ]
});

const isHeadless = false

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

// new goToPage implementation which navigates to specific post url
// to simulate text comment and image comment
async function goToPage(page, post_url) {

    await page.goto(post_url,
        { waitUntil: 'networkidle2' })
    
    await page.waitForSelector('#pi37-paged-content')
    //const textContent = await page.evaluate(() => document.querySelector('#pi37-paged-content').textContent);
    //const innerText = await page.evaluate(() => document.querySelector('#pi37-paged-content').innerText);

    //console.log(textContent);
    //console.log(innerText);
    // var url = await page.$x('*[@id="pi37-paged-content"]/ul/li[2]/div[2]/h3/a');
    //await page.evaluate(() => document.querySelector('#pi37-paged-content > ul > li:nth-child(2) > div.thread-detail > h3 > a').href));
    // console.log(url);
    // //*[@id="pi37-paged-content"]/ul/li[2]/div[2]/h3/a
    

        // //*[@id="pi37-paged-content"]

        // const [elementHandle] = await page.$x('.//a/@href');
    // const propertyHandle = await elementHandle.getProperty('value');
    // const propertyValue = await propertyHandle.jsonValue();

    //#pi37-paged-content > ul > li:nth-child(1)
    // const [element] = await page.$x('//*[@id="pi37-paged-content"]');
    for (i = 0; i < 10; i++) {
        xpathExpr = '//*[@id="pi37-paged-content"]/ul/li[' + i + ']/div[2]/h3/a';
        const [element] = await page.$x(xpathExpr);
        console.log(await (await element.getProperty('href')).jsonValue());
      }
    
    //   const [element] = await page.$x('//*[@id="pi37-paged-content"]/ul/li[2]/div[2]/h3/a');
    // '//*[@id="pi37-paged-content"]/ul/li[2]/div[2]/h3/a'
    // const [element] = await page.evaluate(() => document.querySelectorAll('#pi37-paged-content > ul > li'))
    // console.log(await element.getProperty('href'));
    // console.log(await (await element.getProperty('href')).jsonValue());

    
    // sel = '#pi37-paged-content > ul > li'
    // await page.evaluate((sel) => {
    //     let elements = Array.from(document.querySelectorAll(sel));
    //     console.log("hi");
    //     console.log(elements)
    //     // let links = elements.map(element => {
    //     //     return element.href
    //     // })
    //     // return links;
    // }, sel);

    // const posts = await page.evaluate(() => Array.from(document.querySelectorAll('#pi37-paged-content > ul > li')))
    // console.log(posts[0]);

    // const posts = await page.evaluate(() => Array.from(document.querySelectorAll('#pi37-paged-content > ul > li')))
    // const posts = await page.evaluate(() => document.querySelectorAll('#pi37-paged-content > ul > li'))
    // const post_urls = await page.evaluate((...posts) => {
    //     return posts.map(e => e.innerHTML);
    // }, ...posts);

    // console.log(link_urls);

    //element.querySelectorAll('#div.thread-detail > h3 > a')));
    //console.log(posts[0]);
    // console.log(posts[1]);

    ////*[@id="pi37-paged-content"]/ul/li[2]/div[1]
    // const records = [];
    // var arrayLength = posts.length;
    // for (var i = 0; i < arrayLength; i++) {
	// //console.log('posts id: ' + i);
	// //console.log(posts[i]);
	// //console.log(posts[i]);
	// const text = await page.evaluate(el => {
    //     // do what you want with featureArticle in page.evaluate
	//     return el.textContent;
	// }, posts[i]);
	// console.log(text);
	// //const url = posts[i].querySelectorAll('#div.thread-detail > h3 > a').href;
	// //console.log(url);
    // }

    //#div.thread-detail > h3 > a

    /*
    // the selector for the comment div has class=_7c-t
    await page.waitForSelector('._7c-t')
    await page.click('._7c-t')
    await page.waitForSelector('div[aria-label="Write a comment..."]')
    // type the comment text, in this case "test"
    await page.keyboard.type("test");
    // simulate submit using keyboard enter
    await page.keyboard.press('Enter');

    // simulate file picker, with assumption that image file is accessible
    const [fileChooser] = await Promise.all([
        page.waitForFileChooser(),
        // the anchor tag which triggers file selection dialog
        page.click('a[aria-label="Attach a photo or video"]'),
    ]);
    await fileChooser.accept([filePath]);

    await delay(2000);
    // the selctor after the image selection happens changes to one with class=_5rpu
    await page.waitForSelector('._5rpu')
    await page.click('._5rpu')
    await page.keyboard.press('Enter');
    */
}

exports.gotopage = async function(post_url){
    pagename = "goodrx"
    const browser = await puppeteer.launch({headless: isHeadless})
    const context = browser.defaultBrowserContext();
    //context.overridePermissions("https://www.facebook.com", ["geolocation", "notifications"]);
    const page = await browser.newPage()

    await page.setViewport({width: 1280, height: 800})

    // changes to pass the facebook post url
    await goToPage(page, 'https://messageboards.webmd.com/health-conditions/f/stroke');

    await browser.close();
}

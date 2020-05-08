'use strict';

const express = require('express');
const link_crawler = require('./webmd_mb_link_crawler.js')
const post_crawler = require('./webmd_mb_post_crawler.js')

const app = express();

app.get('/', (req, res) => {
  res
    .status(200)
    .send('Hello Jumping, world!')
    .end();
});

app.get('/webmd/msgboards/crawllinks', async (req, res) => {

  await link_crawler.crawlLinksFromForums();

  res
    .status(200)
    .send('Opening WebMD Message Boards...')
    .end();

});

app.get('/webmd/msgboards/crawlposts', async (req, res) => {

  // crawl posts from the link json files
  await post_crawler.crawlForumPosts();

  res
    .status(200)
    .send('Opening WebMD Message Boards...')
    .end();

});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

// export the nodejs app
module.exports = app;

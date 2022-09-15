import axios from "axios";
import puppeteer from "puppeteer";
import { load } from "cheerio";
import fs from "fs";
import { GUIDE_URLS, IGNORE_LINKS } from "./data.js";

const SCRAPER_API_URL = "http://api.scraperapi.com";
const SCRAPER_API_KEY = "<SCRAPER_API_KEY>";

let browser;
let page;

const scrapeData = async (url, writeStream) => {
  const html = await fetchData(url);
  if (!html) {
    console.log("Error occurred while fetching data");
    return;
  }

  const $ = load(html);
  const links = $("a");
  let pageData;

  // specific selction of classes found in liesg guide pages
  if ($("div[class*='base-page__PageLayout']").length) {
    pageData = $("div[class*='base-page__PageLayout']");
  } else if ($("div[class*='ContentWrapper']").length) {
    pageData = $("div[class*='ContentWrapper']");
  } else if ($("div[class*='content']").length) {
    pageData = $("div[class='content']");
  } else {
    return "No data found!";
  }

  // Append spaces in between elements to prevent text clumping
  $("body").each(function () {
    $(this).append(" ");
  });

  writeStream.write(pageData.text());
  console.log("Crawling data in external links...");
  await scrapeExternalLinks(links, $, writeStream);
};

const scrapeExternalLinks = async (links, $, writeStream) => {
  for (const link of links) {
    const url = $(link).attr("href");

    if (
      !url ||
      IGNORE_LINKS.includes(url) ||
      !url.startsWith("http") ||
      url.includes(".png") ||
      url.includes(".jpg") ||
      url.includes(".pdf") ||
      url.includes("services2.hdb.gov.sg") ||
      url.includes("https://t.me/")
    ) {
      continue;
    }

    if (!url.includes("www.life.gov.sg") && !url.includes("go.gov.sg") && !url.startsWith("/") && !url.startsWith(".")) {
      const html = await fetchData(url);
      if (!html) {
        continue;
      }

      const $ = load(html);

      // Append spaces in between elements to prevent text clumping
      $("*").each(function () {
        $(this).append(" ");
      });

      $("header").remove();
      $("script").remove();
      $("footer").remove();
      $("style").remove();
      $("iframe").remove();
      $("noscript").remove();

      // writeStream.write(url);
      writeStream.write($("body").text());
      // writeStream.write($("body").prop("innerText") || "");
    }
  }
};

const fetchData = async (url) => {
  console.log(`Crawling data in ${url}...`);
  // make http call to url
  // let response = await axios(url).catch((err) => {});
  // let response = await axios(SCRAPER_API_URL, { params: { api_key: SCRAPER_API_KEY, url } }).catch((err) => console.log(err));
  try {
    const res = await page.goto(url, { timeout: 60000 });

    if (!res || res.status() === 404) {
      console.log("Page not found");
      return;
    }

    let bodyHTML = await page.evaluate(() => document.body.innerHTML);

    if ((res.status() !== 200 && bodyHTML.includes("404")) || bodyHTML.toLowerCase().includes("page not found")) {
      console.log("Page not found");
      return;
    }

    return bodyHTML;
  } catch (e) {
    console.log("Error occurred while fetching data");
    console.log(e);
    return;
  }
};

async function main() {
  browser = await puppeteer.launch();
  page = await browser.newPage();

  for (let guide = 0; guide < GUIDE_URLS.length; guide++) {
    //   create file stream
    const writeStream = fs.createWriteStream(`../data/Guide ${guide + 1}.txt`);
    console.log(`Crawling data in internal guide...`);
    await scrapeData(GUIDE_URLS[guide], writeStream);

    // fs.writeFileSync(`data/Guide ${guide + 1}.txt`, text);
    writeStream.close();
  }

  await browser.close();
}

main();

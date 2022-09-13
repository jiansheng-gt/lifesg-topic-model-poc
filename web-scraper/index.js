import axios from "axios";
import { load } from "cheerio";
import fs from "fs";
import { GUIDE_URLS, IGNORE_LINKS } from "./data.js";

const SCRAPER_API_URL = "http://api.scraperapi.com";
const SCRAPER_API_KEY = "<SCRAPER_API_KEY>";

const scrapeData = async (url, writeStream) => {
  const res = await fetchData(url);
  if (!res) {
    return;
  }
  const html = res.data;
  const $ = load(html);
  const links = $("a");
  await scrapeExternalLinks(links, $, writeStream);
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
};

const scrapeExternalLinks = async (links, $, writeStream) => {
  for (const link of links) {
    const url = $(link).attr("href");

    if (
      !url ||
      IGNORE_LINKS.includes(url) ||
      !url.startsWith("http") ||
      url.endsWith("png") ||
      url.endsWith("pdf") ||
      url.includes("services2.hdb.gov.sg")
    ) {
      continue;
    }

    if (!url.includes("www.life.gov.sg") && !url.includes("go.gov.sg") && !url.startsWith("/") && !url.startsWith(".")) {
      const res = await fetchData(url);
      if (!res) {
        continue;
      }
      const html = res.data;
      const $ = load(html);

      // Append spaces in between elements to prevent text clumping
      $("body").each(function () {
        $(this).append(" ");
      });

      // $("body")
      //   .find("*")
      //   .filter(function (i, el) {
      //     if ($(this).attr("class") === "catalogItemWebpart") {
      //       console.log("found it");
      //       console.log("css", $(this).css("display"));
      //       // console.log($.html(this));
      //     }
      //     var display = $(this).css("display");
      //     if (display === "none") {
      //       // console.log($.html(this));
      //       console.log($(this).attr("class"));
      //       $(this).remove();
      //     }
      //   });

      $("header").remove();
      $("script").remove();
      $("footer").remove();
      $("style").remove();
      $("iframe").remove();
      $("noscript").remove();

      writeStream.write(url);
      // writeStream.write($("body").text());
      writeStream.write($("body").prop("innerText") || "");
    }
  }
};

const fetchData = async (url) => {
  console.log(`Crawling data in ${url}...`);
  // make http call to url
  let response = await axios(url).catch((err) => {});
  // let response = await axios(SCRAPER_API_URL, { params: { api_key: SCRAPER_API_KEY, url } }).catch((err) => console.log(err));

  if (!response || response.status !== 200) {
    console.log("Error occurred while fetching data");
    return;
  }
  return response;
};

async function main() {
  for (let guide = 0; guide < GUIDE_URLS.length; guide++) {
    //   create file stream
    const writeStream = fs.createWriteStream(`data-inner-text/Guide ${guide + 1}.txt`);
    await scrapeData(GUIDE_URLS[guide], writeStream);

    // fs.writeFileSync(`data/Guide ${guide + 1}.txt`, text);
    writeStream.close();
  }
}

main();

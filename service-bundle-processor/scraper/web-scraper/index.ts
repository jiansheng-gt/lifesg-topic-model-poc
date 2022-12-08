import { CheerioAPI, load } from "cheerio";
import puppeteer, { Browser, Page } from "puppeteer";
import { IGNORE_LINKS, URL_EXCLUSIONS } from "./constants";

class WebScraper {
	private browser: Browser;
	private page: Page;

	public async init() {
		this.browser = await puppeteer.launch();
		this.page = await this.browser.newPage();
	}

	public async close() {
		return this.browser.close();
	}

	public async scrape(url: string, scrapeExternalLinks: boolean) {
		console.log(`Crawling data in ${url}...`);

		const documents: string[] = [];
		let externalDocuments: string[];
		const html = await this.fetchHtml(url);
		if (!html) {
			console.log("Error occurred while fetching data");
			return;
		}

		const $ = load(html);
		const links = Array.from($("a")).map((elem) => $(elem).attr("href"));

		// Base link
		if (url.includes("life.gov.sg/guides/") || url.includes("services.life.gov.sg/")) {
			documents.push(this.processGuidePage($));
		} else {
			documents.push(this.processPage($));
		}

		// External links
		if (scrapeExternalLinks) {
			externalDocuments = await this.scrapeExternalLinks(links);
		}

		return documents.concat(externalDocuments).join(" ");
	}

	private processPage($: CheerioAPI) {
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

		return $("body").text().trim();
	}

	private processGuidePage($: CheerioAPI) {
		// specific selction of classes found in lifesg guide pages
		const guidesElement1 = $("div[class*='base-page__PageLayout']");
		const guidesElement2 = $("div[class*='ContentWrapper']");
		const servicesElement = $("div[class*='content']");

		const pageData = guidesElement1.length
			? guidesElement1
			: guidesElement2.length
				? guidesElement2
				: servicesElement.length
					? servicesElement
					: null;

		if (!pageData) {
			return this.processPage($);
		}

		// Append spaces in between elements to prevent text clumping
		$("*").each(function () {
			$(this).append(" ");
		});

		// Remove suggested pages section
		$("div[class*=suggested-page]").remove();
		let content = pageData.text();
		while (content.indexOf("You may also be interested in") > -1) {
			content = content.replace("You may also be interested in", "");
		}

		return content;
	}

	private async scrapeExternalLinks(links: string[]) {
		const externalDocs: string[] = [];

		for await (const [index, url] of links.entries()) {
			console.log(`Crawling external link ${index + 1} out of ${links.length}`)
			if (
				!url ||
				!url.startsWith("http") ||
				url.startsWith("/") ||
				url.startsWith(".") ||
				IGNORE_LINKS.includes(url) ||
				URL_EXCLUSIONS.some((exclusion) => url.includes(exclusion))
			) {
				continue;
			}

			const html = await this.fetchHtml(url);

			if (!html) {
				continue;
			}

			const $ = load(html);

			externalDocs.push(this.processPage($));
		}

		return externalDocs;
	}

	private async fetchHtml(url: string) {
		try {
			const res = await this.page.goto(url, { timeout: 60000 });

			if (!res || res.status() === 404) {
				console.log("Page not found");
				return;
			}

			const bodyHTML = await this.page.evaluate(() => document.body.innerHTML);

			if (
				(res.status() !== 200 && bodyHTML.includes("404")) ||
				bodyHTML.toLowerCase().includes("page not found")
			) {
				console.log("Page not found");
				return;
			}

			return bodyHTML;
		} catch (e) {
			console.log("Error occurred while fetching data", e);
			return;
		}
	}
}

export const webScraper = new WebScraper();

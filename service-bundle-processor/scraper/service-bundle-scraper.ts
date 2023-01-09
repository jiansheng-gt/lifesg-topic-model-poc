import * as fs from "fs";
import { ArticleSummaryApiDomain } from "mol-lib-api-contract/content/mobile-content";
import * as path from "path";
import "reflect-metadata";
import { getArticlesAndSchemes, getServiceBundles, getServicesForBundle } from "./api";
import { webScraper } from "./web-scraper";

const OUTPUT_DIR = path.resolve(__dirname, "../data");

interface SentenceTransformerInput {
	contentType: "service_bundles";
	itemId: string;
	title: string;
	text: string;
}

interface WebScraperInput extends SentenceTransformerInput {
	urls: string[];
	scrapeExternalLinks: boolean;
}

(async () => {
	const serviceBundles = await getServiceBundles();

	const webScraperInput = await Promise.all(
		serviceBundles.map<Promise<WebScraperInput>>(async ({ id, title, serviceBundleUrl, topics, audiences }) => {
			if (serviceBundleUrl) {
				return {
					contentType: "service_bundles",
					itemId: id,
					title,
					urls: [serviceBundleUrl],
					text: "",
					scrapeExternalLinks: true,
				};
			}

			// get data of services within bundle
			const services = await getServicesForBundle(id);

			const textsArr: string[] = [];

			// add title, subtitle, summary to text
			services.featuredServices.forEach(({ title, subtitle, summary }) => {
				textsArr.push(title, subtitle, summary);
			});

			services.services.forEach(({ title, subtitle, summary }) => {
				textsArr.push(title, subtitle, summary);
			});

			// get related articles/schemes
			const articlesAndSchemes = await getArticlesAndSchemes(topics, audiences);

			return {
				contentType: "service_bundles",
				itemId: id,
				title,
				urls: (articlesAndSchemes.data.content as ArticleSummaryApiDomain[]).map(
					({ articleUrl }) => articleUrl,
				),
				text: textsArr.filter((val) => val.length > 0).join(" "),
				scrapeExternalLinks: false,
			};
		}),
	);

	await webScraper.init();

	const result: SentenceTransformerInput[] = [];

	for await (const [
		index,
		{ contentType, itemId, title, text, urls, scrapeExternalLinks },
	] of webScraperInput.entries()) {
		console.log(`[${index + 1}/${webScraperInput.length}] Crawling data for "${title}" (itemId: ${itemId})...`);
		// all urls in one item
		const data: string[] = [];
		for await (const url of urls) {
			const scraped = await webScraper.scrape(url, scrapeExternalLinks);
			data.push(scraped);
		}

		result.push({
			contentType,
			itemId,
			text: text + " " + data.join(" "),
			title,
		});

		console.log(`Finished crawling "${title}"!\n\n`);
	}
	await webScraper.close();

	if (!fs.existsSync(OUTPUT_DIR)) {
		fs.mkdirSync(OUTPUT_DIR);
	}

	fs.writeFileSync(path.resolve(OUTPUT_DIR, "scraper-results.json"), JSON.stringify(result, undefined, 2));
})();

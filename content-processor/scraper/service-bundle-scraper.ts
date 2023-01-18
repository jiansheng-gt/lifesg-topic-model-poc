import { ArticleSummaryApiDomain } from "mol-lib-api-contract/content/mobile-content";
import * as path from "path";
import "reflect-metadata";
import { getArticlesAndSchemes, getServiceBundles, getServicesForBundle } from "./api";
import { CachedScraper } from "./CachedScraper";
import { webScraper } from "./web-scraper";

const CACHE_DIR = path.resolve(__dirname, "../data/cache/service-bundle");

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

export const ServiceBundleScraper = async () => {
	const cachedScraper = new CachedScraper<SentenceTransformerInput>(CACHE_DIR);
	const scrapedIds = cachedScraper.getScrapedIds();

	const serviceBundles = await getServiceBundles();

	const webScraperInput = await Promise.all(
		serviceBundles.map<Promise<WebScraperInput>>(async ({ id, title, summary, serviceBundleUrl, topics, audiences }) => {
			// add title, summary to text
			const initialTexts = [title, summary]
				.filter((val) => val.length > 0)
				.join(" ").trim();

			if (serviceBundleUrl) {
				return {
					contentType: "service_bundles",
					itemId: id,
					title,
					urls: [serviceBundleUrl],
					text: initialTexts,
					scrapeExternalLinks: true,
				};
			}

			// get data of services within bundle
			const services = await getServicesForBundle(id);

			const textsArr: string[] = [initialTexts];

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

	for await (const [
		index,
		{ contentType, itemId, title, text, urls, scrapeExternalLinks },
	] of webScraperInput.entries()) {
		console.log(`[${index + 1}/${webScraperInput.length}] Crawling data for "${title}" (itemId: ${itemId})...`);

		if (scrapedIds.includes(itemId)) {
			console.log("Already crawled, skipping")
			continue;
		}

		// all urls in one item
		const data: string[] = [];
		for await (const url of urls) {
			const scraped = await webScraper.scrape(url, scrapeExternalLinks);
			data.push(scraped);
		}

		const result: SentenceTransformerInput = {
			contentType,
			itemId,
			text: text + " " + data.join(" "),
			title,
		};

		cachedScraper.saveToCache(result, itemId, `${index + 1}-${itemId}`);
		console.log(`Finished crawling "${title}"!\n\n`);
	}
	await webScraper.close();

	const result = cachedScraper.getCache();

	return result;
};

import * as fs from "fs";
import { EServiceApiDomain } from "mol-lib-api-contract/content/mobile-content";
import * as path from "path";
import "reflect-metadata";
import { getEServiceGroupDetail, getEServiceGroups, getServicesForBundle } from "./api";
import { webScraper } from "./web-scraper";

const OUTPUT_DIR = path.resolve(__dirname, "../data");

interface SentenceTransformerInput {
	contentType: "eservices";
	itemId: string;
	title: string;
	text: string;
}

interface WebScraperInput extends SentenceTransformerInput {
	urls: string[];
	scrapeExternalLinks: boolean;
}

(async () => {
	const { eserviceGroups } = await getEServiceGroups();

	const eServices: EServiceApiDomain[] = [];
	for (const group of eserviceGroups) {
		const service = await getEServiceGroupDetail(group.id);
		for (const subGroup of service.eserviceGroup.subGroups) {
			eServices.push(...subGroup.services);
		}
	}

	const webScraperInput = await Promise.all(
		eServices.map<Promise<WebScraperInput>>(async ({ id, title, action, subtitle, summary }) => {
			if (action.payload.url && action.payload.url !== "appNavigation") {
				return {
					contentType: "eservices",
					itemId: id,
					title,
					urls: [action.payload.url],
					text: "",
					scrapeExternalLinks: true,
				};
			}

			const textsArr: string[] = [];

			// add title, subtitle, summary to text
			textsArr.push(title, subtitle, summary);

			return {
				contentType: "eservices",
				itemId: id,
				title,
				urls: [],
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

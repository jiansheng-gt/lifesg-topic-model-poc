import { EServiceApiDomain } from "mol-lib-api-contract/content/mobile-content";
import "reflect-metadata";
import { getEServiceGroupDetail, getEServiceGroups } from "./api";
import { webScraper } from "./web-scraper";

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

export const EservicesScraper = async () => {
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
			// add title, subtitle, summary to text
			const initialTexts = [title, subtitle, summary]
				.filter((val) => val.length > 0)
				.join(" ").trim();

			const baseInput = {
				contentType: "eservices" as const,
				itemId: id,
				title,
				text: initialTexts,
			}

			if (action.payload.url && action.payload.url !== "appNavigation") {
				return {
					...baseInput,
					urls: [action.payload.url],
					scrapeExternalLinks: true,
				};
			}

			return {
				...baseInput,
				urls: [],
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

	return result;
};

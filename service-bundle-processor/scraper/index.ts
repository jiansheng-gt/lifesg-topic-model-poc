import { ArticleSummaryApiDomain } from "mol-lib-api-contract/content/mobile-content";
import "reflect-metadata";
import { getArticlesAndSchemes, getServiceBundles, getServicesForBundle } from "./api";

interface WebScraperInput {
	contentType: "service_bundles";
	itemId: string;
	title: string;
	urls: string[];

	/**
	 * existing text from title/summary etc
	 */
	text: string;

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

			const textsArr = [];

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

	console.log(">>>", webScraperInput);
})();

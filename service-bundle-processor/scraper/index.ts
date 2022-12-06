import "reflect-metadata";
import { RequestEndpoint } from "mol-lib-common";
import { plainToInstance } from "class-transformer";
import {
	ArticleSummaryApiDomain,
	GetBundledArticlesAndSchemes,
	GetServiceBundleResponseBodyApiDomain,
	getServiceBundlesServiceApi,
	GetServicesForBundleWithOptionsResponseBodyApiDomain,
	getServicesForBundleWithOptionsServiceApi,
} from "mol-lib-api-contract/content/mobile-content";
import { Language } from "mol-lib-api-contract";

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

const run = async () => {
	const { body } = await new RequestEndpoint()
		.setBaseUrl("https://www.dev.lifesg.io")
		.setOptions({
			json: true,
		})
		.get(getServiceBundlesServiceApi.path);
	const serviceBundles = plainToInstance(GetServiceBundleResponseBodyApiDomain, body).data;

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
			const servicesResponse = await new RequestEndpoint()
				.setBaseUrl("https://www.dev.lifesg.io")
				.setOptions({
					json: true,
				})
				.get(getServicesForBundleWithOptionsServiceApi.path, {
					params: {
						serviceBundleId: id,
						type: "all",
					},
				});
			const services = plainToInstance(
				GetServicesForBundleWithOptionsResponseBodyApiDomain,
				servicesResponse.body.data,
			);

			const textsArr = [];

			// add title, subtitle, summary to text
			services.featuredServices.forEach(({ title, subtitle, summary }) => {
				textsArr.push(title, subtitle, summary);
			});

			services.services.forEach(({ title, subtitle, summary }) => {
				textsArr.push(title, subtitle, summary);
			});

			// get related articles/schemes
			const articlesAndSchemesResponse = await new RequestEndpoint()
				.setBaseUrl("https://www.dev.lifesg.io")
				.setOptions({
					json: true,
				})
				.post("/content/api/v1/queryBundledArticlesAndSchemes", {
					body: GetBundledArticlesAndSchemes.Transformers.transformGetBundledArticlesAndSchemesRequestApiDtoToDomain(
						{
							language: Language.MOLLanguage.ENGLISH,
							topics,
							targetAudiences: audiences,
							limit: 5,
						},
					),
				});

			const articlesAndSchemes =
				GetBundledArticlesAndSchemes.Transformers.transformGetBundledArticlesAndSchemesResponseApiDtoToDomain(
					articlesAndSchemesResponse.body,
				);

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
};

run();

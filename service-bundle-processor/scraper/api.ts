import { plainToInstance } from "class-transformer";
import { TargetAudience, Topic } from "lib-content-taxanomy";
import { Language } from "mol-lib-api-contract";
import {
	GetBundledArticlesAndSchemes,
	GetServiceBundleResponseBodyApiDomain,
	getServiceBundlesServiceApi,
	GetServicesForBundleWithOptionsResponseBodyApiDomain,
	getServicesForBundleWithOptionsServiceApi,
} from "mol-lib-api-contract/content/mobile-content";
import { RequestEndpoint } from "mol-lib-common";

const LIFESG_BASE_URL = "https://www.dev.lifesg.io";

const createClient = () => new RequestEndpoint().setBaseUrl(LIFESG_BASE_URL);

export const getServiceBundles = async () => {
	const { body } = await createClient()
		.setOptions({
			json: true,
		})
		.get(getServiceBundlesServiceApi.path);

	return plainToInstance(GetServiceBundleResponseBodyApiDomain, body).data;
};

export const getServicesForBundle = async (serviceBundleId: string) => {
	const { body } = await createClient()
		.setOptions({
			json: true,
		})
		.get(getServicesForBundleWithOptionsServiceApi.path, {
			params: {
				serviceBundleId,
				type: "all",
			},
		});
	return plainToInstance(GetServicesForBundleWithOptionsResponseBodyApiDomain, body.data);
};

export const getArticlesAndSchemes = async (topics: Topic[], targetAudiences: TargetAudience[]) => {
	const { body } = await createClient()
		.setOptions({
			json: true,
		})
		.post("/content/api/v1/queryBundledArticlesAndSchemes", {
			body: GetBundledArticlesAndSchemes.Transformers.transformGetBundledArticlesAndSchemesRequestApiDtoToDomain({
				language: Language.MOLLanguage.ENGLISH,
				topics,
				targetAudiences,
				limit: 5,
			}),
		});

	return GetBundledArticlesAndSchemes.Transformers.transformGetBundledArticlesAndSchemesResponseApiDtoToDomain(body);
};

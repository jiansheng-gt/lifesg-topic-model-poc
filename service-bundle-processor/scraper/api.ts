import axios from "axios";
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
import { GetEServiceGroupDetailResponseDataApiDomain } from "mol-lib-api-contract/content/mobile-content/get-eservice-detail/get-eservice-group-detail-api-domain";
import { GetEServiceGroupResponseDataApiDomain } from "mol-lib-api-contract/content/mobile-content/get-eservice-summaries/get-eservice-summaries-api-domain";
import { appConfig } from "./config/app-config";

const createClient = () =>
	axios.create({
		baseURL: appConfig.baseUrl,
	});

export const getServiceBundles = async () => {
	const { data } = await createClient().get(getServiceBundlesServiceApi.path);
	return plainToInstance(GetServiceBundleResponseBodyApiDomain, data).data;
};

export const getServicesForBundle = async (serviceBundleId: string) => {
	const { data } = await createClient().get(getServicesForBundleWithOptionsServiceApi.path, {
		params: {
			serviceBundleId,
			type: "all",
		},
	});
	return plainToInstance(GetServicesForBundleWithOptionsResponseBodyApiDomain, data.data);
};

export const getEServiceGroups = async () => {
	const { data } = await createClient().get("/content/api/v2/queryEServiceGroups");
	return plainToInstance(GetEServiceGroupResponseDataApiDomain, data.data);
};

export const getEServiceGroupDetail = async (groupId: string) => {
	const { data } = await createClient().get(`/content/api/v2/queryEServiceGroupDetail/${groupId}`);
	return plainToInstance(GetEServiceGroupDetailResponseDataApiDomain, data.data);
};

export const getArticlesAndSchemes = async (topics: Topic[], targetAudiences: TargetAudience[]) => {
	const { data } = await createClient().post(
		"/content/api/v1/queryBundledArticlesAndSchemes",
		GetBundledArticlesAndSchemes.Transformers.transformGetBundledArticlesAndSchemesRequestApiDomainToDto({
			language: Language.MOLLanguage.ENGLISH,
			topics,
			targetAudiences,
			limit: 5,
		}),
	);

	return GetBundledArticlesAndSchemes.Transformers.transformGetBundledArticlesAndSchemesResponseApiDtoToDomain(data);
};

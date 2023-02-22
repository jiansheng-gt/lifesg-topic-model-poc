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

export class Api {
	constructor(private readonly baseUrl = appConfig.baseUrl) {

	}

	private createClient = () =>
		axios.create({
			baseURL: this.baseUrl,
		});

	public getServiceBundles = async () => {
		const { data } = await this.createClient().get(getServiceBundlesServiceApi.path);
		return plainToInstance(GetServiceBundleResponseBodyApiDomain, data).data;
	};

	public getServicesForBundle = async (serviceBundleId: string) => {
		const { data } = await this.createClient().get(getServicesForBundleWithOptionsServiceApi.path, {
			params: {
				serviceBundleId,
				type: "all",
			},
		});
		return plainToInstance(GetServicesForBundleWithOptionsResponseBodyApiDomain, data.data);
	};

	public getEServiceGroups = async () => {
		const { data } = await this.createClient().get("/content/api/v2/queryEServiceGroups");
		return plainToInstance(GetEServiceGroupResponseDataApiDomain, data.data);
	};

	public getEServiceGroupDetail = async (groupId: string) => {
		const { data } = await this.createClient().get(`/content/api/v2/queryEServiceGroupDetail/${groupId}`);
		return plainToInstance(GetEServiceGroupDetailResponseDataApiDomain, data.data);
	};

	public getArticlesAndSchemes = async (topics: Topic[], targetAudiences: TargetAudience[]) => {
		const { data } = await this.createClient().post(
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

}

export const api = new Api();

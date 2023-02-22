import * as fs from "fs";
import * as path from "path";

import { EServiceApiDomain } from "mol-lib-api-contract/content/mobile-content";
import { Api } from "./api";

const OUTPUT_DIR = path.resolve(__dirname, "../scraper-per-env");

enum ENV {
	DEV = "DEV",
	TST = "TST",
	STG = "STG",
	PRD = "PRD",
}

const apis: [ENV, Api][] = [
	[ENV.DEV, new Api("https://www.dev.lifesg.io")],
	[ENV.TST, new Api("https://www.tst.lifesg.io")],
	[ENV.STG, new Api("https://www.stg.lifesg.io")],
	[ENV.PRD, new Api("https://www.life.gov.sg")],
];

interface EnvData {
	contentType: "service_bundles" | "eservices";
	itemId: string;
	contentId: string;
}

const envUuidMap: Record<ENV, EnvData[]> = {
	[ENV.DEV]: [],
	[ENV.TST]: [],
	[ENV.STG]: [],
	[ENV.PRD]: [],
};
(async () => {
	if (!fs.existsSync(OUTPUT_DIR)) {
		fs.mkdirSync(OUTPUT_DIR);
	}

	for (const [currEnv, api] of apis) {
		const currEnvData: EnvData[] = [];

		//ESERVICES
		const { eserviceGroups } = await api.getEServiceGroups();

		const eServices: EServiceApiDomain[] = [];
		for (const group of eserviceGroups) {
			const service = await api.getEServiceGroupDetail(group.id);
			for (const subGroup of service.eserviceGroup.subGroups) {
				eServices.push(...subGroup.services);
			}
		}

		eServices.forEach(({ id, contentId }) => {
			currEnvData.push({
				contentType: "eservices",
				itemId: id,
				contentId,
			});
		});

		// SERVICE BUNDLES

		const serviceBundles = await api.getServiceBundles();

		serviceBundles.forEach(({ id, contentId }) => {
			currEnvData.push({
				contentType: "service_bundles",
				itemId: id,
				contentId,
			});
		});

		envUuidMap[currEnv] = currEnvData;
	}

	interface Embeddings {
		contentType: "service_bundles" | "eservices";
		itemId: string;
		title: string;
		embedding: number[];
	}

	const embeddingsStr = fs.readFileSync(path.resolve(__dirname, "../data/embeddings.json")).toString("utf8");
	const embeddingsPrd = JSON.parse(embeddingsStr) as Embeddings[];

	Object.values(ENV).forEach((env) => {
		const res = embeddingsPrd.map((emb) => {
			const prodDetails = envUuidMap[ENV.PRD].find(({ itemId }) => itemId === emb.itemId);

			return {
				...emb,
				itemId: envUuidMap[env].find(
					({ contentType, contentId }) =>
						contentId === prodDetails.contentId && contentType === prodDetails.contentType,
				).itemId,
			};
		});

		fs.writeFileSync(
			path.resolve(OUTPUT_DIR, `embeddings.${env.toLowerCase()}.json`),
			JSON.stringify(res, undefined, 2),
		);
	});
})();

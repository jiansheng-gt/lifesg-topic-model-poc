import * as fs from "fs";
import * as path from "path";
import { EservicesScraper } from "./eservices-scraper";
import { ServiceBundleScraper } from "./service-bundle-scraper";

const OUTPUT_DIR = path.resolve(__dirname, "../data");

(async () => {
	const eservices = await EservicesScraper();
	const serviceBundles = await ServiceBundleScraper();

	if (!fs.existsSync(OUTPUT_DIR)) {
		fs.mkdirSync(OUTPUT_DIR);
	}

	fs.writeFileSync(
		path.resolve(OUTPUT_DIR, "scraper-results.json"),
		JSON.stringify([...eservices, ...serviceBundles], undefined, 2),
	);
})();

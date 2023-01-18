import * as fs from "fs";
import * as path from "path";

export class CachedScraper<Cache extends object> {
	private readonly scrapedIdsPath: string;

	constructor(
		private readonly cacheDir: string,
		private readonly scrapedIdsFile = "scraped-ids.txt",
	) {
		this.scrapedIdsPath = path.resolve(cacheDir, scrapedIdsFile);

		if (!fs.existsSync(this.cacheDir)) {
			fs.mkdirSync(this.cacheDir, { recursive: true });
		}

		if (!fs.existsSync(this.scrapedIdsPath)) {
			fs.closeSync(fs.openSync(this.scrapedIdsPath, 'w'));
		}
	}

	public getScrapedIds() {
		return fs.readFileSync(this.scrapedIdsPath).toString("utf8").split("\n");
	}

	public saveToCache(data: Cache, id: string, title: string) {
		fs.appendFileSync(this.scrapedIdsPath, id + "\n");
		fs.writeFileSync(path.resolve(this.cacheDir, title), JSON.stringify(data));
	}

	public getCache() {
		return fs.readdirSync(this.cacheDir)
			.filter((fileName) => fileName !== this.scrapedIdsFile)
			.map((fileName) => {
				const cacheStr = fs.readFileSync(path.resolve(this.cacheDir, fileName)).toString("utf8");
				return JSON.parse(cacheStr) as Cache;
			});
	}
}

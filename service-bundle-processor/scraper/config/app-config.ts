import { ConfigUtils } from "mol-lib-common/utils/config/ConfigUtils";

const {
	getValueFromEnv,
} = ConfigUtils;
require("dotenv").config();

export const appConfig = {
	baseUrl: getValueFromEnv("LIFESG_BASE_URL")
};

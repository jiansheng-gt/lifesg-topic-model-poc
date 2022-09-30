import { getClicksSummary } from "./util/clicks";

export const getRecs = async (numClicks = 0) => {
  return fetch("/api/guide-recs", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(getClicksSummary(numClicks)),
  }).then((res) => res.json());
};

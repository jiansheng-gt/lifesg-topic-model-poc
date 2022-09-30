import { getClicksSummary } from "./util/clicks";

export const getRecs = async () => {
  return fetch("/api/guide-recs", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(getClicksSummary()),
  }).then((res) => res.json());
};

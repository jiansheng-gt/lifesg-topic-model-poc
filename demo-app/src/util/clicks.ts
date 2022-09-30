import { storage } from "./storage";

export const getClicksSummary = (numClicks = 0) => {
  const clicks = storage.getClicks().slice(-numClicks);

  const summary = clicks.reduce((acc, id) => {
    const idCount = (acc[id] || 0) + 1;
    return {
      ...acc,
      [id]: idCount,
    };
  }, {} as Record<string, number>);

  console.log("clicks", summary);
  return summary;
};

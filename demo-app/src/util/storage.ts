const getClicks = (): number[] =>
  JSON.parse(sessionStorage.getItem("clicks") || "[]");

const addClick = (id: number) => {
  // get links clicked from session
  const clicks = getClicks();
  clicks.push(id);

  sessionStorage.setItem("clicks", JSON.stringify(clicks));
};

const clearClicks = () => {
  sessionStorage.clear();
};

export const storage = {
  getClicks,
  addClick,
  clearClicks,
};

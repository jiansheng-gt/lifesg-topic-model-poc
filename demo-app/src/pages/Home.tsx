import { useState, useEffect } from "react";
import { LinkContainer, Page } from "src/app.styles";
import { Card } from "src/components/Card";
import { withBasePage } from "src/hoc/withBasePage";
import { RecData } from "src/types";

const getClicks = () => JSON.parse(sessionStorage.getItem("clicks") || "{}");

const HomeComponent = () => {
  const [data, setData] = useState<RecData[] | null>(null);

  const fetchData = () => {
    fetch("/api/guide-recs", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(getClicks()),
    })
      .then((res) => res.json())
      .then((data) => setData(data));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onClickLink = (id: number) => {
    // get links clicked from session
    const clicks = getClicks();

    console.log("link", clicks[id], id);

    if (clicks[id]) {
      clicks[id] = clicks[id] + 1;
    } else {
      clicks[id] = 1;
    }

    console.log(clicks);
    // set clicks in session
    sessionStorage.setItem("clicks", JSON.stringify(clicks));
    fetchData();
  };

  const renderLinks = (read: boolean) => {
    if (!data) return null;

    const clicks = getClicks();
    let filteredData = data.filter(({ id }) => !!clicks[id] === read);

    return (
      <LinkContainer>
        {filteredData.map(({ id, title, url, sim }) => (
          <Card
            key={id}
            title={title}
            onClick={() => onClickLink(id)}
            {...(!read && {
              subtext: `Similarity: ${(sim * 100).toFixed(2) + "%"}`,
            })}
          />
        ))}
      </LinkContainer>
    );
  };
  return (
    <div className="App">
      <Page className="App-header">
        <h3>Read articles</h3>
        {renderLinks(true)}
        <h3>Suggested articles</h3>
        {renderLinks(false)}
      </Page>
    </div>
  );
};

export const Home = withBasePage(HomeComponent);

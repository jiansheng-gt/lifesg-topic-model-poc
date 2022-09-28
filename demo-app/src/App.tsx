import { useEffect, useState } from "react";
import { LinkContainer, Page } from "./app.styles";
import { Card } from "./components/Card";

interface RecData {
  id: number;
  sim: number;
  title: string;
  url: string;
}

const getClicks = () => JSON.parse(sessionStorage.getItem("clicks") || "{}")

const App = () => {
  const [data, setData] = useState<RecData[] | null>(null);

  const fetchData = () => {
    fetch("/api/guide-recs", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(getClicks())
    }).then((res) => res.json())
      .then(data => setData(data))
  }

  useEffect(() => {
    fetchData();
  }, [])

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
    fetchData()
  };

  const renderLinks = () => {
    if (!data) return null;

    return (
      <LinkContainer>
        {data.map(({ id, title, url, sim }) => (
          <Card
            key={id}
            title={title}
            onClick={() => onClickLink(id)}
            subtext={`Similarity: ${(sim * 100).toFixed(2) + '%'}`}
          />
        ))}
      </LinkContainer>
    );
  };
  return (
    <div className="App">
      <Page className="App-header">{renderLinks()}</Page>
    </div>
  );
};

export default App;

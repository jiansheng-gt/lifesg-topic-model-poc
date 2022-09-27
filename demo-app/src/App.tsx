import { useEffect, useState } from "react";
import { Link, LinkContainer } from "./app.styles";

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
    fetch("http://127.0.0.1:5000/guide-recs", {
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
          <Link onClick={() => onClickLink(id)} key={id}>
            {title}
            <br />
            <br />
            Similarity: {sim}
          </Link>
        ))}
      </LinkContainer>
    );
  };
  return (
    <div className="App">
      <header className="App-header">{renderLinks()}</header>
    </div>
  );
};

export default App;

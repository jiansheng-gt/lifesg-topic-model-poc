import { useState, useEffect } from "react";
import { getRecs } from "src/api";
import { LinkContainer, Page } from "src/app.styles";
import { Card } from "src/components/Card";
import { withBasePage } from "src/hoc/withBasePage";
import { RecData } from "src/types";
import { getClicksSummary } from "src/util/clicks";
import { storage } from "src/util/storage";

const HomeComponent = () => {
  const [data, setData] = useState<RecData[] | null>(null);

  const fetchData = () => {
    getRecs().then((data) => setData(data));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onClickLink = (id: number) => {
    storage.addClick(id);
    fetchData();
  };

  const renderLinks = (read: boolean) => {
    if (!data) return null;

    const clicks = getClicksSummary();
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

import { Link, LinkContainer } from "./app.styles";

const App = () => {
  const links = ["baby", "newborn", "nanny", "car", "petrol", "speed", "elderly", "disease", "caregiver"];

  const onClickLink = (link: string) => {
    // get links clicked from session
    const clicks = JSON.parse(sessionStorage.getItem("clicks") || "{}");

    console.log("link", clicks[link], link);

    if (clicks[link]) {
      clicks[link] = clicks[link] + 1;
    } else {
      clicks[link] = 1;
    }

    console.log(clicks);
    // set clicks in session
    sessionStorage.setItem("clicks", JSON.stringify(clicks));
  };

  const renderLinks = () => {
    return (
      <LinkContainer>
        {links.map((link) => (
          <Link onClick={() => onClickLink(link)} key={link}>
            {link}
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

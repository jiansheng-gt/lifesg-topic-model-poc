import {
  NavBar,
  NavBarItem,
  NavBarItemRight,
  NavBarLink,
} from "./basePage.styles";
import { storage } from "../util/storage";

interface Props {
  children: JSX.Element;
}

export const BasePage = ({ children }: Props) => {
  return (
    <>
      <nav>
        <NavBar>
          <NavBarItem>
            <NavBarLink to="/">Home</NavBarLink>
          </NavBarItem>
          <NavBarItem>
            <NavBarLink to="/top-5">Top 5</NavBarLink>
          </NavBarItem>
          <NavBarItemRight>
            <NavBarLink onClick={storage.clearClicks} to="#">
              CLEAR STORE
            </NavBarLink>
          </NavBarItemRight>
        </NavBar>
      </nav>
      {children}
    </>
  );
};

import { NavBar, NavBarItem, NavBarLink } from "./basePage.styles";

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
        </NavBar>
      </nav>
      {children}
    </>
  );
};

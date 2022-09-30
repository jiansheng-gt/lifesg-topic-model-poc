import React from "react";
import {
  NavBar,
  NavBarItem,
  NavBarItemRight,
  NavBarLink,
} from "./basePage.styles";
import { storage } from "../util/storage";
import { useNavigate } from "react-router-dom";

interface Props {
  children: JSX.Element;
}

export const BasePage = ({ children }: Props) => {
  const navigate = useNavigate();
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
          <NavBarItem>
            <NavBarLink to="/temporal">Temporal</NavBarLink>
          </NavBarItem>
          <NavBarItemRight>
            <NavBarLink
              onClick={() => {
                storage.clearClicks();
                navigate(0);
              }}
              to="#"
            >
              CLEAR STORE
            </NavBarLink>
          </NavBarItemRight>
        </NavBar>
      </nav>
      {children}
    </>
  );
};

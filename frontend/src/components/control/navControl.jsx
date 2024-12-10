import React from "react";
import classes from "./navControl.module.css";
import { NavLink } from "react-router-dom";

export const Nav = ({ links }) => {
  return (
    <div className={classes.nav_container}>
      <nav className={classes.nav_control}>
        <ul className={classes.ul_control}>
          {links.map((link, index) => (
            <li key={index} className={classes.li_control}>
              <NavLink
                to={link.href}
                className={({ isActive }) =>
                  `${classes.link} ${isActive ? classes.active : ""}`
                }
              >
                {link.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

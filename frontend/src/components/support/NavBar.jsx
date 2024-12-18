import React from "react";
import { NavLink } from "react-router-dom";
import classes from "./NavBar.module.css";

export const NavBar = () => {
  return (
    <nav className={classes.navbar}>
      <NavLink
        to="/site-navigation"
        className={({ isActive }) =>
          `${classes.link} ${isActive ? classes.active : ""}`
        }
      >
        Навигация сайта
      </NavLink>
      <NavLink
        to="/available-functions"
        className={({ isActive }) =>
          `${classes.link} ${isActive ? classes.active : ""}`
        }
      >
        Доступные функции
      </NavLink>
      <NavLink
        to="/feedback"
        className={({ isActive }) =>
          `${classes.link} ${isActive ? classes.active : ""}`
        }
      >
        Обратная связь
      </NavLink>
    </nav>
  );
};

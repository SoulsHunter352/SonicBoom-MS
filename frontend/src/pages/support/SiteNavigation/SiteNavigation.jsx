import React from "react";
import { NavBar } from "../../../components/support/NavBar";
import track_pic from "../../../assets/images/NavigationUser.png";
import classes from "./SiteNavigation.module.css";

export default function SiteNavigationPage() {
  return (
    <div>
      <NavBar />
      <div>
        <img src={track_pic} />
        <h1>Навигация сайта</h1>
      </div>
    </div>
  );
}

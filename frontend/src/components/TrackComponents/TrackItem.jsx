import React from "react";
import classes from "./TrackItem.module.css";

export default function TrackItem({ title, icon }) {
  return (
    <div className={classes.trackItem}>
      <div className={classes.trackInfo}>
        <img src={icon} alt="Track" className={classes.trackIcon} />
        <p className={classes.trackTitle}>{title}</p>
      </div>
      <div className={classes.trackActions}>
        <button className={classes.playButton}>
          <i className="fas fa-play"></i> {/* Или используйте SVG иконку */}
        </button>
        <button className={classes.menuButton}>
          <i className="fas fa-ellipsis-v"></i> {/* Меню действий */}
        </button>
      </div>
    </div>
  );
}

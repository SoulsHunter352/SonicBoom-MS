import React, { useState } from "react";
import classes from "./TrackCover.module.css";
export default function TrackCover({
  trackTitle,
  trackCover,
  trackBackground,
}) {
  return (
    <div
      className={classes["track-header"]}
      style={{
        display: "flex", // Исправлено значение
        flexDirection: "column", // Добавлено направление колонки
        justifyContent: "center",
        alignItems: "center", // Центрирование содержимого по горизонтали
        backgroundImage: `url(${trackBackground})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        textAlign: "center",
        marginBottom: "20px",
        padding: "40px",
        borderRadius: "10px",
      }}
    >
      <img
        src={trackCover}
        alt="Track Cover"
        className={classes["track-image"]}
      />
      <h1 className={classes["track-title"]}>{trackTitle}</h1>
    </div>
  );
}

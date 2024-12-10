import React, { useState } from "react";
import classes from "./AlbumBlock.module.css";
export default function AlbumsBlock({ albums }) {
  return (
    <div className={classes["album-grid"]}>
      {albums.map((album) => (
        <div key={album.id} className={classes["album-card"]}>
          <img
            src={album.cover}
            alt={album.title}
            className={classes["album-cover"]}
          />
          <h3 className={classes["album-title"]}>{album.title}</h3>
        </div>
      ))}
    </div>
  );
}

import React from "react";
import { Nav } from "../../components/control/navControl";
import { Outlet } from "react-router-dom";
import classes from "./Control.module.css";
import track_pic from "../../assets/images/track_pic.png";
import user_pic from "../../assets/images/user.jpg";
import album_pic from "../../assets/images/album.png";
import performer_pic from "../../assets/images/performer.jpg";


const navLinks = [
  { id: 1, name: "Пользователи", href: "users" },
  { id: 2, name: "Альбомы", href: "albums" },
  { id: 3, name: "Исполнители", href: "performers" },
  { id: 4, name: "Треки", href: "tracks" },
];

// Данные для каждой страницы
const data = {
  users: [
    { id: 1, name: "Alice", icon: user_pic },
    { id: 2, name: "Bob", icon: user_pic },
    { id: 3, name: "Vladlen", icon: user_pic },
    { id: 4, name: "Charlie", icon: user_pic },
    { id: 5, name: "Carl", icon: user_pic },
    { id: 6, name: "John", icon: user_pic },
    { id: 7, name: "Vlad", icon: user_pic },
    { id: 8, name: "Mattew", icon: user_pic },
    { id: 9, name: "Denis", icon: user_pic },
    { id: 10, name: "Clare", icon: user_pic },
    { id: 11, name: "Kate", icon: user_pic },
  ],
  albums: [
    { id: 1, name: "Album 1", icon: album_pic },
    { id: 2, name: "Album 2", icon: album_pic },
    { id: 3, name: "Album 3", icon: album_pic },
  ],
  performers: [
    { id: 1, name: "Performer A", icon: performer_pic },
    { id: 2, name: "Performer B", icon: performer_pic },
    { id: 3, name: "Performer C", icon: performer_pic },
  ],
  tracks: [
    { id: 1, name: "Track X", icon: track_pic },
    { id: 2, name: "Track Y", icon: track_pic },
    { id: 99, name: "Track Z", icon: track_pic },
  ],
};

export default function Control() {
  return (
    <div className={classes.container}>
      <Nav links={navLinks} />
      {/* Передаем данные через Outlet */}
      <Outlet context={{ data }} />
    </div>
  );
}

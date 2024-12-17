import "./styles.css";
import Header from "./components/Header/Header";
import Player from "./components/Player/Player";
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Feedback from "./pages/support/Feedback/Feedback";
import AvailableFunctions from "./pages/support/AvailableFunctions/AvailableFunctions";
import SiteNavigation from "./pages/support/SiteNavigation/SiteNavigation";

import TrackView from "./pages/Tracks/TrackView";
import TrackAdd from "./pages/Tracks/TrackAdd";

import AlbumView from "./pages/Albums/AlbumView";

import GenreAdd from "./pages/Genres/GenreAdd";

import Home from "./pages/Home/Home";

import Login from "./pages/users/Login/Login";
import Registration from "./pages/users/Registration/Registration";

import Profile from "./pages/users/Profile/Profile";
import EditProfile from "./pages/users/EditProfile/EditProfile";
import ChangePassword from "./pages/users/ChangePassword/ChangePassword";

import Control from "./pages/control/control";
import UsersControl from "./pages/control/UsersControl";
import AlbumsControl from "./pages/control/AlbumsControl";
import PerformersControl from "./pages/control/PerformersControl";
import TracksControl from "./pages/control/TracksControl";

import { EditPage } from "./pages/control/EditPage/EditPage";
import EditUserPage from "./pages/control/EditPage/EditUserPage";
import EditAlbumPage from "./pages/control/EditPage/EditAlbumPage";
import EditPerformerPage from "./pages/control/EditPage/EditPerformPage";
import EditTrackPage from "./pages/control/EditPage/EditTrackPage";

import ArtistAdd from "./pages/Artists/ArtistAdd/ArtistAdd";
import ArtistEdit from "./pages/Artists/ArtistEdit/ArtistEdit";

export default function App() {
  const [user, setUser] = useState({ nickname: "ABOBA", type: "admin" });

  const [playerSong, setPlayerSong] = useState({
    isMuted: false,
    isPlaying: false,
    isRepeated: false,
    volume: 100,
    currentTime: 0,
    name: "Юморист",
    artist: "FACE",
    file: "https://sonic-boom.ru/sb-test/test.mp3",
    cover: "https://sonic-boom.ru/sb-test/cover-test.jpg",
  });

  const updatePlayerSong = (obj) => {
    setPlayerSong((s) => Object.assign({}, s, obj));
  };

  const onSongEnd = () => {
    updatePlayerSong({
      name: "Mice on Venus",
      artist: "C418",
      file: "https://sonic-boom.ru/sb-test/c418.mp3",
      cover: "https://sonic-boom.ru/sb-test/c418.jpg",
    });
  };

  return (
    <Router>
      <div className="wrapper">
        <Header user={user} />

        <div className="page">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="feedback" element={<Feedback />} />
            <Route
              path="available-functions"
              element={<AvailableFunctions />}
            />
            <Route path="site-navigation" element={<SiteNavigation />} />
            <Route path="login" element={<Login />} />
            <Route path="registration" element={<Registration />} />

            <Route path="profile" element={<Profile />}></Route>
            <Route path="edit-profile" element={<EditProfile />}></Route>
            <Route path="change-password" element={<ChangePassword />} />

            <Route path="track" element={<TrackView user={user} />} />
            <Route path="track-add" element={<TrackAdd />}></Route>

            <Route path="artist-add" element={<ArtistAdd />}></Route>
            <Route path="artist-edit" element={<ArtistEdit />}></Route>

            <Route path="genre-add" element={<GenreAdd />}></Route>

            <Route path="album" element={<AlbumView user={user} />} />

            <Route path="control" element={<Control />}>
              <Route path="users" element={<UsersControl />} />
              <Route path="albums" element={<AlbumsControl />} />
              <Route path="performers" element={<PerformersControl />} />
              <Route path="tracks" element={<TracksControl />} />
              <Route path=":page/edit/:id" element={<EditPage />} />
            </Route>
          </Routes>
        </div>

        <Player
          song={playerSong}
          updateSong={updatePlayerSong}
          onSongEnd={onSongEnd}
        />
      </div>
    </Router>
  );
}

import { useState } from "react"; // Используем модули CSS для стилей
import track_pic from "../../assets/images/track_pic.png";
import track_bg from "../../assets/images/track_bg.png";
import plus_circle from "../../assets/images/Plus_circle.png";
import TrackCover from "../../components/TrackComponents/TrackCover";
import ControlPanel from "../../components/ControlPanel/ContolPanel";
import ContentBlock from "../../components/TrackComponents/ContentBlock";
import AlbumBlock from "../../components/TrackComponents/AlbumBlock";
import album_cov1 from "../../assets/images/album_cov1.png";
import album_cov2 from "../../assets/images/album_cov2.png";

export default function TrackView({ user }) {
  const [activeTab, setActiveTab] = useState("Текст");
  const buttonLabels = ["Текст", "Описание", "Альбомы"];

  const albumsData = [
    {
      id: 1,
      title: "Альбом 1",
      cover: album_cov1, // Замените на реальный путь
    },
    {
      id: 2,
      title: "Альбом 2",
      cover: album_cov2,
    },
    {
      id: 3,
      title: "Альбом 3",
      cover: album_cov1,
    },
    {
      id: 4,
      title: "Альбом 4",
      cover: album_cov1,
    },
    {
      id: 5,
      title: "Альбом 5",
      cover: album_cov2,
    },
    {
      id: 6,
      title: "Альбом 6",
      cover: album_cov1,
    },
  ];
  const redirect_path = "/track-add";
  const textContent =
    "Текст трека Текст трека Текст трека Текст трека Текст трека Текст трека Текст трека";
  const descriptionContent = "Описание трека...";
  return (
    <div>
      <TrackCover
        trackTitle="Название трека"
        trackCover={track_pic}
        trackBackground={track_bg}
      />
      <ControlPanel
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        buttonLabels={buttonLabels}
        Icon={plus_circle}
        redirectPath={redirect_path}
        user={user}
      />
      {activeTab === "Текст" && <ContentBlock content={textContent} />}
      {activeTab === "Описание" && (
        <ContentBlock content={descriptionContent} />
      )}
      {activeTab === "Альбомы" && <AlbumBlock albums={albumsData} />}
    </div>
  );
}

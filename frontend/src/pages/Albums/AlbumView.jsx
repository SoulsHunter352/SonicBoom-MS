import { useState } from "react";
import classes from "./AlbumView.module.css";
import track_pic from "../../assets/images/track_pic.png";
import track_bg from "../../assets/images/track_bg.png";
import TrackItem from "../../components/TrackComponents/TrackItem";
import ControlPanel from "../../components/ControlPanel/ContolPanel";
import plus_circle from "../../assets/images/Plus_circle.png";

export default function AlbumView({ user }) {
  const [activeTab, setActiveTab] = useState("Треки");

  // Данные о треках
  const tracks = [
    { title: "Track 1", duration: "3:45", icon: track_pic },
    { title: "Track 2", duration: "4:15", icon: track_pic },
    { title: "Track 3", duration: "5:20", icon: track_pic },
    { title: "Track 4", duration: "2:50", icon: track_pic },
  ];

  const buttonLabels = ["Треки", "Описание", "Исполнитель"];

  // Функция для рендеринга контента на основе активной вкладки
  const renderTabContent = () => {
    switch (activeTab) {
      case "Треки":
        return (
          <div className={classes["tab-content"]}>
            {tracks.length === 0 ? (
              <p>Нет треков для отображения</p>
            ) : (
              tracks.map((track, index) => (
                <TrackItem
                  key={index}
                  icon={track.icon}
                  title={track.title}
                  duration={track.duration}
                />
              ))
            )}
          </div>
        );
      case "Описание":
        return (
          <div className={classes["tab-content"]}>
            <p>Описание альбома будет отображаться здесь.</p>
          </div>
        );
      case "Исполнитель":
        return (
          <div className={classes["tab-content"]}>
            <p>Исполнитель будет отображаться здесь.</p>
          </div>
        );
      case "+":
        return (
          <div className={classes["tab-content"]}>
            <p>Исполнитель будет отображаться здесь.</p>
          </div>
        );
    }
  };

  const trackHeaderStyle = {
    backgroundImage: `url(${track_bg})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    textAlign: "center",
    marginBottom: "20px",
    padding: "40px",
    borderRadius: "10px",
  };

  return (
    <div className={classes["app"]}>
      <main className={classes["main-content"]}>
        {/* Track Header */}
        <div className={classes["track-header"]} style={trackHeaderStyle}>
          <img
            src={track_pic}
            alt="Track Cover"
            className={classes["track-image"]}
          />
          <h1 className={classes["track-title"]}>Название альбома</h1>
        </div>

        {/* Tabs */}
        <ControlPanel
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          buttonLabels={buttonLabels}
          Icon={plus_circle}
          user={user}
        ></ControlPanel>

        {/* Tab Content */}
        {renderTabContent()}
      </main>
    </div>
  );
}

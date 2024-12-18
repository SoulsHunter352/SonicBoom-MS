import { useEffect, useState, useRef } from "react";
import classes from "./PlayerLine.module.css";

export default function PlayerLine({
  song,
  updateSong,
  audioCallback,
  onSongEnd,
  audioBuffer,
}) {
  const playerLineRef = useRef();
  const [currentTimeDynamic, setCurrentTimeDynamic] = useState(
    song.currentTime
  );
  const [playingIntervalId, setPlayingIntervalId] = useState(null);
  const [isChangeTime, setIsChangeTime] = useState(false);

  const roundCurrentTime = (seconds) => {
    return Math.round((parseFloat(seconds) + Number.EPSILON) * 1000) / 1000;
  };

  const updateCurrentTimeVisual = (seconds) => {
    const currentTime = roundCurrentTime(seconds);
    setCurrentTimeDynamic(currentTime);
    return currentTime;
  };

  const updateCurrentTime = (seconds) => {
    const currentTime = updateCurrentTimeVisual(seconds);
    audioCallback(currentTime);
    updateSong({ currentTime });
  };

  const secondsToString = (seconds) => {
    return `${parseInt(seconds / 60)
      .toString()
      .padStart(2, "0")}:${parseInt(seconds % 60)
      .toString()
      .padStart(2, "0")}`;
  };

  const clrInterval = () => {
    if (playingIntervalId) {
      clearInterval(playingIntervalId);
      setPlayingIntervalId(null);
    }
  };

  const playerLineFunc = () => {
    clrInterval();
    if (song.isPlaying) {
      const timeFunc = () => window.performance.now();
      let iterStart = timeFunc();
      let delta = 0;
      setPlayingIntervalId(
        setInterval(() => {
          delta = (timeFunc() - iterStart) / 1000;
          iterStart = timeFunc();
          if (!isChangeTime && song.duration)
            setCurrentTimeDynamic((prev) =>
              prev < song.duration ? roundCurrentTime(prev + delta) : prev
            );
        }, 50)
      );
    }
    return clrInterval;
  };

  // Новый буфер - перематываем в начало
  useEffect(() => {
    if (playerLineRef.current)
      playerLineRef.current.style.pointerEvents = audioBuffer ? "all" : "none";
    if (audioBuffer) updateCurrentTime(0);
    else updateSong({ duration: 0 });
  }, [audioBuffer]);

  useEffect(() => {
    if (!isChangeTime) updateCurrentTime(currentTimeDynamic);
    return playerLineFunc();
  }, [song.isPlaying, isChangeTime]);

  useEffect(playerLineFunc, [song.duration]);

  // Вызываем callback при конце трека
  useEffect(() => {
    if (currentTimeDynamic >= song.duration) {
      if (!song.isRepeated) onSongEnd();
      else updateCurrentTime(0);
    }
  }, [currentTimeDynamic]);

  return (
    <div className={classes["player-line-wrapper"]} ref={playerLineRef}>
      <input
        min="0"
        max={song.duration}
        step="0.001"
        className={classes["player-line"]}
        type="range"
        value={currentTimeDynamic}
        onChange={(e) => updateCurrentTimeVisual(e.target.value)}
        onMouseUp={(e) => {
          setIsChangeTime(false);
          updateCurrentTime(e.target.value);
        }}
        onMouseDown={() => setIsChangeTime(true)}
        onTouchStart={() => setIsChangeTime(true)}
        onTouchEnd={(e) => {
          setIsChangeTime(false);
          updateCurrentTime(e.target.value);
        }}
      />

      <div
        className={classes["player-line-progress"]}
        style={{ width: `${(currentTimeDynamic * 100) / song.duration}%` }}
      ></div>

      <p className={classes["player-current-time"]}>
        {song.duration ? secondsToString(currentTimeDynamic) : "--:--"}
      </p>
      <p className={classes["player-total-time"]}>
        {song.duration ? secondsToString(song.duration) : "--:--"}
      </p>
    </div>
  );
}

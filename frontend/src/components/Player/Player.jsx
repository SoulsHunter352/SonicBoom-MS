import classes from "./Player.module.css";
import noTrackImg from "../../assets/images/noTrack.webp";
import PlayerLine from "./PlayerLine/PlayerLine";
import { useRef, useEffect, useState } from "react";
import DropdownMenu from "../DropdownMenu/DropdownMenu";

export default function Player({ song, updateSong, onSongEnd }) {
  const audioContextRef = useRef();
  const sourceNodeRef = useRef();
  const gainNodeRef = useRef();
  const [audioBuffer, setAudioBuffer] = useState(null);
  const [isOpenMenu, setIsOpenMenu] = useState(false);

  // Громкость
  const getVolume = () => (song.isMuted ? 0 : song.volume ? song.volume : 20);

  const updateVolume = (value) => {
    if (value <= 100 && value >= 0) {
      if (song.isMuted) updateSong({ isMuted: false });
      if (value === 0) updateSong({ isMuted: true });
      updateSong({ volume: value });
    }
  };

  // Запуск аудио буфера с n секунды
  const playAudio = (seconds) => {
    if (!audioBuffer || !audioContextRef.current) return;
    const audioContext = audioContextRef.current;
    const sourceNode = audioContext.createBufferSource();
    const gainNode = audioContext.createGain();
    sourceNode.buffer = audioBuffer;
    sourceNode.connect(gainNode).connect(audioContext.destination);
    gainNode.gain.value = getVolume() / 100;
    sourceNode.start(0, seconds);
    sourceNodeRef.current = sourceNode;
    gainNodeRef.current = gainNode;
    audioContext.resume();
  };

  // Остановка воспроизведения
  const stopAudio = () => {
    if (sourceNodeRef.current) {
      sourceNodeRef.current.stop();
      sourceNodeRef.current.disconnect();
      sourceNodeRef.current = null;
    }
  };

  // Перемотка
  const setAudioCurrentTime = (seconds) => {
    stopAudio();
    if (song.isPlaying) playAudio(seconds);
  };

  // Управление громкостью
  useEffect(() => {
    if (gainNodeRef.current) gainNodeRef.current.gain.value = getVolume() / 100;
  }, [song.isMuted, song.volume]);

  // При обновлении ссылки - загружаем в буфер
  useEffect(() => {
    if (!song.file) return;
    setAudioBuffer(null);
    const audioContext = new (window.AudioContext ||
      window.webkitAudioContext)();
    audioContextRef.current = audioContext;
    fetch(song.file)
      .then((response) => response.arrayBuffer())
      .then((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer))
      .then((buffer) => {
        updateSong({ duration: buffer.duration });
        setAudioBuffer(buffer);
      })
      .catch((err) => console.error("Ошибка загрузки аудио:", err));
    return () => {
      if (audioContextRef.current) audioContextRef.current.close();
    };
  }, [song.file]);

  // Горячие клавиши (Space, M, ArrowUp, ArrowDown)
  const documentRef = useRef(document);
  const handleKeyDown = (e) => {
    const tag = e.target.tagName;
    if ((tag === "INPUT" || tag === "TEXTAREA") && e.target.type !== "range")
      return;
    const key = e.key.toLowerCase();
    if (key === " " && audioBuffer) updateSong({ isPlaying: !song.isPlaying });
    else if (key === "m" || key === "ь") updateSong({ isMuted: !song.isMuted });
    else if (key === "arrowup") updateVolume(song.volume + 5);
    else if (key === "arrowdown") updateVolume(song.volume - 5);
  };
  useEffect(() => {
    documentRef.current.addEventListener("keydown", handleKeyDown);
    return () => {
      documentRef.current.removeEventListener("keydown", handleKeyDown);
    };
  }, [song]);

  function PlayerControlButton({ children, title, onClick }) {
    return (
      <button
        className={classes["player-controls-button"]}
        type="button"
        onClick={onClick}
        title={title}
      >
        {children}
      </button>
    );
  }

  return (
    <div className={classes["player"]}>
      <div className={classes["player-wrapper"]}>
        <PlayerLine
          song={song}
          updateSong={updateSong}
          audioCallback={setAudioCurrentTime}
          onSongEnd={onSongEnd}
          audioBuffer={audioBuffer}
        />

        <div className={classes["player-controls-wrapper"]}>
          <div className={classes["player-controls"]}>
            <PlayerControlButton title="Назад">
              <i className="fa-solid fa-backward"></i>
            </PlayerControlButton>

            <PlayerControlButton
              title={song.isPlaying ? "Пауза" : "Воспроизведение"}
              onClick={() => {
                if (audioBuffer) updateSong({ isPlaying: !song.isPlaying });
              }}
            >
              <i
                className={`fa-solid ${
                  song.isPlaying ? "fa-circle-pause" : "fa-circle-play"
                }`}
              ></i>
            </PlayerControlButton>

            <PlayerControlButton title="Вперёд">
              <i className="fa-solid fa-forward"></i>
            </PlayerControlButton>

            <div className={classes["player-repeat-song"]}>
              <PlayerControlButton
                title="Повторять трек"
                onClick={() => updateSong({ isRepeated: !song.isRepeated })}
              >
                <i
                  className={`fa-solid fa-repeat ${
                    song.isRepeated ? classes["active"] : ""
                  }`}
                ></i>
              </PlayerControlButton>
            </div>
          </div>

          <div className={classes["player-song-info"]}>
            <div className={classes["player-song-cover"]}>
              <img src={song.cover ? song.cover : noTrackImg} alt="cover" />
            </div>

            <div className={classes["player-song-info-text"]}>
              <div
                title={song.name ? song.name : "Трек не выбран"}
                className={classes["player-song-name-wrapper"]}
              >
                <p>{song.name ? song.name : "Трек не выбран"}</p>
              </div>

              <div
                title={song.artist ? song.artist : "-"}
                className={classes["player-song-artist-wrapper"]}
              >
                <p>{song.artist ? song.artist : "-"}</p>
              </div>
            </div>
          </div>

          <div className={classes["player-add-song"]}>
            {song.name && (
              <>
                <PlayerControlButton
                  title="Добавить трек в плейлист"
                  onClick={() => setIsOpenMenu((prev) => !prev)}
                >
                  <i className="fa-solid fa-circle-plus"></i>
                </PlayerControlButton>

                <DropdownMenu
                  isOpen={isOpenMenu}
                  setIsOpen={setIsOpenMenu}
                  up={true}
                >
                  <option>2</option>
                </DropdownMenu>
              </>
            )}
          </div>

          <div className={classes["player-volume-slider"]}>
            <PlayerControlButton
              title={song.isMuted ? "Включить звук" : "Выключить звук"}
              onClick={() => updateSong({ isMuted: !song.isMuted })}
            >
              <i
                className={`fa-solid ${
                  song.isMuted ? "fa-volume-xmark" : "fa-volume-high"
                }`}
              ></i>
            </PlayerControlButton>

            <input
              title="Ползунок громкости"
              type="range"
              name="player-volume"
              min="0"
              max="100"
              step="1"
              value={getVolume()}
              onChange={(e) => updateVolume(parseInt(e.target.value))}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

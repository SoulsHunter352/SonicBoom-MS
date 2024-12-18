import React, { useState, useRef } from "react";
import Form from "../../components/Form/Form";
import FormButton from "../../components/Form/FormButton/FormButton";
import GenreSelector from "../../components/TrackComponents/GenreSelector";
import classes from "./TrackAdd.module.css";
import { forwardRef } from "react";
import Mp3UploadButton from "../../components/TrackComponents/Mp3UploadButton";
export default function TrackAdd() {
  const inputs = {
    login: {
      inputType: "input",
      label: "Название трека",
      required: true,
      name: "login",
      placeholder: "",
    },
  };
  const TrackInput = () => {
    const [trackName, setTrackName] = React.useState("");

    const handleChange = (event) => {
      setTrackName(event.target.value);
    };

    return (
      <div className={classes["conteiner-text-area-track"]}>
        <label className={classes["text-area-track-label"]}>
          Введите текст песни
        </label>
        <textArea
          id="trackName"
          className={classes["text-area-track-add"]}
          type="text"
          placeholder=""
          value={trackName}
          onChange={handleChange}
        />
      </div>
    );
  };
  const form_button_title = "Добавить трек";
  const savePath = "../../assets/mp3file-TEST/";
  const textarelabel = "Введите текст трека";
  const genres = ["Панк", "Поп", "Кантри", "Рок"];
  const title = "Добавить трек";

  return (
    <div className={classes["TrackAddContent"]}>
      <Form
        inputs={inputs}
        title={title}
        children={[
          <GenreSelector genres={genres} />,
          <TrackInput />,
          <Mp3UploadButton savePath={savePath} />,
          <FormButton title={form_button_title} />,
        ]}
      />
    </div>
  );
}

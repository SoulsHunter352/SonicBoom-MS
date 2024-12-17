import React, { useState, useRef } from "react";
import Form from "../../components/Form/Form";
import FormButton from "../../components/Form/FormButton/FormButton";
import classes from "./GenreAdd.module.css";
export default function GenreAdd() {
  const inputs = {
    login: {
      inputType: "input",
      label: "Название жанра",
      required: true,
      name: "login",
      placeholder: "",
    },
  };
  const form_button_title = "Добавить жанр";
  const title = "Добавить жанр";
  return (
    <div className={classes["GenreAddContent"]}>
      <Form
        inputs={inputs}
        title={title}
        children={<FormButton title={form_button_title} />}
      />
    </div>
  );
}

import React, { useState } from "react";
import classes from "./FeedbackForm.module.css";

export default function FeedbackForm({ onSubmit }) {
  const [questionText, setQuestionText] = useState("");

  const handleChange = (event) => {
    setQuestionText(event.target.value);
  };

  const handleSubmit = () => {
    if (questionText.trim()) {
      onSubmit(questionText);
      setQuestionText(""); // Очищаем поле после отправки
    }
  };

  return (
    <section className={classes["feedback-form"]}>
      <h3>Задать вопрос</h3>
      <textarea
        placeholder="Текст вопроса"
        className={classes["text-area"]}
        value={questionText}
        onChange={handleChange}
      />
      <button className={classes["submit-button"]} onClick={handleSubmit}>
        Отправить вопрос
      </button>
    </section>
  );
}

import { useState } from "react";
import Header from "../Header/Header";
import classes from "./FeedbackPage.module.css";

export default function FeedbackPage() {
  return (
    <div className={classes["feedback-page"]}>
      <Header type="user" />
      <main className={classes["content-container"]}>
        <h2>Обратная связь</h2>
        <section className={classes["feedback-list"]}>
          <div className={classes["question"]}>
            <p>Вопрос</p>
            <p>Ответ на вопрос</p>
            <span className={classes["status"]} style={{ color: "red" }}>
              Не решен
            </span>
            <p>19:20 11.11.2024</p>
          </div>
          <div className={classes["question"]}>
            <p>Вопрос</p>
            <p>Ответ на вопрос</p>
            <span className={classes["status"]} style={{ color: "green" }}>
              Решен
            </span>
            <p>19:20 11.11.2024</p>
          </div>
          <div className={classes["question"]}>
            <p>Вопрос</p>
            <p>Ответ на вопрос</p>
            <span className={classes["status"]} style={{ color: "yellow" }}>
              Принят
            </span>
            <p>19:20 11.11.2024</p>
          </div>
        </section>
        <section className={classes["feedback-form"]}>
          <h3>Обратная связь</h3>
          <textarea
            placeholder="Текст вопроса"
            className={classes["text-area"]}
          />
          <button className={classes["submit-button"]}>
            Отправить сообщение
          </button>
        </section>
      </main>
    </div>
  );
}

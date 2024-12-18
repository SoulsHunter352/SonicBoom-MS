import React, { useState } from "react";
import classes from "./Feedback.module.css";
import { NavBar } from "../../../components/support/NavBar";
import Question from "../../../components/support/FeedbackQuestion";
import { SearchBar } from "../../../components/support/SearchBar";
import FeedbackForm from "../../../components/support/FeedbackForm";

/*const inputs = {
  description: {
    inputType: "textArea",
    label: "Задать вопрос",
    required: true,
    minLength: 1,
    name: "description",
  },
};*/

export default function FeedbackPage() {
  const initialQuestions = [
    {
      question: "Как использовать сайт?",
      answer: "...",
      status: "Не решен",
      timestamp: "19:20 11.11.2024",
    },
    {
      question: "Можно ли создать несколько плейлистов?",
      answer: "Да, вы можете создать любое количество плейлистов.",
      status: "Решен",
      timestamp: "19:30 11.11.2024",
    },
    {
      question: "Как изменить пароль?",
      answer: "Для изменения пароля перейдите в настройки профиля.",
      status: "Принят",
      timestamp: "19:40 11.11.2024",
    },
  ];

  const [questions, setQuestions] = useState(initialQuestions);
  const [originalQuestions] = useState(initialQuestions);

  const handleSearch = (query) => {
    if (query.trim() === "") {
      setQuestions(originalQuestions);
    } else {
      const filtered = originalQuestions.filter((item) =>
        item.question.toLowerCase().includes(query.toLowerCase())
      );
      setQuestions(filtered);
    }
  };

  const addQuestion = (newQuestionText) => {
    const newQuestion = {
      question: newQuestionText,
      answer: "",
      status: "Не решен",
      timestamp: new Date().toLocaleTimeString(),
    };

    setQuestions((prevQuestions) => [...prevQuestions, newQuestion]);
  };

  return (
    <div className={classes["feedback-page"]}>
      <NavBar />
      <main className={classes["content-container"]}>
        <SearchBar onSearch={handleSearch} />
        <FeedbackForm onSubmit={addQuestion} />
        <section className={classes["feedback-list"]}>
          {questions.map((question, index) => (
            <Question
              key={index}
              question={question.question}
              answer={question.answer}
              status={question.status}
              timestamp={question.timestamp}
            />
          ))}
        </section>
      </main>
    </div>
  );
}

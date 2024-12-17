import React from "react";
import classes from "./FeedbackQuestion.module.css";

export default function Question({ question, answer, status, timestamp }) {
  let statusColor = "red";
  if (status === "Решен") statusColor = "green";
  else if (status === "Принят") statusColor = "yellow";

  return (
    <div className={classes["question"]}>
      <p>{question}</p>
      <p>{answer}</p>
      <span className={classes["status"]} style={{ color: statusColor }}>
        {status}
      </span>
      <p>{timestamp}</p>
    </div>
  );
}

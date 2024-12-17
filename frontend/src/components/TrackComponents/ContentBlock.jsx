import React, { useState } from "react";
import classes from "./ContentBlock.module.css";
export default function ContentBlock({ content }) {
  return (
    <div className={classes["tab-content"]}>
      <p>{content}</p>
    </div>
  );
}

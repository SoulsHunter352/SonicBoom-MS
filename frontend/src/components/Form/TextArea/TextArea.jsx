import classesTextArea from "./TextArea.module.css";
import classes from "../Input/Input.module.css";
import { forwardRef } from "react";

function TextArea({ label, error, ...props }, ref) {
  return (
    <>
      <label className={classes.flabel} htmlFor={props.name}>
        {label}
      </label>
      <textarea
        id={props.name}
        ref={ref}
        className={`${classes.input} ${classesTextArea.input}`}
        {...props}
      ></textarea>
      <p className={classes.errors}>{error}</p>
    </>
  );
}

export default forwardRef(TextArea);

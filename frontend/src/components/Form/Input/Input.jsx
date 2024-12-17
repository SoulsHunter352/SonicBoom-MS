import { useState } from "react";
import classes from "./Input.module.css";
import TextArea from "../TextArea/TextArea";
import { forwardRef } from "react";

function Input({ label, setFormError, error, ...props }, ref) {
  const { inputType, ...inputProps } = props;

  return (
    <>
      <label className={classes.flabel} htmlFor={props.name}>
        {label}
      </label>
      <input
        id={props.name}
        className={classes.input}
        value={props.value}
        {...inputProps}
        ref={ref}
      ></input>
      <p className={classes.errors}>{error}</p>
    </>
  );
}

export default forwardRef(Input);

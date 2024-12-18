import classes from "./Form.module.css";
import Input from "./Input/Input";
import TextArea from "./TextArea/TextArea";
import FileInput from "./FileInput/FileInput";
import validate from "./validation.jsx";
import { useState, useRef } from "react";

export default function Form({ title, inputs, children }) {
  const [data, setData] = useState(() =>
    Object.entries(inputs).reduce((acc, input) => {
      acc[input[0]] = input[1].value || "";
      return acc;
    }, {})
  );

  const [errors, setErrors] = useState(() =>
    Object.entries(inputs).reduce((acc, input) => {
      acc[input[0]] = "";
      return acc;
    }, {})
  );

  function setError(key, value) {
    // console.log(key + value);
    setErrors({ ...errors, [key]: value });
    // console.log(errors[key]);
  }

  function validate_field(key, value) {
    return validate(inputs[key], value);
    // setError(key, validate(inputs[key], value));
  }

  function validate_field_on_blur(event) {
    let name = event.target.name;
    setError(name, validate_field(name, data[name]));
  }

  function form_validation(e) {
    e.preventDefault();
    let localErrors = {};
    for (let key of Object.keys(data)) {
      localErrors[key] = validate_field(key, data[key]);
    }
    setErrors(localErrors);
    for (let value of Object.values(localErrors)) {
      if (value) return;
    }
    console.log(data.login, data.password, data.description);
  }

  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  return (
    <div className={classes.wrapper}>
      <h2>{title}</h2>
      <form noValidate onSubmit={form_validation} className={classes.form}>
        {Object.entries(inputs).map((input, key) => {
          let { inputType, ...inputProps } = input[1];
          if (inputType == "input") {
            return (
              <Input
                key={key}
                {...inputProps}
                setFormError={setError}
                onBlur={validate_field_on_blur}
                onChange={handleChange}
                value={data[input[0]]}
                error={errors[input[0]]}
              />
            );
          } else if (inputType == "textArea")
            return (
              <TextArea
                key={key}
                {...inputProps}
                setFormError={setError}
                onBlur={validate_field_on_blur}
                onChange={handleChange}
                value={data[input[0]]}
                error={errors[input[0]]}
              />
            );
        })}
        {children}
      </form>
    </div>
  );
}

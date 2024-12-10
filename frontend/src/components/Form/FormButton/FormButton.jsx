import classes from "./FormButton.module.css";

export default function FormButton({ title }) {
  return (
    <button className={classes.form_button} type="submit">
      {title}
    </button>
  );
}

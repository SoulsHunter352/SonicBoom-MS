import classes from "./MainButton.module.css";

export default function MainButton({ children, title }) {
  return (
    <button
      title={title ? title : children}
      type="button"
      className={classes["main-btn"]}
    >
      {children}
    </button>
  );
}

import classes from "./MainButton.module.css";

export default function MainButton({ children, title, onClick }) {
  return (
    <button
      title={title ? title : children}
      type="button"
      className={classes["main-btn"]}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

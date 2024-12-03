import classes from "./DropdownMenu.module.css";
import { useRef } from "react";
import { useClickOutside } from "../../hooks/useClickOutside";

export default function DropdownMenu({
  setIsOpen,
  isOpen,
  children,
  className,
}) {
  const dropdownRef = useRef();

  useClickOutside(dropdownRef, () => {
    if (isOpen) setIsOpen(false);
  });

  function getItem(item, id) {
    if (item)
      return (
        <li key={id} className={classes["menu-item"]}>
          {item}
          {id !== children.length - 1 && <hr />}
        </li>
      );
    return null;
  }

  return (
    <nav
      className={`${classes.menu} ${isOpen ? classes.active : ""} ${
        className ? className : ""
      }`}
      ref={dropdownRef}
    >
      <ul className={classes["menu-list"]}>{children.map(getItem)}</ul>
    </nav>
  );
}

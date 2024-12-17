import classes from "./DropdownMenu.module.css";
import { useRef } from "react";
import { useClickOutside } from "../../hooks/useClickOutside";

export default function DropdownMenu({
  isOpen,
  setIsOpen,
  children,
  className,
  up = false,
}) {
  const dropdownRef = useRef();

  useClickOutside(dropdownRef, () => {
    if (isOpen) setIsOpen(false);
  });

  const getItem = (item, id) => {
    if (item)
      return (
        <li key={id} className={classes["menu-item"]}>
          {item}
          {children.length > 1 && id !== children.length - 1 && <hr />}
        </li>
      );
    return null;
  };

  return (
    <nav
      className={`${className ? className : ""} ${classes.menu} ${
        isOpen ? classes.active : ""
      } ${up ? classes.up : ""}`}
      ref={dropdownRef}
    >
      <ul className={classes["menu-list"]}>
        {children.map ? children.map(getItem) : getItem(children)}
      </ul>
    </nav>
  );
}

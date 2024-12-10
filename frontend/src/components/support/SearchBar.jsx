import React, { useState } from "react";
import classes from "./SearchBar.module.css";

export const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleInputChange = (event) => {
    setQuery(event.target.value);
    if (onSearch) {
      onSearch(event.target.value);
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.input_container}>
        <i className="fa-solid fa-magnifying-glass"></i>
        <input
          className={classes.info_search}
          type="text"
          value={query}
          onChange={handleInputChange}
          placeholder="Search..."
        />
      </div>
    </div>
  );
};

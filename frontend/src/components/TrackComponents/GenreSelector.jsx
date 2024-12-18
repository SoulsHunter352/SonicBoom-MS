import React, { useState } from "react";
import classes from "./GenreSelector.module.css";

export default function GenreSelector({ genres }) {
  const [selectedGenre, setSelectedGenre] = useState("");

  const handleGenreChange = (genre) => {
    setSelectedGenre(genre);
  };

  return (
    <div>
      <select
        className={classes["genre_selector"]}
        value={selectedGenre}
        onChange={(event) => handleGenreChange(event.target.value)}
      >
        <option value="" disabled>
          Выберите жанр
        </option>
        {genres.map((genre) => (
          <option key={genre} value={genre}>
            {genre}
          </option>
        ))}
      </select>
    </div>
  );
}

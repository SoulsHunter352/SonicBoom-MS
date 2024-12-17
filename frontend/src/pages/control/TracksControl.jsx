import React, { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { ControlList } from "../../components/control/ControlList/ControlList";
import { SearchBar } from "../../components/control/ControlSearch/SearchBar";

export default function TracksControl() {
  const { data } = useOutletContext(); // Получаем данные из контекста
  const tracks = data.tracks || []; // Извлекаем только альбомы, добавляем fallback на пустой массив

  // Состояние для результатов поиска
  const [filteredResults, setFilteredResults] = useState(tracks);

  // Обработчик поиска
  const handleSearch = (query) => {
    if (!query) {
      setFilteredResults(tracks);
    } else {
      const filtered = tracks.filter((item) =>
        item.name.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredResults(filtered);
    }
  };

  return (
    <div>
      {/* Поле поиска */}
      <SearchBar onSearch={handleSearch} />

      {/* Отображение результатов поиска */}
      <ControlList results={filteredResults} page={"tracks"} />
    </div>
  );
}

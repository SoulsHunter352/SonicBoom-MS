import React, { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { ControlList } from "../../components/control/ControlList/ControlList";
import { SearchBar } from "../../components/control/ControlSearch/SearchBar";

export default function AlbumsControl() {
  const { data } = useOutletContext(); // Получаем данные из контекста
  const albums = data.albums || []; // Извлекаем только альбомы, добавляем fallback на пустой массив

  // Состояние для результатов поиска
  const [filteredResults, setFilteredResults] = useState(albums);

  // Обработчик поиска
  const handleSearch = (query) => {
    if (!query) {
      setFilteredResults(albums); // Если запрос пуст, показать все альбомы
    } else {
      const filtered = albums.filter((item) =>
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
      <ControlList results={filteredResults} page={"albums"} />
    </div>
  );
}

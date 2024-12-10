import React from "react";
import { useParams, useLocation } from "react-router-dom";

export const EditUserPage = () => {
  const { id } = useParams(); // Получаем ID из URL
  const location = useLocation();
  const item = location.state?.item; // Данные переданного элемента (если есть)

  useEffect(() => {
    console.log(id); // или любой другой код для обработки изменений
  }, [id]); // Добавьте зависимости

  return (
    <div>
      <h1>Редактирование {item?.name || `элемента с ID ${id}`}</h1>
      {/* Здесь ваш код редактирования */}
    </div>
  );
};

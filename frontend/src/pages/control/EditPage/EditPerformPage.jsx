import { useParams } from "react-router-dom";

export const EditPage = () => {
  const { id } = useParams();

  return (
    <div>
      <h1>Редактировать элемент автора Альбома с ID: {id}</h1>
      {/* Логика редактирования */}
    </div>
  );
};

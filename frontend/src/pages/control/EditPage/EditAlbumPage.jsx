import { useParams } from "react-router-dom";

export const EditPage = () => {
  const { id } = useParams();
  console.log(id);

  return (
    <div>
      <h1>Редактировать элемент Альбома с ID: {id}</h1>
      {/* Логика редактирования */}
    </div>
  );
};

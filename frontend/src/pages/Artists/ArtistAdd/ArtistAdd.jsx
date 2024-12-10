import Form from "../../../components/Form/Form";
import FormButton from "../../../components/Form/FormButton/FormButton";

let inputs = {
  name: {
    inputType: "input",
    type: "text",
    label: "Имя исполнителя",
    required: true,
    name: "name",
    placeholder: "",
    value: "",
  },
  biography: {
    inputType: "textArea",
    type: "text",
    label: "Краткая биография",
    required: false,
    name: "biography",
    placeholder: "",
    value: "",
  },
  picture: {
    inputType: "fileInput",
    type: ".png, .jpg, .jpeg, .webp",
    label: "Фотография",
    required: false,
    name: "picture",
    placeholder: "",
    value: "",
  },
};

export default function ArtistAdd() {
  return (
    <div style={{ margin: "auto" }}>
      <Form title="Добавить исполнителя" inputs={inputs}>
        <FormButton title="Сохранить" />
      </Form>
    </div>
  );
}

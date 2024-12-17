import Form from "../../../components/Form/Form";
import FormButton from "../../../components/Form/FormButton/FormButton";
import UserAvatar from "../../../components/users/UserAvatar/UserAvatar";
import ProfileCard from "../../../components/users/ProfileCard/ProfileCard";

let inputs = {
  old_password: {
    inputType: "input",
    type: "password",
    label: "Старый пароль",
    required: true,
    name: "old_password",
    placeholder: "",
    value: "",
  },
  new_password1: {
    inputType: "input",
    type: "password",
    label: "Новый пароль",
    required: true,
    minLength: 8,
    name: "new_password1",
    placeholder: "",
    value: "",
  },
  new_password2: {
    inputType: "input",
    type: "password",
    label: "Повторите новый пароль",
    required: true,
    minLength: 8,
    name: "new_password2",
    placeholder: "",
    value: "",
  },
};

export default function ChangePassword() {
  return (
    <div style={{ margin: "auto" }}>
      <Form title="Сменить пароль" inputs={inputs}>
        <FormButton title="Сохранить" />
      </Form>
    </div>
  );
}

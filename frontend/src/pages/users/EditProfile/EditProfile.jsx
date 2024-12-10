import Form from "../../../components/Form/Form";
import FormButton from "../../../components/Form/FormButton/FormButton";
import UserAvatar from "../../../components/users/UserAvatar/UserAvatar";
import { Link } from "react-router-dom";
import ProfileCard from "../../../components/users/ProfileCard/ProfileCard";

const inputs = {
  email: {
    inputType: "input",
    label: "E-mail*",
    required: true,
    name: "email",
    placeholder: "",
    value: "test@gmail.com",
  },
  username: {
    inputType: "input",
    label: "Никнейм*",
    required: true,
    minLength: 8,
    name: "username",
    placeholder: "",
    value: "Никнейм",
  },
};

export default function ChangePassword() {
  return (
    <div style={{ margin: "auto" }}>
      <ProfileCard>
        <UserAvatar />
        <Form title="" inputs={inputs}>
          <FormButton title="Сохранить" />
        </Form>
      </ProfileCard>
    </div>
  );
}

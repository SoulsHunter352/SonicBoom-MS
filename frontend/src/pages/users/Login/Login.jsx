import Form from "../../../components/Form/Form";
import FormButton from "../../../components/Form/FormButton/FormButton";
import { Link } from "react-router-dom";

const inputs = {
  login: {
    inputType: "input",
    label: "Логин или email",
    required: true,
    name: "login",
    placeholder: "",
  },
  password: {
    inputType: "input",
    type: "password",
    label: "Пароль",
    required: true,
    minLength: 8,
    name: "password",
    placeholder: "",
  },
};

export default function Login() {
  return (
    <div style={{ margin: "auto" }}>
      <Form title="Авторизация" inputs={inputs}>
        <FormButton title="Войти" />
        <p>
          Нет аккаунта?
          <Link to="/registration">
            <span style={{ color: "rgb(4, 124, 162)" }}> Создать аккаунт</span>
          </Link>
        </p>
      </Form>
    </div>
  );
}

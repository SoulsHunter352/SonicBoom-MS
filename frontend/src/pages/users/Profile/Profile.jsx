import UserAvatar from "../../../components/users/UserAvatar/UserAvatar";
import ProfileCard from "../../../components/users/ProfileCard/ProfileCard";
import FormButton from "../../../components/Form/FormButton/FormButton";
import classes from "./Profile.module.css";
import { Link } from "react-router-dom";

const username = "Никнейм";
const email = "test@gmail.com";
const login = "Логин";

export default function Profile() {
  return (
    <>
      <ProfileCard>
        <div className={classes.about_user}>
          <div className={classes.info}>
            <p>{username}</p>
            <p>{email}</p>
            <p>{login}</p>
          </div>
          <UserAvatar />
        </div>
        <div className={classes.actions}>
          <Link to="/edit-profile">
            <FormButton title="Редактировать профиль" />
          </Link>
          <Link to="/change-password">
            <FormButton title="Сменить пароль" />
          </Link>
        </div>
      </ProfileCard>
    </>
  );
}

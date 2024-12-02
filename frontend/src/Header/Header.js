import classes from "./Header.module.css";
import MainButton from "../MainButton/MainButton";
import logoImg from "../../public/assets/546px-SBMS.png";
import noAvatarImg from "../../public/assets/no-avatar.jpg";

export default function Header({ type }) {
  return (
    <header className={classes.header}>
      <div className={classes["brand-container"]}>
        <img src={logoImg} alt="LOGO" />
        <p>Sonic BOOM</p>
      </div>
      <div className={classes["search-container"]}>
        <MainButton title={"Поиск"}>
          <i class="fa-solid fa-magnifying-glass"></i>
        </MainButton>
      </div>
      <div className={classes["nav-buttons-container"]}>
        {type === "non-auth" ? (
          <>
            <MainButton>Регистрация</MainButton>
            <MainButton>Вход</MainButton>
          </>
        ) : (
          <>
            <MainButton>Мои плейлисты</MainButton>
            {type === "admin" && <MainButton>Управление</MainButton>}
            <MainButton>Вопросы</MainButton>
          </>
        )}
      </div>
      {type !== "non-auth" && (
        <div className={classes["avatar-container"]}>
          <img src={noAvatarImg} alt="USER" />
        </div>
      )}
    </header>
  );
}

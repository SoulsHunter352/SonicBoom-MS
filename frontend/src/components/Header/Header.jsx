import classes from "./Header.module.css";
import MainButton from "./MainButton/MainButton";
import DropdownMenu from "../DropdownMenu/DropdownMenu";
import logoImg from "../../assets/images/600px-SBMS.webp";
import noAvatarImg from "../../assets/images/noAvatar.webp";
import { useState } from "react";
import { Link } from "react-router-dom";

export default function Header({ user }) {
  const [isOpenNav, setIsOpenNav] = useState(false);
  const [isOpenProfile, setIsOpenProfile] = useState(false);
  const [isOpenSearch, setIsOpenSearch] = useState(false);

  function navButtons() {
    return user.type === "non-auth" ? (
      <>
        <MainButton to="/registration">Регистрация</MainButton>
        <MainButton to="/login">Вход</MainButton>
      </>
    ) : (
      <>
        <MainButton>Мои плейлисты</MainButton>
        {user.type === "admin" && (
          <MainButton to="/control/users">Управление</MainButton>
        )}
        <MainButton to="/feedback">Вопросы</MainButton>
      </>
    );
  }

  return (
    <header className={classes.header}>
      <Link to="/">
        <div className={classes["brand-container"]}>
          <img src={logoImg} alt="logo" />
          <p>Sonic BOOM</p>
        </div>
      </Link>

      <div className={classes["search-container"]}>
        <MainButton
          title="Поиск"
          onClick={() => setIsOpenSearch((prev) => !prev)}
        >
          <i className="fa-solid fa-magnifying-glass"></i>
        </MainButton>

        <DropdownMenu isOpen={isOpenSearch} setIsOpen={setIsOpenSearch}>
          <input type="text" name="search" placeholder="Поиск..." />
        </DropdownMenu>
      </div>

      <div className={classes["nav-buttons-container"]}>{navButtons()}</div>

      <div className={classes["bars-container"]}>
        <MainButton
          title="Развернуть список"
          onClick={() => setIsOpenNav((prev) => !prev)}
        >
          <i className="fa-solid fa-bars"></i>
        </MainButton>

        <DropdownMenu
          isOpen={isOpenNav}
          setIsOpen={setIsOpenNav}
          className={classes["header-dropdown-menu"]}
        >
          {navButtons().props.children}
        </DropdownMenu>
      </div>

      {user.type !== "non-auth" && (
        <div className={classes["avatar-container"]}>
          <img
            src={user?.avatar ? user.avatar : noAvatarImg}
            alt="avatar"
            onClick={() => setIsOpenProfile((prev) => !prev)}
            title="Профиль пользователя"
          />

          <DropdownMenu
            isOpen={isOpenProfile}
            setIsOpen={setIsOpenProfile}
            className={classes["header-dropdown-menu"]}
          >
            <p>{user?.nickname ? user.nickname : ""}</p>
            <MainButton to="/profile">Профиль</MainButton>
            <MainButton>Поддержка</MainButton>
            <MainButton>О сайте</MainButton>
            <MainButton title="Выйти">
              <span style={{ color: "red" }}>Выйти</span>
            </MainButton>
          </DropdownMenu>
        </div>
      )}
    </header>
  );
}

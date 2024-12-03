import classes from "./Header.module.css";
import MainButton from "../MainButton/MainButton";
import DropdownMenu from "../DropdownMenu/DropdownMenu";
import logoImg from "../../assets/images/600px-SBMS.webp";
import noAvatarImg from "../../assets/images/noAvatar.webp";
import { useState } from "react";

export default function Header({ user, type }) {
  const [isOpenNav, setIsOpenNav] = useState(false);
  const [isOpenProfile, setIsOpenProfile] = useState(false);

  function toggleIsOpenNav() {
    setIsOpenNav((prev) => !prev);
  }

  function toggleIsOpenProfile() {
    setIsOpenProfile((prev) => !prev);
  }

  function navButtons() {
    return type === "non-auth" ? (
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
    );
  }

  return (
    <header className={classes.header}>
      <div className={classes["brand-container"]}>
        <img src={logoImg} alt="LOGO" />
        <p>Sonic BOOM</p>
      </div>

      <div className={classes["search-container"]}>
        <MainButton title="Поиск">
          <i class="fa-solid fa-magnifying-glass"></i>
        </MainButton>
      </div>

      <div className={classes["nav-buttons-container"]}>{navButtons()}</div>

      <div className={classes["bars-container"]}>
        <MainButton title="Развернуть список" onClick={toggleIsOpenNav}>
          <i class="fa-solid fa-bars"></i>
        </MainButton>

        <DropdownMenu
          setIsOpen={setIsOpenNav}
          isOpen={isOpenNav}
          className={classes["header-dropdown-menu"]}
        >
          {navButtons().props.children}
        </DropdownMenu>
      </div>

      {type !== "non-auth" && (
        <div className={classes["avatar-container"]}>
          <img
            src={user?.avatar ? user.avatar : noAvatarImg}
            alt="USER"
            onClick={toggleIsOpenProfile}
            title="Профиль пользователя"
          />

          <DropdownMenu
            setIsOpen={setIsOpenProfile}
            isOpen={isOpenProfile}
            className={classes["header-dropdown-menu"]}
          >
            <p>{user?.nickname ? user.nickname : "Никнейм"}</p>
            <MainButton>Профиль</MainButton>
            <MainButton>Поддержка</MainButton>
            <MainButton>
              <span style={{ color: "red" }}>Выход</span>
            </MainButton>
          </DropdownMenu>
        </div>
      )}
    </header>
  );
}

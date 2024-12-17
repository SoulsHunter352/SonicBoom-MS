import classes from "./ControlPanel.module.css";
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom"; // Импортируем useNavigate

// Компонент для панели управления
export default function ControlPanel({
  activeTab,
  setActiveTab,
  buttonLabels,
  Icon,
  redirectPath,
  user, // Добавляем переменную для пути перенаправления
}) {
  const [isOpen, setIsOpen] = useState(false); // Состояние для управления выпадающим меню
  const [isOpenProfile, setIsOpenProfile] = useState(false);
  const navigate = useNavigate(); // Инициализируем useNavigate

  const toggleMenu = () => {
    setIsOpen((prev) => !prev);
  };

  const handlePlusButtonClick = () => {
    navigate(redirectPath); // Перенаправляем на указанный путь
  };

  return (
    <div className={classes["tabs"]}>
      {buttonLabels.map((label, index) => (
        <button
          key={index}
          className={`${classes["tab-button"]} ${
            activeTab === label ? classes["active"] : ""
          }`}
          onClick={() => setActiveTab(label)}
        >
          {label}
        </button>
      ))}
      <div className={classes["relative-container"]}>
        {user.type === "admin" ? (
          <Link to={redirectPath}>
            <button
              className={`${classes["plus-button"]}`}
              // Обработчик нажатия кнопки
            >
              <img
                src={Icon}
                alt="plus_cover"
                className={classes["plus-button"]}
              />
            </button>
          </Link>
        ) : null}

        {/*
        <DropdownMenu
          isOpen={isOpenProfile}
          setIsOpen={setIsOpenProfile}
          className={`${classes["dropdown-menu"]} ${
            isOpenProfile ? classes.active : ""
          }`}
        >
          <MainButton onClick={() => setIsOpenProfile(false)}>
            Добавить
          </MainButton>
          <MainButton onClick={() => setIsOpenProfile(false)}>
            Редактировать
          </MainButton>
          <MainButton onClick={() => setIsOpenProfile(false)}>
            Удалить
          </MainButton>
        </DropdownMenu>
        */}
      </div>
      {/* Кнопка для открытия выпадающего меню */}
    </div>
  );
}

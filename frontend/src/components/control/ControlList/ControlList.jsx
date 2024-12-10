import React from "react";
import { Link } from "react-router-dom";
import classes from "./ControlList.module.css";

export const ControlList = ({ results, page }) => {
  return (
    <div className={classes.container}>
      <ul className={classes.ul_list}>
        {results.map((result, index) => (
          <li className={classes.li_list} key={index}>
            {/* Отображение изображения */}
            <img src={result.icon} alt={result.name} className={classes.icon} />

            {/* Отображение имени */}
            <span className={classes.span_name}>{result.name}</span>

            {/* Ссылка на редактирование */}
            <Link to={`/control/${page}/edit/${result.id}`}>
              <span className={classes.span_control}>Редактировать</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

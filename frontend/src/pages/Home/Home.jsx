import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Добро пожаловать!</h1>
      <p style={styles.text}>Это главная страница приложения.</p>
      <Link to="/track">
        <button type="button" style={styles.link}>
          Перейти к странице трека
        </button>
      </Link>

      <Link to="/artist">
        <button type="button" style={styles.link}>
          Перейти к странице исполнителя
        </button>
      </Link>

      <Link to="/album">
        <button type="button" style={styles.link}>
          Перейти к странице альбома
        </button>
      </Link>

      <Link to="/login">
        <button type="button" style={styles.link}>
          Перейти к странице login
        </button>
      </Link>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f5f5f5",
    fontFamily: "Arial, sans-serif",
    textAlign: "center",
  },
  heading: {
    fontSize: "2.5rem",
    color: "#333",
    marginBottom: "1rem",
  },
  text: {
    fontSize: "1.2rem",
    color: "#555",
    textAlign: "center",
    marginBottom: "2rem",
  },
  link: {
    fontSize: "1rem",
    color: "#fff",
    backgroundColor: "#6c63ff",
    padding: "10px 20px",
    textDecoration: "none",
    borderRadius: "5px",
  },
};

import "./styles.css";
import Header from "./Header/Header";
import { useState } from "react";

export default function App() {
  const [headerType, setHeaderType] = useState("admin");

  return (
    <>
      <Header type={headerType}></Header>
    </>
  );
}

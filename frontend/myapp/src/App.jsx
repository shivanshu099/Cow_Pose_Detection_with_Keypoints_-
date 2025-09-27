import { useState } from "react";
import "./App.css";
import Classification from "./components/classification";
import Navbar from "./components/Navbar";

import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Classification />
    </>
  );
}

export default App;

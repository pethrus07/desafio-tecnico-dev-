/**
 * Ponto de entrada do bundle: monta o <App /> na div #root do index.html.
 * Separa "onde a aplicação nasce" de "o que ela é" — nenhuma decisão de
 * produto mora aqui. O import do index.css neste arquivo é o que faz o CSS
 * do Tailwind entrar no bundle; sem ele a tela sobe sem estilo nenhum.
 */
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

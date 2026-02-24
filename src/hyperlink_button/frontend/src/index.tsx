import React from "react";
import { createRoot } from "react-dom/client";
import { withStreamlitConnection } from "streamlit-component-lib";
import HyperlinkButton from "./HyperlinkButton";
import "./style.css";

const Connected = withStreamlitConnection(HyperlinkButton);

const root = document.getElementById("root");
if (root) {
  createRoot(root).render(<Connected />);
}

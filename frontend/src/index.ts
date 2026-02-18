import { RenderData, Streamlit } from "streamlit-component-lib";

type ComponentArgs = {
  label?: string;
  help?: string;
  disabled?: boolean;
  use_container_width?: boolean;
};

const style = document.createElement("style");
style.textContent = `
  :root {
    --hyperlink-color: #1f6feb;
    --hyperlink-focus: #1f6feb;
  }

  body {
    margin: 0;
    padding: 0;
    background: transparent;
    color: inherit;
  }

  .hyperlink-button {
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    color: var(--hyperlink-color);
    font: inherit;
    text-align: left;
    cursor: pointer;
    text-decoration: none;
    line-height: 1.2;
  }

  .hyperlink-button:hover {
    text-decoration: underline;
  }

  .hyperlink-button:focus-visible {
    outline: 2px solid var(--hyperlink-focus);
    outline-offset: 2px;
    border-radius: 2px;
  }

  .hyperlink-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    text-decoration: none;
  }

  .hyperlink-button.full-width {
    width: 100%;
  }
`;
document.head.appendChild(style);

const button = document.createElement("button");
button.type = "button";
button.className = "hyperlink-button";
document.body.appendChild(button);

let clickCount = 0;

button.addEventListener("click", () => {
  if (button.disabled) {
    return;
  }
  clickCount += 1;
  Streamlit.setComponentValue(clickCount);
});

const applyTheme = (theme?: RenderData["theme"]) => {
  const linkColor = theme?.primaryColor ?? "#1f6feb";
  document.documentElement.style.setProperty("--hyperlink-color", linkColor);
  document.documentElement.style.setProperty("--hyperlink-focus", linkColor);

  if (theme?.font) {
    document.body.style.fontFamily = theme.font;
  }

  if (theme?.textColor) {
    document.body.style.color = theme.textColor;
  }
};

const onRender = (event: CustomEvent<RenderData>) => {
  const data = event.detail;
  const args = (data.args ?? {}) as ComponentArgs;
  const label = args.label ?? "";
  const help = args.help ?? "";
  const isDisabled = Boolean(args.disabled ?? data.disabled ?? false);
  const useContainerWidth = Boolean(args.use_container_width ?? false);

  button.textContent = label;
  button.title = help;
  button.disabled = isDisabled;

  if (useContainerWidth) {
    button.classList.add("full-width");
  } else {
    button.classList.remove("full-width");
  }

  applyTheme(data.theme);
  Streamlit.setFrameHeight();
};

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight();

import { Streamlit } from "streamlit-component-lib"

// For debugging/testing: the Streamlit component-lib doesn't attach itself to window.
// Expose it so headless tests can verify the bundle executed.
;(window as any).__hyperlink_button_streamlit = Streamlit

type Args = {
  label?: string
  help?: string
  disabled?: boolean
  width?: "content" | "stretch" | number
  icon?: string | null
  icon_position?: "left" | "right"
  shortcut?: string | null
}

function render(args: Args, theme: any): void {
  const root = document.getElementById("root")
  if (!root) return

  // Reset
  root.innerHTML = ""

  const label = String(args.label ?? "")
  const disabled = Boolean(args.disabled)

  const btn = document.createElement("button")
  btn.type = "button"
  btn.textContent = label
  btn.disabled = disabled

  // Link-like styling. We keep it minimal and rely on Streamlit theme vars.
  const primary = getComputedStyle(document.documentElement).getPropertyValue("--primary-color").trim()
  const text = getComputedStyle(document.documentElement).getPropertyValue("--text-color").trim()
  const color = primary || text || "#0b5fff"

  btn.style.background = "transparent"
  btn.style.border = "0"
  btn.style.padding = "0"
  btn.style.margin = "0"
  btn.style.color = color
  btn.style.cursor = disabled ? "not-allowed" : "pointer"
  btn.style.font = "inherit"
  btn.style.textDecoration = "none"
  btn.style.lineHeight = "1.2"
  btn.style.display = "inline"

  btn.addEventListener("mouseenter", () => {
    if (!disabled) btn.style.textDecoration = "underline"
  })
  btn.addEventListener("mouseleave", () => {
    btn.style.textDecoration = "none"
  })

  if (args.help) {
    btn.title = String(args.help)
  }

  btn.addEventListener("click", (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (disabled) return
    Streamlit.setComponentValue(true)
  })

  root.appendChild(btn)

  Streamlit.setFrameHeight()
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (event: any) => {
  const data = event.detail
  render(data.args as Args, data.theme)
})

// If we are loaded outside Streamlit (e.g. direct navigation to index.html),
// render a simple placeholder so it's obvious the bundle is alive.
setTimeout(() => {
  const root = document.getElementById("root")
  if (!root) return
  if (root.childElementCount > 0) return
  const hint = document.createElement("div")
  hint.textContent = "hyperlink_button: waiting for Streamlit"
  hint.style.font = "12px/1.4 system-ui, sans-serif"
  hint.style.opacity = "0.6"
  root.appendChild(hint)
  Streamlit.setFrameHeight()
}, 50)

Streamlit.setComponentReady()

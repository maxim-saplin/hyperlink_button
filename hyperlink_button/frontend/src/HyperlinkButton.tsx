import React, { useCallback, useEffect, useMemo, useRef, useState } from "react"
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib"

type IconPosition = "left" | "right"
type WidthOption = "content" | "stretch" | number
type ButtonType = "primary" | "secondary" | "tertiary"

interface ComponentArgs {
  label: string
  testid?: string | null
  help?: string | null
  disabled?: boolean
  icon?: string | null
  icon_position?: IconPosition
  width?: WidthOption
  use_container_width?: boolean | null
  type?: ButtonType
  instance_id?: string | number | null
  last_click_count?: number | null
}

const typeColors: Record<ButtonType, string> = {
  primary: "#1a73e8",
  secondary: "#0b5a7a",
  tertiary: "#1f4a2e"
}

const setRootStyles = (host: HTMLElement) => {
  host.style.margin = "0"
  host.style.padding = "0"
  host.style.display = "block"
}

const buildTestId = (args: ComponentArgs): string => {
  if (typeof args.testid === "string" && args.testid.length > 0) {
    return args.testid
  }
  if (args.instance_id !== undefined && args.instance_id !== null) {
    return `hyperlink-button-${args.instance_id}`
  }
  return "hyperlink-button"
}

const normalizeWidth = (width: WidthOption | undefined, useContainer: boolean) => {
  if (useContainer) {
    return "100%"
  }
  if (width === "stretch") {
    return "100%"
  }
  if (width === "content" || width === undefined) {
    return "auto"
  }
  if (typeof width === "number" && Number.isFinite(width)) {
    return `${width}px`
  }
  return "auto"
}

const parseLastClickCount = (value: unknown): number => {
  if (typeof value === "number" && Number.isFinite(value) && value >= 0) {
    return Math.floor(value)
  }
  return 0
}

const HyperlinkButton = (props: StreamlitComponentBase) => {
  const args = props.args as ComponentArgs
  const [clickCount, setClickCount] = useState(() =>
    parseLastClickCount(args.last_click_count)
  )
  const isFirstRender = useRef(true)

  useEffect(() => {
    setRootStyles(document.body)
    Streamlit.setFrameHeight()
  }, [])

  const label = typeof args.label === "string" ? args.label : ""
  const help = typeof args.help === "string" ? args.help : undefined
  const disabled = Boolean(args.disabled)
  const icon = typeof args.icon === "string" ? args.icon : undefined
  const iconPosition = (args.icon_position ?? "left") as IconPosition
  const buttonType = (args.type ?? "secondary") as ButtonType
  const useContainerWidth = Boolean(args.use_container_width)
  const width = args.width as WidthOption | undefined

  const testId = useMemo(() => buildTestId(args as ComponentArgs), [args])
  const size = useMemo(
    () => normalizeWidth(width, useContainerWidth),
    [width, useContainerWidth]
  )

  const handleActivate = useCallback(() => {
    if (disabled) {
      return
    }
    setClickCount((prev) => prev + 1)
  }, [disabled])

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false
      return
    }
    Streamlit.setComponentValue(clickCount)
  }, [clickCount])

  const styles = {
    "--hb-color": typeColors[buttonType] ?? typeColors.primary,
    width: size
  } as React.CSSProperties

  const iconElement = icon ? (
    <span className="hb-icon" aria-hidden="true">
      {icon}
    </span>
  ) : null

  return (
    <div className="hb-root" data-testid={testId} style={styles}>
      <button
        className="hb-button"
        type="button"
        onClick={handleActivate}
        disabled={disabled}
        aria-disabled={disabled}
        title={help}
      >
        {iconPosition === "left" && iconElement}
        <span className="hb-label">{label}</span>
        {iconPosition === "right" && iconElement}
      </button>
    </div>
  )
}

export default withStreamlitConnection(HyperlinkButton)

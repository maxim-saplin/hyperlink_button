import React, { useCallback, useEffect, useMemo, useState } from "react";
import { ComponentProps, Streamlit } from "streamlit-component-lib";

type Variant = "primary" | "secondary" | "tertiary";
type IconPosition = "left" | "right";

const coerceVariant = (value: unknown): Variant => {
  if (value === "primary" || value === "tertiary") {
    return value;
  }
  return "secondary";
};

const coerceIconPosition = (value: unknown): IconPosition => {
  if (value === "right") {
    return "right";
  }
  return "left";
};

type ParsedIcon =
  | { kind: "none" }
  | { kind: "material"; name: string }
  | { kind: "text"; text: string };

const parseIcon = (value: unknown): ParsedIcon => {
  if (typeof value !== "string" || value.trim().length === 0) {
    return { kind: "none" };
  }

  const m = value.match(/^:material\/([a-z0-9_]+):$/i);
  if (m) {
    return { kind: "material", name: m[1] };
  }

  return { kind: "text", text: value };
};

const newClickId = (): string => {
  try {
    return crypto.randomUUID();
  } catch {
    return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }
};

const HyperlinkButton = ({ args, theme }: ComponentProps) => {
  const label = typeof args?.label === "string" ? args.label : "Link";
  const help = typeof args?.help === "string" ? args.help : undefined;
  const disabled = Boolean(args?.disabled);
  const useContainerWidth = Boolean(args?.use_container_width);
  const icon = useMemo(() => parseIcon(args?.icon), [args?.icon]);
  const variant = coerceVariant(args?.type);
  const iconPosition = coerceIconPosition(args?.icon_position);

  const [lastClickId, setLastClickId] = useState<string>("");

  const styleVars = useMemo(() => {
    const primary = theme?.primaryColor;
    return primary ? ({ "--hb-link": primary } as React.CSSProperties) : undefined;
  }, [theme?.primaryColor]);

  const handleClick = useCallback(() => {
    if (disabled) {
      return;
    }
    const next = newClickId();
    setLastClickId(next);
    Streamlit.setComponentValue({ click_id: next });
  }, [disabled]);

  useEffect(() => {
    Streamlit.setFrameHeight();
  });

  const containerClass = useContainerWidth ? "hb-container hb-full" : "hb-container";
  const buttonClass = `hb-button hb-${variant}`;

  const leftIcon = iconPosition === "left";

  return (
    <div className={containerClass} style={styleVars}>
      <button
        className={buttonClass}
        type="button"
        disabled={disabled}
        onClick={handleClick}
        title={help}
        aria-label={help ?? label}
        data-testid="hyperlink-button"
      >
        {leftIcon && icon.kind === "text" ? (
          <span className="hb-icon" aria-hidden="true">
            {icon.text}
          </span>
        ) : null}
        {leftIcon && icon.kind === "material" ? (
          <span className="hb-material" aria-hidden="true">
            {icon.name}
          </span>
        ) : null}
        <span className="hb-label">{label}</span>
        {!leftIcon && icon.kind === "text" ? (
          <span className="hb-icon" aria-hidden="true">
            {icon.text}
          </span>
        ) : null}
        {!leftIcon && icon.kind === "material" ? (
          <span className="hb-material" aria-hidden="true">
            {icon.name}
          </span>
        ) : null}
      </button>
    </div>
  );
};

export default HyperlinkButton;

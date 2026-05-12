import { COLORS } from "../../constants";

export function StatusDot({ status }) {
  const colors = {
    live: COLORS.teal,
    err: COLORS.red,
    connecting: COLORS.amber,
    "": "rgba(136,135,128,0.4)",
  };
  const isBlinking = status === "connecting";

  return (
    <span
      style={{
        width: 7,
        height: 7,
        borderRadius: "50%",
        flexShrink: 0,
        display: "inline-block",
        background: colors[status] || colors[""],
        animation: isBlinking ? "blink 1s ease-in-out infinite" : "none",
      }}
    />
  );
}


export function LegendSwatch({ color, dashed }) {
  return (
    <span
      style={{
        height: 2,
        width: 20,
        borderRadius: 1,
        flexShrink: 0,
        background: dashed
          ? `repeating-linear-gradient(to right, ${color} 0 5px, transparent 5px 9px)`
          : color,
      }}
    />
  );
}


import { styles } from "../styles";

export function ConfigForm({ clientId, size, interval_, target, onSizeChange, onIntervalChange, onTargetChange }) {
  return (
    <div style={styles.formGrid}>
      <div style={styles.field}>
        <label style={styles.label}>
          Job batch size <span style={{ opacity: 0.6 }}>(50-300)</span>
        </label>
        <input style={styles.input} type="number" min={50} max={300} step={1} value={size} onChange={onSizeChange} />
      </div>
      <div style={styles.field}>
        <label style={styles.label}>
          Arrival Interval <span style={{ opacity: 0.6 }}>(2-5)</span>
        </label>
        <input style={styles.input} type="number" min={2} max={5} step={1} value={interval_} onChange={onIntervalChange} />
      </div>
      <div style={{ ...styles.field, gridColumn: "span 2" }}>
        <label style={styles.label}>
          Target % <span style={{ opacity: 0.6 }}>(10-80)</span>
        </label>
        <input style={styles.input} type="number" min={10} max={80} step={1} value={target} onChange={onTargetChange} />
      </div>
    </div>
  );
}


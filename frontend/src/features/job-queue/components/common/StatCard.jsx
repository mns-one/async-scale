import { styles } from "../../styles";

export function StatCard({ label, value, color }) {
  return (
    <div style={styles.statCard}>
      <div style={styles.statLabel}>{label}</div>
      <div style={{ ...styles.statValue, color: color || "#f0ede8" }}>{value != null ? value : "-"}</div>
    </div>
  );
}

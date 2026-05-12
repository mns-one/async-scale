import { styles } from "../styles";
import { StatusDot } from "./common/StatusDot";

export function MonitorHeader({ status, statusTxt }) {
  return (
    <div style={styles.header}>
      <h1 style={styles.h1}>Async Flow</h1>
      <p style={styles.subtitle}>Configure job simulation parameters and observe live processing stats</p>
      <div style={styles.statusRow}>
        <StatusDot status={status} />
        <span>{statusTxt}</span>
      </div>
    </div>
  );
}


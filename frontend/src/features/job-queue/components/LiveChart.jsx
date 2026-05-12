import { COLORS, MAX_PTS } from "../constants";
import { styles } from "../styles";
import { LegendSwatch } from "./common/LegendSwatch";

export function LiveChart({ canvasRef, seq, ts }) {
  return (
    <div style={styles.chartCard}>
      <div style={styles.chartTop}>
        <span style={styles.chartLbl}>Live feed - last {MAX_PTS} packets</span>
        <div style={styles.legend}>
          <span style={styles.legItem}>
            <LegendSwatch color={COLORS.blue} />
            Jobs to process
          </span>
          <span style={styles.legItem}>
            <LegendSwatch color={COLORS.teal} dashed />
            Active workers
          </span>
        </div>
      </div>

      <div style={{ position: "relative", height: 220 }}>
        <canvas ref={canvasRef} role="img" aria-label="Live line chart showing jobs to process and active workers over time" />
      </div>

      <div style={styles.footerBar}>
        <span style={styles.footerTxt}>{seq != null ? `seq ${seq}` : "seq -"}</span>
        <span style={styles.footerTxt}>{ts || "-"}</span>
      </div>
    </div>
  );
}


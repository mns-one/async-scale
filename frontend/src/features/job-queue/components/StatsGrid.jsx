import { COLORS } from "../constants";
import { styles } from "../styles";
import { StatCard } from "./common/StatCard";

export function StatsGrid({ stats }) {
  const jobsToProcess = Number(stats?.jobs_to_process ?? 0);
  const activeWorkers = Number(stats?.active_workers ?? 0);
  const ratioPercent =
    activeWorkers > 0 ? `${((activeWorkers / jobsToProcess) * 100).toFixed(2)}%` : "0.00%";

  return (
    <div style={styles.statsGrid}>
      <StatCard label="Jobs to process" value={stats?.jobs_to_process} color={COLORS.blue} />
      <StatCard label="Active workers" value={stats?.active_workers} color={COLORS.teal} />
      <StatCard label="Job to Worker Ratio" value={ratioPercent} />
      <StatCard label="New jobs arrived" value={`+${Number(stats?.new_jobs ?? 0)}`} color={COLORS.red}/>
    </div>
  );
}

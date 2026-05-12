import { useEffect, useState } from "react";
import { styles } from "../styles";
import { uuid } from "../utils/uuid";
import { useLiveChart } from "../hooks/useLiveChart";
import { useJobQueueSession } from "../hooks/useJobQueueSession";
import { MonitorHeader } from "../components/MonitorHeader";
import { ConfigForm } from "../components/ConfigForm";
import { StatsGrid } from "../components/StatsGrid";
import { LiveChart } from "../components/LiveChart";

export default function JobQueueMonitorPage() {
  const [clientId] = useState(() => uuid());
  const [size, setSize] = useState(200);
  const [interval_, setInterval_] = useState(3);
  const [target, setTarget] = useState(40);

  const { canvasRef, resetChart, pushPoint } = useLiveChart();
  const session = useJobQueueSession({
    clientId,
    size,
    interval_,
    target,
    onBeforeStart: resetChart,
    onDataPoint: pushPoint,
  });
  const { stopSession } = session;

  useEffect(() => {
    resetChart();
  }, [resetChart]);

  useEffect(() => {
    return () => {
      stopSession();
    };
  }, [stopSession]);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
        input[type=number]::-webkit-inner-spin-button { opacity: 0.4; }
        input[type=number]:focus { border-color: rgba(136,135,128,0.6) !important; box-shadow: 0 0 0 2px rgba(55,138,221,0.15); }
      `}</style>

      <div style={styles.wrap}>
        <MonitorHeader status={session.status} statusTxt={session.statusTxt} />

        <ConfigForm
          clientId={clientId}
          size={size}
          interval_={interval_}
          target={target}
          onSizeChange={(e) => setSize(Number(e.target.value))}
          onIntervalChange={(e) => setInterval_(Number(e.target.value))}
          onTargetChange={(e) => setTarget(Number(e.target.value))}
        />

        <div style={styles.btnRow}>
          <button
            style={session.running ? styles.btnStop : styles.btnStart}
            onClick={session.running ? stopSession : session.startSession}
          >
            {session.running ? "End" : "START"}
          </button>
        </div>
        <div style={styles.simLine}>
          10 Job batches of size upto {size} will arrive at an interval of max {interval_} second <br/>
          Server will scale workers to process {target}% of pending jobs
        </div>

        <hr style={styles.sep} />

        <StatsGrid stats={session.stats} />
        <LiveChart canvasRef={canvasRef} seq={session.seq} ts={session.ts} />
      </div>
    </>
  );
}

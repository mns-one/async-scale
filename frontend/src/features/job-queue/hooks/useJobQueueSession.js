import { useCallback, useRef, useState } from "react";
import { createSessionSocket, postSessionConfig } from "../services/jobQueueApi";

const EMPTY_STATS = {
  jobs_to_process: null,
  active_workers: null,
  jobs_done: null,
  new_jobs: null,
};

export function useJobQueueSession({ clientId, size, interval_, target, onBeforeStart, onDataPoint }) {
  const [status, setStatus] = useState("");
  const [statusTxt, setStatusTxt] = useState("Not connected");
  const [stats, setStats] = useState(null);
  const [seq, setSeq] = useState(null);
  const [ts, setTs] = useState(null);
  const [running, setRunning] = useState(false);

  const wsRef = useRef(null);
  const lastStatsRef = useRef(EMPTY_STATS);

  const stopSession = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const startSession = useCallback(async () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    lastStatsRef.current = EMPTY_STATS;
    setSeq(null);
    setTs(null);
    setStats(null);
    onBeforeStart();
    setRunning(false);
    setStatus("connecting");
    setStatusTxt("Connecting...");

    const ws = createSessionSocket(clientId);
    wsRef.current = ws;

    ws.onopen = async () => {
      setStatus("connecting");
      setStatusTxt("Connected - sending config...");
      try {
        const res = await postSessionConfig({ clientId, size, interval_, target });
        if (res.ok) {
          setStatus("live");
          setStatusTxt("Live");
          setRunning(true);
        } else {
          setStatus("err");
          setStatusTxt(`POST error ${res.status}`);
        }
      } catch {
        setStatus("err");
        setStatusTxt("POST failed - is backend running?");
      }
    };

    ws.onmessage = (e) => {
      try {
        const pkt = JSON.parse(e.data);
        const payload = pkt.payload ?? {};
        const merged = { ...lastStatsRef.current, ...payload };
        lastStatsRef.current = merged;

        setSeq(pkt.seq);
        setTs(new Date(pkt.ts).toLocaleTimeString());
        setStats(merged);

        if (Number.isFinite(merged.jobs_to_process) && Number.isFinite(merged.active_workers)) {
          onDataPoint(pkt.seq, merged.jobs_to_process, merged.active_workers);
        }
      } catch {
        // Ignore malformed packets and keep session alive.
      }
    };

    ws.onerror = () => {
      setStatus("err");
      setStatusTxt("WebSocket error");
      setRunning(false);
    };

    ws.onclose = () => {
      setStatus("");
      setStatusTxt("Disconnected");
      setRunning(false);
    };
  }, [clientId, size, interval_, target, onBeforeStart, onDataPoint]);

  return {
    status,
    statusTxt,
    stats,
    seq,
    ts,
    running,
    startSession,
    stopSession,
  };
}


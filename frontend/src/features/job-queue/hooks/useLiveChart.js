import { useCallback, useEffect, useRef } from "react";
import { Chart as ChartJS, registerables } from "chart.js";
import { COLORS, MAX_PTS } from "../constants";

ChartJS.register(...registerables);

export function useLiveChart() {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  const resetChart = useCallback(() => {
    if (!canvasRef.current) {
      return;
    }

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const ctx = canvasRef.current.getContext("2d");
    chartRef.current = new ChartJS(ctx, {
      type: "line",
      data: {
        labels: [0],
        datasets: [
          {
            label: "Jobs to process",
            data: [0],
            borderColor: COLORS.blue,
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
            fill: false,
          },
          {
            label: "Active workers",
            data: [0],
            borderColor: COLORS.teal,
            borderWidth: 2,
            borderDash: [5, 4],
            pointRadius: 0,
            tension: 0.3,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 },
        plugins: {
          legend: { display: false },
          tooltip: {
            mode: "index",
            intersect: false,
            backgroundColor: "rgba(12,12,12,0.9)",
            titleFont: { family: "monospace", size: 11 },
            bodyFont: { family: "monospace", size: 11 },
            padding: 8,
            borderColor: "rgba(136,135,128,0.2)",
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            ticks: { display: false },
            grid: { color: "rgba(136,135,128,0.08)" },
            border: { display: false },
          },
          y: {
            beginAtZero: true,
            ticks: {
              font: { family: "monospace", size: 10 },
              color: "#5f5e5a",
              maxTicksLimit: 5,
              callback: (v) => Math.round(v),
            },
            grid: { color: "rgba(136,135,128,0.08)" },
            border: { display: false },
          },
        },
      },
    });
  }, []);

  const pushPoint = useCallback((seqN, jobs, workers) => {
    const chart = chartRef.current;
    if (!chart) {
      return;
    }

    chart.data.labels.push(seqN);
    chart.data.datasets[0].data.push(jobs);
    chart.data.datasets[1].data.push(workers);

    if (chart.data.labels.length > MAX_PTS) {
      chart.data.labels.shift();
      chart.data.datasets[0].data.shift();
      chart.data.datasets[1].data.shift();
    }

    chart.update("none");
  }, []);

  useEffect(() => {
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, []);

  return { canvasRef, resetChart, pushPoint };
}


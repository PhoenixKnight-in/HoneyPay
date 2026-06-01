import { useState, useEffect } from "react";
import LiveFeed from "./components/LiveFeed";
import AttackTypeChart from "./components/AttackTypeChart";
import TopIPsChart from "./components/TopIPsChart";
import VolumeChart from "./components/VolumeChart";
import StatsCounter from "./components/StatsCounter";
import Sidebar from "./components/Sidebar";
import "./index.css";
import axios from "axios";

const API_BASE = "http://localhost:8001";

export default function App() {
  const [attacks, setAttacks] = useState([]);
  const [stats, setStats] = useState(null);
  const [activeNav, setActiveNav] = useState("Overview");
  const [apiStatus, setApiStatus] = useState("checking");

  const fetchData = async () => {
    try {
      const [statsRes, logsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/stats`),
        axios.get(`${API_BASE}/api/logs?limit=50`)
      ]);
      setStats(statsRes.data);
      setAttacks(logsRes.data);
      setApiStatus("online");
    } catch (err) {
      console.error("Failed to fetch data:", err);
      setApiStatus("offline");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-shell">
      <Sidebar activeNav={activeNav} setActiveNav={setActiveNav} />
      <div className="main-content">
        {/* Top Bar */}
        <header className="topbar">
          <div className="topbar-left">
            <span className="topbar-title">HONEYPAY SOC</span>
            <div className="topbar-indicators">
              <span className={`indicator ${apiStatus === "online" ? "online" : "offline"}`}>
                <span className="dot" /> API Status: {apiStatus === "online" ? "Online" : "Offline"}
              </span>
              <span className="indicator online">
                <span className="dot" /> Honeypot: Active
              </span>
            </div>
          </div>
          <div className="topbar-right">
            <span className="total-attacks-badge">
              Total Attacks: <strong>{stats?.total ?? 0}</strong>
            </span>
          </div>
        </header>

        {/* Stats Row */}
        <StatsCounter stats={stats} attacks={attacks} />

        {/* Middle Row: Live Feed + Attack Types */}
        <div className="middle-row">
          <div className="panel feed-panel">
            <div className="panel-header">
              <span>Live Attack Feed</span>
              <span className="live-badge">LIVE DATA</span>
            </div>
            <LiveFeed attacks={attacks} />
          </div>
          <div className="panel chart-panel">
            <div className="panel-header">
              <span>Attack Types</span>
            </div>
            <AttackTypeChart data={stats?.by_type ?? []} />
            <TopIPsChart data={stats?.top_ips ?? []} />
          </div>
        </div>

        {/* Volume Chart */}
        <div className="panel volume-panel">
          <div className="panel-header">
            <div>
              <div className="panel-title">Attack Volume (Last 24h)</div>
              <div className="panel-subtitle">Aggregated sensor data across all endpoints</div>
            </div>
            <span className="threat-badge">● THREAT INTENSITY</span>
          </div>
          <VolumeChart data={stats?.hourly ?? []} />
        </div>
      </div>
    </div>
  );
}
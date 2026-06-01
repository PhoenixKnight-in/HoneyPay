import {
  AreaChart, Area, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid
} from "recharts";

function formatHour(isoStr) {
  if (!isoStr) return "";
  const d = new Date(isoStr);
  return d.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: false });
}

export default function VolumeChart({ data }) {
  const counts = data.map(d => d.count);
  const peak = counts.length > 0 ? Math.max(...counts) : 0;
  const avg = counts.length > 0 ? Math.round(counts.reduce((a, b) => a + b, 0) / counts.length) : 0;

  const lastSpike = data
    .slice()
    .reverse()
    .find(d => d.count > avg);

  const lastSpikeTime = lastSpike
    ? new Date(lastSpike.hour).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })
    : "--";

  const chartData = data.map(d => ({
    hour: formatHour(d.hour),
    count: d.count,
  }));

  return (
    <div className="volume-chart">
      <ResponsiveContainer width="100%" height={180}>
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis
            dataKey="hour"
            tick={{ fill: "#475569", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            interval="preserveStartEnd"
          />
          <YAxis
            tick={{ fill: "#475569", fontSize: 10 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 6 }}
            labelStyle={{ color: "#94a3b8" }}
            itemStyle={{ color: "#3b82f6" }}
          />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#3b82f6"
            strokeWidth={2}
            fill="url(#areaGrad)"
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className="volume-stats">
        <div className="vol-stat">
          <div className="vol-stat-label">PEAK VOLUME</div>
          <div className="vol-stat-value">{peak}/hr</div>
        </div>
        <div className="vol-stat">
          <div className="vol-stat-label">AVERAGE VOLUME</div>
          <div className="vol-stat-value">{avg}/hr</div>
        </div>
        <div className="vol-stat">
          <div className="vol-stat-label">LAST SPIKE</div>
          <div className="vol-stat-value orange">{lastSpikeTime}</div>
        </div>
        <div className="vol-stat">
          <div className="vol-stat-label">THREAT DURATION</div>
          <div className="vol-stat-value">{data.length} hrs</div>
        </div>
      </div>
    </div>
  );
}
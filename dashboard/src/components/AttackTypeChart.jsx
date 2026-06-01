import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = {
  "SQL Injection": "#dc2626",
  "Brute Force":   "#d97706",
  "Recon":         "#2563eb",
  "Scanner":       "#7c3aed",
};

const DEFAULT_COLOR = "#334155";

export default function AttackTypeChart({ data }) {
  const total = data.reduce((sum, d) => sum + d.count, 0);

  return (
    <div className="attack-type-chart">
      <div className="donut-wrapper">
        <ResponsiveContainer width="100%" height={160}>
          <PieChart>
            <Pie
              data={data.length > 0 ? data : [{ attack_type: "None", count: 1 }]}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={72}
              dataKey="count"
              nameKey="attack_type"
              strokeWidth={0}
            >
              {(data.length > 0 ? data : [{ attack_type: "None", count: 1 }]).map((entry, i) => (
                <Cell
                  key={i}
                  fill={COLORS[entry.attack_type] || DEFAULT_COLOR}
                />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 6 }}
              labelStyle={{ color: "#94a3b8" }}
              itemStyle={{ color: "#e2e8f0" }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="donut-center">
          <div className="donut-pct">100%</div>
          <div className="donut-label">CLASSIFIED</div>
        </div>
      </div>

      <div className="type-legend">
        {data.map((entry, i) => {
          const pct = total > 0 ? Math.round((entry.count / total) * 100) : 0;
          const color = COLORS[entry.attack_type] || DEFAULT_COLOR;
          return (
            <div className="legend-row" key={i}>
              <span className="legend-bar" style={{ borderLeftColor: color }} />
              <span className="legend-name">{entry.attack_type}</span>
              <span className="legend-pct" style={{ color }}>{pct}%</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
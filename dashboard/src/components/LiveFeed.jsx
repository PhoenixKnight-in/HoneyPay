const TYPE_COLORS = {
  "SQL Injection": { bg: "#dc2626", text: "#fff" },
  "Brute Force":   { bg: "#d97706", text: "#fff" },
  "Recon":         { bg: "#2563eb", text: "#fff" },
  "Scanner":       { bg: "#7c3aed", text: "#fff" },
};

function formatTime(ts) {
  if (!ts) return "--";
  const d = new Date(ts);
  return d.toLocaleTimeString("en-US", { hour12: true, hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function truncate(str, n) {
  if (!str) return "--";
  return str.length > n ? str.slice(0, n) + "..." : str;
}

export default function LiveFeed({ attacks }) {
  return (
    <div className="livefeed">
      <table className="feed-table">
        <thead>
          <tr>
            <th>TIMESTAMP</th>
            <th>SOURCE IP</th>
            <th>TARGET</th>
            <th>TYPE</th>
            <th>STATUS</th>
          </tr>
        </thead>
        <tbody>
          {attacks.length === 0 ? (
            <tr>
              <td colSpan={5} className="feed-empty">No attacks yet. Run a script!</td>
            </tr>
          ) : (
            attacks.slice(0, 20).map((a, i) => {
              const color = TYPE_COLORS[a.attack_type] || { bg: "#334155", text: "#fff" };
              return (
                <tr key={i} className="feed-row">
                  <td className="feed-time">{formatTime(a.timestamp)}</td>
                  <td className="feed-ip">{a.ip_address}</td>
                  <td className="feed-endpoint">{truncate(a.endpoint, 22)}</td>
                  <td>
                    <span className="type-badge" style={{ background: color.bg, color: color.text }}>
                      {a.attack_type}
                    </span>
                  </td>
                  <td>
                    <span className="status-dot detected" />
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
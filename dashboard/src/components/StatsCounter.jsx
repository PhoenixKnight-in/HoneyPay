export default function StatsCounter({ stats, attacks }) {
  const blockedIPs = [...new Set(attacks.map(a => a.ip_address))].length;
  const honeypotHits = attacks.filter(a =>
    ["/admin/panel", "/api/internal/db/dump", "/config/env",
     "/api/root/override", "/api/v1/users/all"].includes(a.endpoint)
  ).length;

  const cards = [
    {
      label: "TOTAL ATTACKS DETECTED",
      value: (stats?.total ?? 0).toLocaleString(),
      sub: "+12% vs last hour",
      subColor: "#4ade80",
      subIcon: "↑",
    },
    {
      label: "HONEYPOT HITS",
      value: honeypotHits.toLocaleString(),
      sub: "Status: High Activity",
      subColor: "#f59e0b",
      subIcon: "⚠",
    },
    {
      label: "BLOCKED IPS",
      value: blockedIPs.toLocaleString(),
      sub: "Active bans",
      subColor: "#94a3b8",
      subIcon: "⊘",
    },
    {
      label: "SYSTEM HEALTH",
      value: "99.9%",
      sub: "Uptime consistent",
      subColor: "#94a3b8",
      subIcon: "◷",
    },
  ];

  return (
    <div className="stats-row">
      {cards.map((card) => (
        <div className="stat-card" key={card.label}>
          <div className="stat-label">{card.label}</div>
          <div className="stat-value">{card.value}</div>
          <div className="stat-sub" style={{ color: card.subColor }}>
            {card.subIcon} {card.sub}
          </div>
        </div>
      ))}
    </div>
  );
}
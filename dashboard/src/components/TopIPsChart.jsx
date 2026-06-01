export default function TopIPsChart({ data }) {
  const max = data.length > 0 ? Math.max(...data.map(d => d.count)) : 1;

  return (
    <div className="top-ips">
      <div className="top-ips-title">Top Attacker IPs</div>
      {data.length === 0 ? (
        <div className="feed-empty">No data yet</div>
      ) : (
        data.map((entry, i) => (
          <div className="ip-row" key={i}>
            <span className="ip-rank">#{i + 1}</span>
            <span className="ip-addr">{entry.ip_address}</span>
            <div className="ip-bar-wrap">
              <div
                className="ip-bar"
                style={{ width: `${(entry.count / max) * 100}%` }}
              />
            </div>
            <span className="ip-count">{entry.count}</span>
          </div>
        ))
      )}
    </div>
  );
}
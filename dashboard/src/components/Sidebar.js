export default function Sidebar({ activeNav, setActiveNav }) {
  const navItems = [
    { icon: "⊞", label: "Overview" },
    { icon: "◈", label: "Real-time Logs" },
    { icon: "⬡", label: "Honeypot Monitor" },
    { icon: "◎", label: "Attack Simulator" },
    { icon: "⚙", label: "Settings" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">⬡</div>
        <div className="logo-text">
          <div className="logo-name">HONEYPAY</div>
          <div className="logo-sub">Payment API Shield</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.label}
            className={`nav-item ${activeNav === item.label ? "active" : ""}`}
            onClick={() => setActiveNav(item.label)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <button className="scan-btn">Initiate Scan</button>
        <button className="nav-item">
          <span className="nav-icon">?</span>
          <span className="nav-label">Support</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon">→</span>
          <span className="nav-label">Logout</span>
        </button>
      </div>
    </aside>
  );
}
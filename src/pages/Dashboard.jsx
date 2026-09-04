import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";

const RISK_COLORS = { low: "#16a34a", medium: "#d97706", high: "#dc2626" };

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [risk, setRisk] = useState(null);
  const [history, setHistory] = useState([]);
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [riskRes, historyRes, moduleRes] = await Promise.all([
          api.get("/academics/my-risk/"),
          api.get("/academics/my-risk-history/"),
          api.get("/academics/my-module-performance/"),
        ]);
        setRisk(riskRes.data);
        setHistory(
          historyRes.data.map((h) => ({
            ...h,
            computed_at: new Date(h.computed_at).toLocaleDateString(),
          }))
        );
        setModules(moduleRes.data);
      } catch (err) {
        console.error("Failed to load dashboard", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, []);

  if (loading) return <div style={styles.centered}>Loading your dashboard...</div>;

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.headerTitle}>Welcome, {user?.first_name || "Student"}</h1>
          <p style={styles.headerSub}>Student No: {user?.student_number}</p>
        </div>
        <button style={styles.logoutButton} onClick={logout}>Log Out</button>
      </header>

      <section style={styles.riskCard}>
        <div>
          <p style={styles.riskLabel}>Current Risk Level</p>
          <span
            style={{
              ...styles.riskBadge,
              background: RISK_COLORS[risk?.risk_level] || "#999",
            }}
          >
            {risk?.risk_level?.toUpperCase()}
          </span>
        </div>
        <p style={styles.adviceText}>{risk?.advice_text}</p>
      </section>

      <section style={styles.chartCard}>
        <h2 style={styles.sectionTitle}>Risk Trend</h2>
        {history.length > 1 ? (
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="computed_at" />
              <YAxis dataKey="average_mark" domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="average_mark" stroke="#2563eb" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p style={{ color: "#666" }}>Not enough history yet to show a trend.</p>
        )}
      </section>

      <section style={styles.tableCard}>
        <h2 style={styles.sectionTitle}>Module Performance</h2>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Module</th>
              <th style={styles.th}>Weighted Avg</th>
              <th style={styles.th}>Status</th>
              <th style={styles.th}>At Risk</th>
            </tr>
          </thead>
          <tbody>
            {modules.map((m) => (
              <tr key={m.module_code}>
                <td style={styles.td}>{m.module_code} — {m.module_name}</td>
                <td style={styles.td}>{m.weighted_average ?? "—"}%</td>
                <td style={styles.td}>{m.status}</td>
                <td style={styles.td}>{m.at_risk_in_module ? "⚠️ Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

const styles = {
  page: { fontFamily: "system-ui, sans-serif", background: "#f4f6f8", minHeight: "100vh", padding: "2rem" },
  centered: { display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", fontFamily: "system-ui, sans-serif" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" },
  headerTitle: { margin: 0, fontSize: "1.4rem" },
  headerSub: { margin: 0, color: "#666", fontSize: "0.9rem" },
  logoutButton: { padding: "0.5rem 1rem", background: "#fff", border: "1px solid #ccc", borderRadius: "6px", cursor: "pointer" },
  riskCard: { background: "#fff", borderRadius: "12px", padding: "1.5rem", marginBottom: "1.5rem", boxShadow: "0 2px 10px rgba(0,0,0,0.05)" },
  riskLabel: { margin: "0 0 0.5rem", color: "#666", fontSize: "0.85rem" },
  riskBadge: { display: "inline-block", padding: "0.3rem 0.9rem", borderRadius: "999px", color: "#fff", fontWeight: 600, fontSize: "0.9rem" },
  adviceText: { marginTop: "1rem", color: "#333", lineHeight: 1.5 },
  chartCard: { background: "#fff", borderRadius: "12px", padding: "1.5rem", marginBottom: "1.5rem", boxShadow: "0 2px 10px rgba(0,0,0,0.05)" },
  tableCard: { background: "#fff", borderRadius: "12px", padding: "1.5rem", boxShadow: "0 2px 10px rgba(0,0,0,0.05)" },
  sectionTitle: { marginTop: 0, fontSize: "1.1rem" },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { textAlign: "left", padding: "0.6rem", borderBottom: "2px solid #eee", fontSize: "0.85rem", color: "#666" },
  td: { padding: "0.6rem", borderBottom: "1px solid #eee", fontSize: "0.9rem" },
};
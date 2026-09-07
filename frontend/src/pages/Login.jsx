import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [studentNumber, setStudentNumber] = useState("");
  const [password, setPassword] = useState("");
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await login(studentNumber, password);
    if (success) navigate("/dashboard");
  };

  return (
    <div style={styles.wrapper}>
      <form style={styles.card} onSubmit={handleSubmit}>
        <h1 style={styles.title}>Student Login</h1>

        <label style={styles.label}>Student Number</label>
        <input
          style={styles.input}
          value={studentNumber}
          onChange={(e) => setStudentNumber(e.target.value)}
          placeholder="e.g. 202285904"
          required
        />

        <label style={styles.label}>Password</label>
        <input
          style={styles.input}
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && <p style={styles.error}>{error}</p>}

        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Log In"}
        </button>

        <p style={styles.footerText}>
          Don't have an account? <a href="/register">Register here</a>
        </p>
      </form>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    background: "#f4f6f8",
    fontFamily: "system-ui, sans-serif",
  },
  card: {
    background: "#fff",
    padding: "2.5rem",
    borderRadius: "12px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
    width: "100%",
    maxWidth: "380px",
  },
  title: { marginBottom: "1.5rem", fontSize: "1.5rem", fontWeight: 600 },
  label: { display: "block", fontSize: "0.85rem", marginBottom: "0.3rem", color: "#444" },
  input: {
    width: "100%",
    padding: "0.6rem 0.75rem",
    marginBottom: "1rem",
    border: "1px solid #ccc",
    borderRadius: "6px",
    fontSize: "1rem",
    boxSizing: "border-box",
  },
  button: {
    width: "100%",
    padding: "0.7rem",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    fontSize: "1rem",
    cursor: "pointer",
  },
  error: { color: "#dc2626", fontSize: "0.85rem", marginBottom: "1rem" },
  footerText: { marginTop: "1rem", fontSize: "0.85rem", textAlign: "center" },
};
import React, { useEffect, useState } from 'react';

const API_BASE = '/api';

function App() {
  // ---- Items ----
  const [items, setItems] = useState([]);
  const [itemsError, setItemsError] = useState(null);

  // ---- Loan Decision ----
  const [income, setIncome] = useState('');
  const [debt, setDebt] = useState('');
  const [employmentYears, setEmploymentYears] = useState('');
  const [decision, setDecision] = useState(null);
  const [decisionError, setDecisionError] = useState(null);

  // ---- Memory ----
  const [memUserId, setMemUserId] = useState('');
  const [memContext, setMemContext] = useState(''); // JSON string
  const [token, setToken] = useState('');
  const [recalledContext, setRecalledContext] = useState(null);
  const [memoryMessage, setMemoryMessage] = useState('');

  // Load items on mount
  useEffect(() => {
    fetch(`${API_BASE}/items`)
      .then(res => res.json())
      .then(data => setItems(data.items || []))
      .catch(err => setItemsError(err.message));
  }, []);

  // ---- Loan Decision handler ----
  const requestLoanDecision = async () => {
    setDecisionError(null);
    setDecision(null);
    try {
      const res = await fetch(`${API_BASE}/loan-decision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          income: parseFloat(income),
          debt: parseFloat(debt),
          employment_years: parseInt(employmentYears)
        })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setDecision(data);
    } catch (err) {
      setDecisionError(err.message);
    }
  };

  // ---- Memory handlers ----
  const handleRemember = async () => {
    try {
      const contextObj = JSON.parse(memContext);
      const res = await fetch(`${API_BASE}/remember`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: memUserId, context: contextObj })
      });
      const data = await res.json();
      setToken(data.token);
      setMemoryMessage(`Token stored: ${data.token}`);
    } catch (err) {
      setMemoryMessage(`Error: ${err.message}`);
    }
  };

  const handleRecall = async () => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE}/recall/${token}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setRecalledContext(data);
      setMemoryMessage('');
    } catch (err) {
      setMemoryMessage(`Error: ${err.message}`);
    }
  };

  const handleForget = async () => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE}/forget/${token}`, { method: 'DELETE' });
      const data = await res.json();
      setMemoryMessage(data.status);
      setRecalledContext(null);
    } catch (err) {
      setMemoryMessage(`Error: ${err.message}`);
    }
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '2rem', maxWidth: 800, margin: '0 auto' }}>
      <h1>Platform Engineer Demo</h1>

      {/* ---------- Infrastructure Items ---------- */}
      <section style={{ marginBottom: '2rem' }}>
        <h2>Infrastructure Items</h2>
        {itemsError && <p style={{ color: 'red' }}>Error: {itemsError}</p>}
        {items.length === 0 && !itemsError && <p>Loading items...</p>}
        <ul>
          {items.map(item => (
            <li key={item.id}>
              <strong>{item.name}</strong> <small>(ID: {item.id})</small>
            </li>
          ))}
        </ul>
      </section>

      {/* ---------- Loan Decision (Traceable Reasoning) ---------- */}
      <section style={{ marginBottom: '2rem', borderTop: '2px solid #ccc', paddingTop: '1rem' }}>
        <h2>Loan Decision (Traceable Reasoning)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', maxWidth: 400 }}>
          <label>Income:</label>
          <input value={income} onChange={e => setIncome(e.target.value)} type="number" />
          <label>Debt:</label>
          <input value={debt} onChange={e => setDebt(e.target.value)} type="number" />
          <label>Employment years:</label>
          <input value={employmentYears} onChange={e => setEmploymentYears(e.target.value)} type="number" />
        </div>
        <button onClick={requestLoanDecision} style={{ marginTop: '0.5rem' }}>Request decision</button>
        {decisionError && <p style={{ color: 'red' }}>Error: {decisionError}</p>}
        {decision && (
          <div style={{ marginTop: '1rem' }}>
            <p><strong>Approved:</strong> {decision.approved ? 'Yes' : 'No'}</p>
            <p><strong>Reasoning chain:</strong></p>
            <ol>
              {decision.reasoning.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ol>
          </div>
        )}
      </section>

      {/* ---------- Governed Memory ---------- */}
      <section style={{ borderTop: '2px solid #ccc', paddingTop: '1rem' }}>
        <h2>Governed Memory (Privacy by Design)</h2>
        <div style={{ marginBottom: '1rem' }}>
          <h3>Store context (PII is automatically filtered)</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', maxWidth: 500 }}>
            <label>User ID (will be pseudonymized):</label>
            <input value={memUserId} onChange={e => setMemUserId(e.target.value)} />
            <label>Context (JSON, e.g. {"{ \"preference\":\"dark\", \"email\":\"a@b.com\" }"}):</label>
            <input value={memContext} onChange={e => setMemContext(e.target.value)} />
          </div>
          <button onClick={handleRemember} style={{ marginTop: '0.5rem' }}>Remember</button>
          {memoryMessage && <p>{memoryMessage}</p>}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <h3>Recall / Forget</h3>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              value={token}
              onChange={e => setToken(e.target.value)}
              placeholder="Token"
              style={{ flex: 1 }}
            />
            <button onClick={handleRecall}>Recall</button>
            <button onClick={handleForget}>Forget (right to erasure)</button>
          </div>
          {recalledContext && (
            <pre style={{ background: '#f0f0f0', padding: '0.5rem' }}>
              {JSON.stringify(recalledContext, null, 2)}
            </pre>
          )}
        </div>
      </section>
    </div>
  );
}

export default App;
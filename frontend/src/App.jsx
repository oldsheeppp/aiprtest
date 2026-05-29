import { useEffect, useState } from "react";
import { CreditCard, RotateCcw, Search, ShieldCheck } from "lucide-react";

import "./styles.css";


async function requestJson(path, options = {}) {
  const response = await fetch(path, options);
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.detail || "request failed");
  }
  return body;
}


export default function App() {
  const [userId, setUserId] = useState("1");
  const [amountCents, setAmountCents] = useState("1200");
  const [currency, setCurrency] = useState("USD");
  const [user, setUser] = useState(null);
  const [userError, setUserError] = useState("");
  const [payment, setPayment] = useState(null);
  const [paymentError, setPaymentError] = useState("");
  const [events, setEvents] = useState([]);
  const [auditError, setAuditError] = useState("");

  async function loadUser(nextUserId = userId) {
    setUserError("");
    try {
      setUser(await requestJson(`/users/${nextUserId}`));
    } catch (error) {
      setUser(null);
      setUserError(error.message);
    }
  }

  async function chargePayment(event) {
    event.preventDefault();
    setPaymentError("");
    try {
      setPayment(
        await requestJson("/payments/charge", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: Number(userId),
            amount_cents: Number(amountCents),
            currency: currency.toUpperCase()
          })
        })
      );
    } catch (error) {
      setPayment(null);
      setPaymentError(error.message);
    }
  }

  async function refundPayment() {
    if (!payment) {
      setPaymentError("charge a payment before refunding");
      return;
    }

    setPaymentError("");
    try {
      setPayment(
        await requestJson("/payments/refund", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ payment_id: payment.id })
        })
      );
    } catch (error) {
      setPaymentError(error.message);
    }
  }

  async function loadAuditLog() {
    setAuditError("");
    try {
      const body = await requestJson("/admin/audit-log", {
        headers: { "X-Role": "admin" }
      });
      setEvents(body.events);
    } catch (error) {
      setEvents([]);
      setAuditError(error.message);
    }
  }

  useEffect(() => {
    loadUser("1");
  }, []);

  return (
    <main className="app-shell">
      <header className="top-bar">
        <div>
          <p className="eyebrow">FastAPI + React</p>
          <h1>PR Review Sandbox</h1>
        </div>
        <span className="status-pill">In-memory data</span>
      </header>

      <section className="workspace" aria-label="Sandbox controls">
        <div className="panel user-panel">
          <div className="panel-heading">
            <h2>User lookup</h2>
            <p>Read public user records from the API.</p>
          </div>
          <div className="inline-controls">
            <label>
              User ID
              <input
                min="1"
                type="number"
                value={userId}
                onChange={(event) => setUserId(event.target.value)}
              />
            </label>
            <button type="button" onClick={() => loadUser()}>
              <Search aria-hidden="true" size={18} />
              Load user
            </button>
          </div>
          {user ? (
            <dl className="profile-list">
              <div>
                <dt>Name</dt>
                <dd>{user.name}</dd>
              </div>
              <div>
                <dt>Email</dt>
                <dd>{user.email}</dd>
              </div>
            </dl>
          ) : null}
          {userError ? <p className="error-message">{userError}</p> : null}
        </div>

        <form className="panel payment-panel" onSubmit={chargePayment}>
          <div className="panel-heading">
            <h2>Payments</h2>
            <p>Exercise mocked charge and refund flows.</p>
          </div>
          <div className="payment-grid">
            <label>
              Amount in cents
              <input
                min="1"
                type="number"
                value={amountCents}
                onChange={(event) => setAmountCents(event.target.value)}
              />
            </label>
            <label>
              Currency
              <input
                maxLength={3}
                value={currency}
                onChange={(event) => setCurrency(event.target.value)}
              />
            </label>
          </div>
          <div className="button-row">
            <button type="submit">
              <CreditCard aria-hidden="true" size={18} />
              Charge
            </button>
            <button className="secondary-button" type="button" onClick={refundPayment}>
              <RotateCcw aria-hidden="true" size={18} />
              Refund
            </button>
          </div>
          {payment ? <p className="result-line">{`${payment.id} ${payment.status}`}</p> : null}
          {paymentError ? <p className="error-message">{paymentError}</p> : null}
        </form>

        <div className="panel audit-panel">
          <div className="panel-heading">
            <h2>Audit log</h2>
            <p>Calls the admin-only endpoint with an admin role header.</p>
          </div>
          <button type="button" onClick={loadAuditLog}>
            <ShieldCheck aria-hidden="true" size={18} />
            Load audit log
          </button>
          {auditError ? <p className="error-message">{auditError}</p> : null}
          <ul className="event-list">
            {events.map((event, index) => (
              <li key={`${event.event}-${index}`}>{event.event}</li>
            ))}
          </ul>
        </div>
      </section>
    </main>
  );
}

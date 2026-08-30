import {
  CloudSun,
  Wallet,
  PiggyBank,
  CreditCard,
  ShieldCheck,
  Plus,
} from "lucide-react";

function Dashboard() {
  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="logo">
          Flow<span>Pay</span>
        </div>

        <nav>
          <a className="active">Dashboard</a>
          <a>Income</a>
          <a>Savings</a>
          <a>Flex Credit</a>
          <a>Trust Score</a>
        </nav>

        <div className="sidebar-footer">
          Finance that moves
          <br />
          with your income.
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">GOOD MORNING</p>
            <h1>Your money, in your rhythm.</h1>
          </div>

          <button className="add-income-btn">
            <Plus size={18} />
            Add Income
          </button>
        </header>

        <section className="weather-card">
          <div className="weather-icon">
            <CloudSun size={38} />
          </div>

          <div>
            <p className="eyebrow">INCOME WEATHER</p>
            <h2>Stable</h2>
            <p>
              Your recent earnings are within your normal range.
              Current allocations can continue safely.
            </p>
          </div>

          <div className="forecast">
            <span>7-day expected income</span>
            <strong>₹5,400 – ₹6,300</strong>
          </div>
        </section>

        <section className="stats-grid">
          <StatCard
            icon={<Wallet size={22} />}
            label="Available"
            value="₹4,820"
            note="Safe to spend"
          />

          <StatCard
            icon={<PiggyBank size={22} />}
            label="Savings Pocket"
            value="₹2,640"
            note="+₹260 today"
          />

          <StatCard
            icon={<CreditCard size={22} />}
            label="Flex Credit"
            value="₹6,800"
            note="₹3,200 repaid"
          />

          <StatCard
            icon={<ShieldCheck size={22} />}
            label="Trust Score"
            value="72 / 100"
            note="+4 this month"
          />
        </section>

        <section className="dashboard-grid">
          <div className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">TODAY'S FLOW</p>
                <h3>₹1,800 received</h3>
              </div>

              <span className="status-pill">Stable</span>
            </div>

            <div className="allocation-list">
              <Allocation label="Available" amount="₹1,380" percent="77%" />
              <Allocation label="Savings" amount="₹260" percent="14%" />
              <Allocation label="Repayment" amount="₹160" percent="9%" />
            </div>

            <div className="explanation">
              <strong>Why this allocation?</strong>
              <p>
                Your earnings are currently stable, so FlowPay can continue
                normal savings and repayment contributions without putting
                essential liquidity at risk.
              </p>
            </div>
          </div>

          <div className="panel">
            <p className="eyebrow">FLOW ENGINE</p>
            <h3>Financial capacity</h3>

            <div className="engine-score">
              <span>Safe allocation capacity</span>
              <strong>82%</strong>
            </div>

            <div className="engine-bar">
              <div className="engine-fill" />
            </div>

            <ul className="engine-signals">
              <li>
                <span>Income volatility</span>
                <strong>Low</strong>
              </li>
              <li>
                <span>Emergency buffer</span>
                <strong>Healthy</strong>
              </li>
              <li>
                <span>Debt pressure</span>
                <strong>Moderate</strong>
              </li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  );
}

function StatCard({ icon, label, value, note }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>

      <div>
        <p>{label}</p>
        <h3>{value}</h3>
        <span>{note}</span>
      </div>
    </div>
  );
}

function Allocation({ label, amount, percent }) {
  return (
    <div className="allocation-row">
      <div>
        <strong>{label}</strong>
        <span>{percent}</span>
      </div>

      <strong>{amount}</strong>
    </div>
  );
}

export default Dashboard;

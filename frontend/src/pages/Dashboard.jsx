import {
  ArrowUpRight,
  CloudSun,
  CreditCard,
  Plus,
  ShieldCheck,
  Sparkles,
  Wallet,
} from "lucide-react";

import { motion } from "framer-motion";

const metrics = [
  {
    label: "Available",
    value: "₹4,820",
    note: "Safe to spend",
    icon: Wallet,
  },
  {
    label: "Savings Pocket",
    value: "₹2,640",
    note: "+₹260 today",
    icon: Sparkles,
  },
  {
    label: "Flex Credit",
    value: "₹6,800",
    note: "₹3,200 repaid",
    icon: CreditCard,
  },
  {
    label: "Trust Score",
    value: "72",
    note: "+4 this month",
    icon: ShieldCheck,
  },
];

function Dashboard() {
  return (
    <main className="dashboard-shell">
      <header className="dashboard-header">
        <div>
          <p className="dashboard-eyebrow">
            LIVE FINANCIAL STATE
          </p>

          <h1>
            Your money,
            <br />
            <span>in your rhythm.</span>
          </h1>

          <p className="dashboard-description">
            FlowPay reads your earning pattern and adapts how much
            you can safely spend, save, repay and protect.
          </p>
        </div>

        <motion.button
          className="add-income-button"
          whileHover={{
            y: -2,
          }}
          whileTap={{
            scale: 0.97,
          }}
        >
          <Plus size={18} />
          Add income
        </motion.button>
      </header>

      <section className="dashboard-hero-grid">
        <motion.div
          className="income-card"
          initial={{
            opacity: 0,
            y: 18,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.3,
          }}
          transition={{
            duration: 0.5,
          }}
        >
          <div className="income-card-header">
            <div>
              <p className="dashboard-eyebrow">
                TODAY'S FLOW
              </p>

              <h2>₹1,800 received</h2>
            </div>

            <div className="live-badge">
              <span />
              LIVE
            </div>
          </div>

          <div className="income-flow">
            <div className="flow-side">
              <span>Income</span>
              <strong>₹1,800</strong>
            </div>

            <div className="flow-line">
              <motion.div
                className="flow-line-fill"
                initial={{
                  width: 0,
                }}
                whileInView={{
                  width: "100%",
                }}
                viewport={{
                  once: true,
                }}
                transition={{
                  duration: 1.15,
                  ease: "easeInOut",
                }}
              />

              <motion.div
                className="flow-line-dot"
                initial={{
                  left: "0%",
                }}
                whileInView={{
                  left: "96%",
                }}
                viewport={{
                  once: true,
                }}
                transition={{
                  duration: 1.15,
                  ease: "easeInOut",
                }}
              />
            </div>

            <div className="flow-side flow-side-right">
              <span>Adapted safely</span>
              <strong>Stable</strong>
            </div>
          </div>

          <div className="allocation-grid">
            <AllocationCard
              label="Available"
              value="₹1,380"
              percent="77%"
              type="available"
            />

            <AllocationCard
              label="Save"
              value="₹260"
              percent="14%"
              type="save"
            />

            <AllocationCard
              label="Repay"
              value="₹160"
              percent="9%"
              type="repay"
            />

            <AllocationCard
              label="Protect"
              value="Active"
              percent="Buffer"
              type="protect"
            />
          </div>
        </motion.div>

        <motion.div
          className="weather-card"
          initial={{
            opacity: 0,
            y: 18,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.3,
          }}
          transition={{
            duration: 0.5,
            delay: 0.08,
          }}
        >
          <div className="weather-icon-wrap">
            <motion.div
              className="weather-icon"
              animate={{
                y: [0, -5, 0],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <CloudSun size={35} />
            </motion.div>

            <div className="weather-ring ring-one" />
            <div className="weather-ring ring-two" />
          </div>

          <p className="dashboard-eyebrow">
            INCOME WEATHER
          </p>

          <div className="weather-title">
            <h2>Stable</h2>
            <span />
          </div>

          <p className="weather-copy">
            Your recent earnings are tracking within your expected
            range.
          </p>

          <div className="weather-forecast">
            <span>Next 7 days</span>

            <strong>₹5.4k — ₹6.3k</strong>

            <small>
              Forecast confidence 86%
              <ArrowUpRight size={14} />
            </small>
          </div>
        </motion.div>
      </section>

      <section className="metric-grid">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;

          return (
            <motion.article
              key={metric.label}
              className="metric-card"
              initial={{
                opacity: 0,
                y: 18,
              }}
              whileInView={{
                opacity: 1,
                y: 0,
              }}
              viewport={{
                once: true,
                amount: 0.2,
              }}
              transition={{
                delay: index * 0.05,
              }}
              whileHover={{
                y: -5,
              }}
            >
              <div className="metric-icon">
                <Icon size={19} />
              </div>

              <span className="metric-label">
                {metric.label}
              </span>

              <strong className="metric-value">
                {metric.value}
              </strong>

              <span className="metric-note">
                {metric.note}
              </span>

              <div className="spark-bars">
                <i />
                <i />
                <i />
                <i />
                <i />
                <i />
              </div>
            </motion.article>
          );
        })}
      </section>
    </main>
  );
}

function AllocationCard({
  label,
  value,
  percent,
  type,
}) {
  return (
    <motion.div
      className={`allocation-card allocation-${type}`}
      whileHover={{
        y: -4,
      }}
    >
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{percent}</small>
    </motion.div>
  );
}

export default Dashboard;
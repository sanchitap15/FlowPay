import {
  ArrowDown,
  ArrowRight,
  Sparkles,
} from "lucide-react";

import { motion } from "framer-motion";

function Landing() {
  const scrollToDashboard = () => {
    document
      .getElementById("dashboard")
      ?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="landing-page">
      <div className="landing-glow landing-glow-one" />
      <div className="landing-glow landing-glow-two" />

      <nav className="landing-nav">
        <div className="landing-brand">
          <div className="brand-symbol">F</div>

          <span className="brand-text">
            Flow<span>Pay</span>
          </span>
        </div>

        <div className="landing-nav-links">
          <button onClick={scrollToDashboard}>Product</button>
          <button onClick={scrollToDashboard}>How it works</button>

          <button
            className="nav-launch"
            onClick={scrollToDashboard}
          >
            Open app
            <ArrowRight size={15} />
          </button>
        </div>
      </nav>

      <div className="landing-content">
        <motion.div
          className="landing-copy"
          initial={{
            opacity: 0,
            y: 24,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.65,
          }}
        >
          <motion.div
            className="landing-pill"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.25 }}
          >
            <Sparkles size={14} />
            Income-adaptive finance
          </motion.div>

          <h1>
            Finance that
            <br />
            follows your <span>flow.</span>
          </h1>

          <p className="landing-description">
            Your income doesn’t arrive on a fixed schedule.
            <br />
            Your finances shouldn’t have to either.
          </p>

          <p className="landing-subcopy">
            FlowPay adapts saving, repayment and protection around
            how you actually earn.
          </p>

          <div className="landing-actions">
            <motion.button
              className="landing-primary"
              onClick={scrollToDashboard}
              whileHover={{
                y: -3,
              }}
              whileTap={{
                scale: 0.98,
              }}
            >
              Enter FlowPay
              <ArrowRight size={18} />
            </motion.button>

            <button
              className="landing-secondary"
              onClick={scrollToDashboard}
            >
              See how it works
              <ArrowDown size={16} />
            </button>
          </div>
        </motion.div>

        <motion.div
          className="landing-visual"
          initial={{
            opacity: 0,
            x: 40,
          }}
          animate={{
            opacity: 1,
            x: 0,
          }}
          transition={{
            duration: 0.8,
            delay: 0.1,
          }}
        >
          <div className="preview-card">
            <div className="preview-heading">
              <div>
                <span>This week's income</span>
                <strong>₹8,460</strong>
              </div>

              <div className="preview-growth">
                +18.4%
              </div>
            </div>

            <div className="preview-chart">
              <svg
                viewBox="0 0 600 180"
                preserveAspectRatio="none"
              >
                <defs>
                  <linearGradient
                    id="previewLine"
                    x1="0%"
                    y1="0%"
                    x2="100%"
                    y2="0%"
                  >
                    <stop
                      offset="0%"
                      stopColor="#245c49"
                    />

                    <stop
                      offset="100%"
                      stopColor="#79b79b"
                    />
                  </linearGradient>

                  <linearGradient
                    id="previewArea"
                    x1="0%"
                    y1="0%"
                    x2="0%"
                    y2="100%"
                  >
                    <stop
                      offset="0%"
                      stopColor="#9ccab4"
                      stopOpacity="0.32"
                    />

                    <stop
                      offset="100%"
                      stopColor="#9ccab4"
                      stopOpacity="0"
                    />
                  </linearGradient>
                </defs>

                <motion.path
                  d="M0 145 C60 138 90 104 140 118 C195 130 215 77 270 89 C330 102 350 55 415 66 C470 76 495 45 540 51 C570 55 585 35 600 27 L600 180 L0 180 Z"
                  fill="url(#previewArea)"
                  initial={{
                    opacity: 0,
                  }}
                  animate={{
                    opacity: 1,
                  }}
                  transition={{
                    delay: 0.6,
                  }}
                />

                <motion.path
                  d="M0 145 C60 138 90 104 140 118 C195 130 215 77 270 89 C330 102 350 55 415 66 C470 76 495 45 540 51 C570 55 585 35 600 27"
                  fill="none"
                  stroke="url(#previewLine)"
                  strokeWidth="4"
                  strokeLinecap="round"
                  initial={{
                    pathLength: 0,
                  }}
                  animate={{
                    pathLength: 1,
                  }}
                  transition={{
                    duration: 1.5,
                    delay: 0.25,
                    ease: "easeInOut",
                  }}
                />
              </svg>
            </div>

            <div className="preview-bottom">
              <div>
                <span>Income weather</span>

                <strong className="preview-stable">
                  <i />
                  Stable
                </strong>
              </div>

              <div>
                <span>Next 7 days</span>
                <strong>₹5.4k — ₹6.3k</strong>
              </div>
            </div>
          </div>

          <motion.div
            className="floating-save"
            animate={{
              y: [0, -8, 0],
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          >
            <span>Saved automatically</span>
            <strong>₹260</strong>
            <small>Based on today’s capacity</small>
          </motion.div>

          <motion.div
            className="floating-trust"
            animate={{
              y: [0, 7, 0],
            }}
            transition={{
              duration: 5.8,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          >
            <div className="trust-ring">
              <span>72</span>
            </div>

            <div>
              <span>Trust Score</span>
              <strong>Building steadily</strong>
            </div>
          </motion.div>
        </motion.div>
      </div>

      <button
        className="landing-scroll"
        onClick={scrollToDashboard}
      >
        Explore FlowPay
        <ArrowDown size={15} />
      </button>
    </section>
  );
}

export default Landing;
import "./App.css";

import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div className="app">
      <Landing />

      <section id="dashboard">
        <Dashboard />
      </section>
    </div>
  );
}

export default App;
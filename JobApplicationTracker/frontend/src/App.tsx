import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { ThemeToggle } from './components/ThemeToggle';
import { DashboardPage } from './pages/DashboardPage';
import { AddJobPage } from './pages/AddJobPage';
import { JobsListPage } from './pages/JobsListPage';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <div className="app">
          <header className="app-header">
            <nav className="nav">
              <Link to="/" className="nav-brand">
                Job Tracker
              </Link>
              <div className="nav-right">
                <ul className="nav-links">
                  <li>
                    <Link to="/">Dashboard</Link>
                  </li>
                  <li>
                    <Link to="/jobs">My Applications</Link>
                  </li>
                  <li>
                    <Link to="/add-job">Add Job</Link>
                  </li>
                </ul>
                <ThemeToggle />
              </div>
            </nav>
          </header>
          <main className="app-main">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/add-job" element={<AddJobPage />} />
              <Route path="/jobs" element={<JobsListPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;

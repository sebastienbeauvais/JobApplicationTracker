import { Link } from 'react-router-dom';
import { useDashboard } from '../hooks/useDashboard';
import { JobStatus } from '../types/job';

const STATUS_LABELS: Record<JobStatus, string> = {
  applied: 'Applied',
  interviewing: 'Interviewing',
  offer_received: 'Offer Received',
  accepted: 'Accepted',
  rejected: 'Rejected',
  withdrawn: 'Withdrawn',
};

const STATUS_COLORS: Record<JobStatus, string> = {
  applied: '#3b82f6',
  interviewing: '#f59e0b',
  offer_received: '#8b5cf6',
  accepted: '#10b981',
  rejected: '#ef4444',
  withdrawn: '#6b7280',
};

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
}

export function DashboardPage() {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return (
      <div className="page dashboard-page">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page dashboard-page">
        <div className="alert alert-error">{error}</div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const maxCount = Math.max(...data.applications_over_time.map((d) => d.count), 1);

  return (
    <div className="page dashboard-page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <Link to="/add-job" className="btn btn-primary">
          + Add New Application
        </Link>
      </div>

      <div className="dashboard-grid">
        {/* Total Applications Card */}
        <div className="dashboard-card card-total">
          <h3 className="card-title">Total Applications</h3>
          <div className="card-value">{data.total_applications}</div>
        </div>

        {/* Interview Rate Card */}
        <div className="dashboard-card card-rate">
          <h3 className="card-title">Interview Rate</h3>
          <div className="card-value">{data.interview_rate.toFixed(1)}%</div>
          <p className="card-subtitle">of applications led to interviews</p>
        </div>

        {/* Applications by Status */}
        <div className="dashboard-card card-status">
          <h3 className="card-title">Applications by Status</h3>
          <div className="status-bars">
            {data.applications_by_status.map((item) => (
              <div key={item.status} className="status-bar-item">
                <div className="status-bar-label">
                  <span>{STATUS_LABELS[item.status]}</span>
                  <span className="status-count">{item.count}</span>
                </div>
                <div className="status-bar-track">
                  <div
                    className="status-bar-fill"
                    style={{
                      width: `${data.total_applications > 0 ? (item.count / data.total_applications) * 100 : 0}%`,
                      backgroundColor: STATUS_COLORS[item.status],
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Applications Over Time */}
        <div className="dashboard-card card-timeline">
          <h3 className="card-title">Applications Over Time (Last 30 Days)</h3>
          <div className="timeline-chart">
            {data.applications_over_time.map((item, index) => (
              <div
                key={item.date}
                className="timeline-bar"
                style={{
                  height: `${(item.count / maxCount) * 100}%`,
                }}
                title={`${formatDate(item.date)}: ${item.count} application${item.count !== 1 ? 's' : ''}`}
              />
            ))}
          </div>
          <div className="timeline-labels">
            <span>{formatDate(data.applications_over_time[0]?.date || '')}</span>
            <span>Today</span>
          </div>
        </div>

        {/* Recent Applications */}
        <div className="dashboard-card card-recent">
          <div className="card-header">
            <h3 className="card-title">Recent Applications</h3>
            <Link to="/jobs" className="link">
              View All
            </Link>
          </div>
          {data.recent_applications.length === 0 ? (
            <p className="empty-message">No applications yet</p>
          ) : (
            <ul className="recent-list">
              {data.recent_applications.slice(0, 5).map((app) => (
                <li key={app.id} className="recent-item">
                  <div className="recent-info">
                    <span className="recent-title">{app.job_title}</span>
                    <span className="recent-company">{app.company}</span>
                  </div>
                  <div className="recent-meta">
                    <span
                      className="status-badge"
                      style={{ backgroundColor: STATUS_COLORS[app.status] }}
                    >
                      {STATUS_LABELS[app.status]}
                    </span>
                    <span className="recent-date">
                      {formatDate(app.application_date)}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

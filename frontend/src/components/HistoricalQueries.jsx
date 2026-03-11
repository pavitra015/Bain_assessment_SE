import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './HistoricalQueries.css';

const HistoricalQueries = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get('/history');
      setHistory(response.data || []);
    } catch (err) {
      if (err.response?.status === 404) {
        setHistory([]);
      } else {
        setError('Failed to load historical queries. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDistance = (value) => {
    return value ? value.toFixed(2) : '0.00';
  };

  const handleBackToCalculator = () => {
    navigate('/');
  };

  return (
    <div className="historical-queries">
      <div className="history-header">
        <div>
          <h1>Distance Calculator</h1>
          <p className="subtitle">
            Prototype web application for calculating the distance between addresses.
          </p>
        </div>
        <button className="back-button" onClick={handleBackToCalculator}>
          <span>Back to Calculator</span>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M3 3h14a1 1 0 011 1v12a1 1 0 01-1 1H3a1 1 0 01-1-1V4a1 1 0 011-1zm1 2v10h12V5H4zm2 2h8v2H6V7zm0 4h5v2H6v-2z"/>
          </svg>
        </button>
      </div>

      <div className="history-content">
        <div className="history-section-header">
          <h2>Historical Queries</h2>
          <p className="section-subtitle">History of the user's queries.</p>
        </div>

        {loading ? (
          <div className="loading-message">Loading historical queries...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : history.length === 0 ? (
          <div className="empty-message">No historical queries found. Start by calculating some distances!</div>
        ) : (
          <div className="history-table-container">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Source Address</th>
                  <th>Destination Address</th>
                  <th>Distance in Miles</th>
                  <th>Distance in Kilometers</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id}>
                    <td>{item.source_address}</td>
                    <td>{item.destination_address}</td>
                    <td>{formatDistance(item.distance_in_miles)}</td>
                    <td>{formatDistance(item.distance_in_kms)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoricalQueries;

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './DistanceCalculator.css';

const DistanceCalculator = () => {
  const navigate = useNavigate();
  const [sourceAddress, setSourceAddress] = useState('');
  const [destinationAddress, setDestinationAddress] = useState('');
  const [unit, setUnit] = useState('miles');
  const [distance, setDistance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCalculateDistance = async () => {
    if (!sourceAddress.trim() || !destinationAddress.trim()) {
      setError('Please enter both source and destination addresses');
      return;
    }

    setLoading(true);
    setError('');
    setDistance(null);

    try {
      const response = await axios.post('/distance', {
        source_address: sourceAddress,
        destination_address: destinationAddress,
      });

      console.log('Backend response:', response.data);

      setDistance({
        miles: response.data.distance_in_miles || 0,
        kilometers: response.data.distance_in_kms || 0,
      });
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Failed to calculate distance. Please check the addresses and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleUnitChange = (newUnit) => {
    setUnit(newUnit);
  };

  const formatDistance = (value) => {
    return value ? value.toFixed(2) : '0.00';
  };

  const handleViewHistory = () => {
    navigate('/history');
  };

  return (
    <div className="distance-calculator">
      <div className="calculator-header">
        <div>
          <h1>Distance Calculator</h1>
          <p className="subtitle">
            Prototype web application for calculating the distance between addresses.
          </p>
        </div>
        <button className="history-button" onClick={handleViewHistory}>
          <span>View Historical Queries</span>
        </button>
      </div>

      <div className="calculator-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="source">Source Address</label>
            <input
              id="source"
              type="text"
              placeholder="Input address"
              value={sourceAddress}
              onChange={(e) => setSourceAddress(e.target.value)}
              className="address-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="destination">Destination Address</label>
            <input
              id="destination"
              type="text"
              placeholder="Input address"
              value={destinationAddress}
              onChange={(e) => setDestinationAddress(e.target.value)}
              className="address-input"
            />
          </div>

          <div className="form-group unit-group">
            <label>Unit</label>
            <div className="radio-group">
              <label className="radio-label">
                <input
                  type="radio"
                  name="unit"
                  value="miles"
                  checked={unit === 'miles'}
                  onChange={() => handleUnitChange('miles')}
                />
                <span>Miles</span>
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  name="unit"
                  value="kilometers"
                  checked={unit === 'kilometers'}
                  onChange={() => handleUnitChange('kilometers')}
                />
                <span>Kilometers</span>
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  name="unit"
                  value="both"
                  checked={unit === 'both'}
                  onChange={() => handleUnitChange('both')}
                />
                <span>Both</span>
              </label>
            </div>
          </div>

          <div className="form-group distance-group">
            <label>Distance</label>
            <div className="distance-display">
              {distance && (
                <>
                  {(unit === 'miles' || unit === 'both') && (
                    <div className="distance-value">
                      <span className="value">{formatDistance(distance.miles)}</span>
                      <span className="unit-label">mi</span>
                    </div>
                  )}
                  {(unit === 'kilometers' || unit === 'both') && (
                    <div className="distance-value">
                      <span className="value">{formatDistance(distance.kilometers)}</span>
                      <span className="unit-label">km</span>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>

        <button
          className="calculate-button"
          onClick={handleCalculateDistance}
          disabled={loading}
        >
          <span>{loading ? 'Calculating...' : 'Calculate Distance'}</span>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M3 3h14a1 1 0 011 1v12a1 1 0 01-1 1H3a1 1 0 01-1-1V4a1 1 0 011-1zm1 2v10h12V5H4zm2 2h8v2H6V7zm0 4h5v2H6v-2z"/>
          </svg>
        </button>

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default DistanceCalculator;

import pytest
from unittest.mock import patch, MagicMock
from geopy.exc import GeocoderTimedOut


@pytest.fixture
def mock_coordinates():
    """Fixture for mock coordinate data."""
    mock_source = MagicMock()
    mock_source.latitude = 40.7127281
    mock_source.longitude = -74.0060152
    
    mock_destination = MagicMock()
    mock_destination.latitude = 42.3554334
    mock_destination.longitude = -71.060511
    
    return mock_source, mock_destination


@pytest.fixture
def distance_request_data():
    """Fixture for distance request payload."""
    return {
        "source_address": "New York, NY",
        "destination_address": "Boston, MA"
    }


def mock_geocode_success(mock_source, mock_destination):
    """Helper to mock successful geocoding."""
    mock_locator = MagicMock()
    mock_locator.geocode.side_effect = [mock_source, mock_destination]
    return mock_locator


class TestDistanceEndpoint:
    """Test cases for the /distance endpoint."""
    
    def test_distance_calculation_success(self, client, mock_coordinates, distance_request_data):
        """Test 1: Successful distance calculation."""
        mock_source, mock_destination = mock_coordinates
        
        with patch('backend.router.distance.Nominatim') as mock_nominatim:
            mock_nominatim.return_value = mock_geocode_success(mock_source, mock_destination)
            response = client.post("/distance", json=distance_request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "distance_in_kms" in data
        assert "distance_in_miles" in data
    
    def test_distance_calculation_failure(self, client, distance_request_data):
        """Test 2: Distance calculation failure (invalid address or timeout)."""
        with patch('backend.router.distance.Nominatim') as mock_nominatim:
            mock_locator = MagicMock()
            mock_locator.geocode.side_effect = GeocoderTimedOut("Service timed out")
            mock_nominatim.return_value = mock_locator
            
            response = client.post("/distance", json=distance_request_data)
        
        assert response.status_code == 408
        assert "Unable to process your request" in response.json()["detail"]
    
    def test_database_add_success(self, client, db_session, mock_coordinates, distance_request_data):
        """Test 3: Successful database save after distance calculation."""
        from backend.models.history import History
        
        mock_source, mock_destination = mock_coordinates
        
        with patch('backend.router.distance.Nominatim') as mock_nominatim:
            mock_nominatim.return_value = mock_geocode_success(mock_source, mock_destination)
            response = client.post("/distance", json=distance_request_data)
        
        assert response.status_code == 200
        
        # Verify record was saved to database
        history_count = db_session.query(History).count()
        assert history_count == 1
        
        saved_record = db_session.query(History).first()
        assert saved_record.source_address == distance_request_data["source_address"]
        assert saved_record.destination_address == distance_request_data["destination_address"]
    
    def test_database_add_failure(self, client, db_session, mock_coordinates, distance_request_data):
        """Test 4: Database save failure handling."""
        mock_source, mock_destination = mock_coordinates
        
        with patch('backend.router.distance.Nominatim') as mock_nominatim:
            mock_nominatim.return_value = mock_geocode_success(mock_source, mock_destination)
            
            # Mock database commit to raise an exception
            with patch.object(db_session, 'commit', side_effect=Exception("Database error")):
                response = client.post("/distance", json=distance_request_data)
        
        assert response.status_code == 500
        assert "Failed to save calculation to database" in response.json()["detail"]

import pytest
from unittest.mock import patch


class TestHistoryEndpoint:
    """Test cases for the /history endpoint."""
    
    def test_history_empty(self, client):
        """Test 5: Empty history - no records in database."""
        response = client.get("/history")
        
        assert response.status_code == 404
        assert "No history found" in response.json()["detail"]
    
    def test_history_database_fetch_issue(self, client, db_session):
        """Test 6: Database connection/fetch issue."""
        # Mock the database query to raise an exception
        with patch.object(db_session, 'query', side_effect=Exception("Database connection error")):
            response = client.get("/history")
        
        assert response.status_code == 500
        assert "Failed to retrieve history" in response.json()["detail"]

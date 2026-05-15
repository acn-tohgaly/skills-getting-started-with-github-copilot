"""
Tests for GET /activities endpoint
AAA Pattern: Arrange - Act - Assert
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all 9 activities"""
    # Arrange
    expected_activity_count = 9
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count


def test_get_activities_returns_correct_structure(client):
    """Test that activities have correct structure with all required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in data.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_contains_chess_club(client):
    """Test that activities include Chess Club with initial participants"""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == expected_chess_participants
    assert data["Chess Club"]["max_participants"] == 12


def test_get_activities_participant_count_matches_length(client):
    """Test that availability calculation would be correct (max - current length)"""
    # Arrange
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_data in data.items():
        current_count = len(activity_data["participants"])
        max_capacity = activity_data["max_participants"]
        assert current_count <= max_capacity

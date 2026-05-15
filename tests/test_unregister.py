"""
Tests for POST /activities/{activity_name}/unregister endpoint
AAA Pattern: Arrange - Act - Assert
"""
import pytest


def test_unregister_successful_for_signed_up_participant(client):
    """Test successful unregistration of a signed-up participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes the participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert email not in data[activity_name]["participants"]


def test_unregister_fails_for_nonexistent_activity(client):
    """Test unregister fails with 404 for non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_not_signed_up_participant(client):
    """Test unregister fails with 400 when student not signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"  # Not in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_frees_up_spot_for_new_signup(client):
    """Test that unregistering frees up a spot for new signups"""
    # Arrange
    activity_name = "Chess Club"
    original_participant = "michael@mergington.edu"
    new_participant = "newstudent@mergington.edu"
    
    # Act - Unregister original participant
    client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": original_participant}
    )
    
    # Then sign up new participant
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_participant}
    )
    
    # Assert
    assert response.status_code == 200
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert new_participant in data[activity_name]["participants"]
    assert original_participant not in data[activity_name]["participants"]


def test_unregister_then_re_signup_same_participant(client):
    """Test that a participant can unregister and re-signup"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act - Unregister
    client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Then re-signup
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert email in data[activity_name]["participants"]

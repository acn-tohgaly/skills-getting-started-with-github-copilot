"""
Shared pytest fixtures for all tests.
Provides a fresh app and client with reset state for each test.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Team-based basketball training and league play",
            "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Outdoor soccer practices and friendly matches",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Society": {
            "description": "Acting workshops, stage production, and performance practice",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 16,
            "participants": ["zara@mergington.edu", "oliver@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Advanced problem solving and mathematical competition prep",
            "schedule": "Wednesdays, 4:30 PM - 6:00 PM",
            "max_participants": 12,
            "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking, research, and debate tournaments",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["olivia@mergington.edu", "william@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client(reset_activities):
    """Provide a TestClient with fresh app state"""
    return TestClient(app)

from fastapi.testclient import TestClient
from src.app import app
import pytest

client = TestClient(app)

# Test root redirect
def test_root_redirect():
    # Arrange: TestClient is set up
    # Act: Make GET request to root
    response = client.get("/")
    # Assert: Should redirect to /static/index.html
    assert response.status_code in (200, 307, 308)
    assert "/static/index.html" in response.headers.get("location", "") or str(response.url).endswith("/static/index.html")

# Test activities listing
def test_get_activities():
    # Arrange: TestClient is set up
    # Act: Make GET request to /activities
    response = client.get("/activities")
    # Assert: Should return dict of activities
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()

# Test signup for activity
def test_signup_for_activity():
    # Arrange: Choose activity and email
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act: Sign up user
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert: Should succeed
    assert response.status_code == 200
    assert f"Signed up" in response.json()["message"]
    # Act: Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert: Should fail with 400
    assert response_dup.status_code == 400

# Test unregister from activity
def test_unregister_from_activity():
    # Arrange: Choose activity and email
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act: Unregister user
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert: Should succeed
    assert response.status_code == 200
    assert email in response.json()["message"]
    # Act: Try unregistering again
    response_dup = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert: Should fail with 404
    assert response_dup.status_code == 404

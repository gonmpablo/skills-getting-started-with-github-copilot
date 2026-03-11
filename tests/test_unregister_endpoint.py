from urllib.parse import quote


def unregister(client, activity_name, email):
    encoded_activity = quote(activity_name, safe="")
    return client.delete(f"/activities/{encoded_activity}/signup", params={"email": email})


def test_unregister_removes_existing_participant(client):
    email = "michael@mergington.edu"

    response = unregister(client, "Chess Club", email)

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = unregister(client, "Unknown Club", "student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_student_not_registered(client):
    response = unregister(client, "Chess Club", "not.registered@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"

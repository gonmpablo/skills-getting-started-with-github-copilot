def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200

    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities

    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_sets_no_store_cache_header(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers.get("cache-control") == "no-store"


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"

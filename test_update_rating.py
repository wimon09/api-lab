import pytest


# Boundary values just outside the valid range are refused without changing the rating.
@pytest.mark.parametrize(
    ("stars", "expected_status"),
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_rating_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    before = api.get(path, headers=auth)
    assert before.status_code == 200
    old_stars = before.json()["stars"]

    res = api.put(path, json={"stars": stars}, headers=auth)

    assert res.status_code == expected_status
    current = api.get(path, headers=auth)
    assert current.status_code == 200
    assert current.json()["stars"] == (stars if expected_status == 200 else old_stars)

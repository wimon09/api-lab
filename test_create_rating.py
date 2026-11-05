import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, a real pizza and the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: values below 1 and above 5 are refused.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: a decimal value is refused with a type error.
def test_decimal_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
    }


# C2: text is refused where the API requires a whole number.
def test_text_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal string into Go struct field Rating.stars of type int"
    }


# C2: omitting stars is refused by the rating range rule.
def test_missing_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a pizza ID that does not exist is refused.
def test_pizza_does_not_exist(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: a request without an authorization token is refused.
def test_missing_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}

    res = api.post("/api/ratings", json=new)

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# C4: a token with the wrong length is refused.
def test_short_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    headers = {"Authorization": "token short"}

    res = api.post("/api/ratings", json=new, headers=headers)

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

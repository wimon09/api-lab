# Another user cannot read a rating, and the owner can still read it unchanged.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.get(path, headers=other_auth)

    assert 400 <= res.status_code < 500
    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


# Another user cannot change a rating, and the owner's rating stays unchanged.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.put(path, json={"stars": 4}, headers=other_auth)

    assert 400 <= res.status_code < 500
    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating


# Another user cannot delete a rating, and the owner can still read it.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.delete(path, headers=other_auth)

    assert 400 <= res.status_code < 500
    owner_read = api.get(path, headers=auth)
    assert owner_read.status_code == 200
    assert owner_read.json() == rating

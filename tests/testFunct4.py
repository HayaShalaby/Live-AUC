def test_get_friends():
    # Arrange
    test_email = "testuser@example.com"
    expected_friends = ["friend1@example.com", "friend2@example.com", "friend3@example.com"]

    # Act
    response = app.test_client().get(f'/api/user/friends/{test_email}')
    friends_list = response.get_json()

    # Assert
    assert response.status_code == 200
    assert friends_list == expected_friends

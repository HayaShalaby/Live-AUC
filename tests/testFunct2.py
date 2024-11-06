def test_load_profile_info():
    # Arrange
    test_email = "testuser@example.com"
    expected_profile = {
        "username": "testuser",
        "pfp": "default.jpg",
        "points": "100",
        "friends": "5",
        "following": "10"
    }
    
    # Act
    response = app.test_client().get(f'/api/user/profile/{test_email}')
    profile_info = response.get_json()

    # Assert
    assert response.status_code == 200
    assert profile_info == expected_profile

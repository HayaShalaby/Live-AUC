def test_follow_user():
    # Arrange
    follower_email = "follower@example.com"
    followee_email = "followee@example.com"
    expected_response = {"message": "Successfully followed"}

    # Act
    response = app.test_client().post(f'/api/user/follow/{follower_email}/{followee_email}')
    response_data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_data == expected_response

def test_get_user_points():
    # Arrange
    test_email = "testuser@example.com"
    expected_points = 100

    # Act
    response = app.test_client().get(f'/api/user/points/{test_email}')
    points_data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert points_data['points'] == expected_points

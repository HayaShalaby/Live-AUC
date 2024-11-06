def test_add_username():
    # Arrange
    test_email = "testuser@example.com"
    expected_response = {"message": "Record inserted successfully"}
    
    # Act
    response = app.test_client().get(f'/api/user/{test_email}')
    response_data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_data == expected_response

def test_close_connection():
    # Arrange & Act
    close_connection()

    # Assert
    assert cursor.closed is True
    assert connection.closed is True

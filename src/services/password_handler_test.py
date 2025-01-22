import pytest
from src.services.password_handler import PasswordHandler

class TestPasswordHandler:
    def setup_method(self):
        self.password_handler = PasswordHandler()
        self.test_password = "test_password123"

    def test_hash_password_success(self):
        # Act
        hashed = self.password_handler.hash_password(self.test_password)
        
        # Assert
        assert hashed != self.test_password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_success(self):
        # Arrange
        hashed = self.password_handler.hash_password(self.test_password)
        
        # Act
        is_valid = self.password_handler.verify_password(self.test_password, hashed)
        
        # Assert
        assert is_valid is True

    def test_verify_password_failure(self):
        # Arrange
        hashed = self.password_handler.hash_password(self.test_password)
        wrong_password = "wrong_password123"
        
        # Act
        is_valid = self.password_handler.verify_password(wrong_password, hashed)
        
        # Assert
        assert is_valid is False 
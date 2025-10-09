import unittest
import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.validation import validate_email, validate_phone_us, validate_name_length


class TestValidationUtils(unittest.TestCase):
    """Test cases for validation utility functions."""
    
    def test_validate_email_valid(self):
        """Test valid email formats."""
        valid_emails = [
            "user@example.com",
            "test.email@domain.co.uk", 
            "user+tag@example.org",
            "firstname.lastname@company.com",
            "user123@test-domain.net"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email))
    
    def test_validate_email_invalid(self):
        """Test invalid email formats."""
        invalid_emails = [
            "",
            "invalid",
            "@example.com",
            "user@",
            "user space@example.com",
            "user@.com",
            "user@domain.",
            None,
            123
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email))
    
    def test_validate_phone_us_valid(self):
        """Test valid US phone number formats."""
        valid_phones = [
            "(555) 123-4567",
            "(555)123-4567", 
            "555-123-4567",
            "555.123.4567",
            "5551234567",
            "(123) 456-7890",
            "123.456.7890"
        ]
        
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertTrue(validate_phone_us(phone))
    
    def test_validate_phone_us_invalid(self):
        """Test invalid US phone number formats."""
        invalid_phones = [
            "",
            "123",
            "555-123-456",  # Too short
            "555-123-45678",  # Too long
            "(555) 123-456",  # Too short
            "555 123 4567 8",  # Too long
            "abc-def-ghij",  # Non-numeric
            "+1-555-123-4567",  # International format
            None,
            123
        ]
        
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertFalse(validate_phone_us(phone))
    
    def test_validate_name_length_valid(self):
        """Test valid name lengths."""
        valid_names = [
            "Jo",  # Minimum length
            "John",
            "John Doe",
            "A" * 50,  # Maximum length
            "Mary-Jane Smith-Jones"
        ]
        
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(validate_name_length(name))
    
    def test_validate_name_length_invalid(self):
        """Test invalid name lengths."""
        invalid_names = [
            "",  # Empty
            " ",  # Whitespace only
            "J",  # Too short
            "A" * 51,  # Too long
            None,
            123
        ]
        
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(validate_name_length(name))
    
    def test_validate_name_length_custom_limits(self):
        """Test name validation with custom length limits."""
        # Test with custom min/max
        self.assertTrue(validate_name_length("John", min_length=3, max_length=10))
        self.assertFalse(validate_name_length("Jo", min_length=3, max_length=10))
        self.assertFalse(validate_name_length("VeryLongName", min_length=3, max_length=10))


if __name__ == '__main__':
    unittest.main()
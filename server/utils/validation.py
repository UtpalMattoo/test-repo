import re


def validate_email(email: str) -> bool:
    """
    Validate email format using regex pattern.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email validation regex
    # Matches: user@domain.com, user.name@domain.co.uk, etc.
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(email_pattern, email))


def validate_phone_us(phone: str) -> bool:
    """
    Validate US phone number format.
    
    Accepts formats:
    - (555) 123-4567
    - 555-123-4567
    - 555.123.4567
    - 5551234567
    
    Args:
        phone: Phone number to validate
        
    Returns:
        bool: True if phone format is valid US format, False otherwise
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove all non-digit characters for length check
    digits_only = re.sub(r'\D', '', phone)
    
    # Must have exactly 10 digits for US phone numbers
    if len(digits_only) != 10:
        return False
    
    # US phone number patterns
    patterns = [
        r'^\(\d{3}\)\s?\d{3}[-.]?\d{4}$',  # (555) 123-4567 or (555)123-4567
        r'^\d{3}[-.]?\d{3}[-.]?\d{4}$',    # 555-123-4567 or 555.123.4567
        r'^\d{10}$'                        # 5551234567
    ]
    
    for pattern in patterns:
        if re.match(pattern, phone):
            return True
    
    return False


def validate_name_length(name: str, min_length: int = 2, max_length: int = 50) -> bool:
    """
    Validate name length requirements.
    
    Args:
        name: Name to validate
        min_length: Minimum required length (default: 2)
        max_length: Maximum allowed length (default: 50)
        
    Returns:
        bool: True if name length is valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    name = name.strip()
    return min_length <= len(name) <= max_length
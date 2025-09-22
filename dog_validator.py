class InvalidDogAgeError(Exception):
    """Custom exception for invalid dog age"""
    pass

def validate_dog_age(age):
    """
    Validates if the given dog age is between 0 and 20.
    
    Args:
        age: A number representing dog's age
        
    Raises:
        InvalidDogAgeError: If age is not between 0 and 20
        ValueError: If age is not a valid number
    """
    try:
        age_float = float(age)
        if not (0 <= age_float <= 20):
            raise InvalidDogAgeError(f"Dog age must be between 0 and 20. Got: {age}")
        return age_float
    except ValueError:
        raise ValueError(f"Age must be a valid number. Got: {age}")

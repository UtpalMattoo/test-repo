from typing import Union, NoReturn

class InvalidDogAgeError(ValueError):
    """Custom exception for invalid dog age."""
    pass

def validate_dog_age(age: Union[int, float]) -> Union[float, NoReturn]:
    """
    Validates if the dog's age is within acceptable range (0-20 years).
    
    Args:
        age: The age to validate in years
        
    Returns:
        The validated age if valid
        
    Raises:
        InvalidDogAgeError: If age is outside the valid range
    """
    try:
        age_float = float(age)
        if not 0 <= age_float <= 20:
            raise InvalidDogAgeError(f"Dog age must be between 0 and 20 years. Got: {age_float}")
        return age_float
    except (TypeError, ValueError):
        raise InvalidDogAgeError(f"Dog age must be a valid number. Got: {age}")

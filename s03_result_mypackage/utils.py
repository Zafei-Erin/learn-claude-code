"""
Utility functions for mypackage.
"""


def greet(name: str) -> str:
    """
    Return a greeting message for the given name.
    
    Args:
        name: The name to greet
        
    Returns:
        A greeting string
    """
    return f"Hello, {name}!"


def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


def capitalize_words(text: str) -> str:
    """
    Capitalize the first letter of each word in the given text.
    
    Args:
        text: The input string
        
    Returns:
        String with each word capitalized
    """
    return " ".join(word.capitalize() for word in text.split())


def reverse_string(text: str) -> str:
    """
    Reverse the given string.
    
    Args:
        text: The input string
        
    Returns:
        The reversed string
    """
    return text[::-1]

class PromptAlreadyExistsException(Exception):
    """Exception raised when a prompt with the same name already exists."""
    def __init__(self, message=f"Prompt already exists."):
        self.message = message  
        super()._init__(self.message)

class PromptNotFoundException(Exception):
    "Exception raised when a prompt is not found."""
    def __init__(self, message="Prompt not found."):
        self.message = message
        super()._init_(self.message)

class MissingKeyException(Exception):
    def __init__(self, message):
        super()._init__(message)
        self.message = message
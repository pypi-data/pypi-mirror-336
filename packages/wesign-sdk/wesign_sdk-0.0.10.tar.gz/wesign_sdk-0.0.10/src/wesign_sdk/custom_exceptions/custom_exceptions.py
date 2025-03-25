#custom_exception.py

class InvalidPathError(Exception):
    """Exception raised for invalid absolute paths."""
    def __init__(self, path, message="Provided path is not valid"):
        self.path = path
        self.message = message
        super().__init__(f"{message}: {path}")
        
class InvalidAPIKeyError(Exception):
    """Exception raised for an invalid API key."""
    def __init__(self, message="Invalid API key: The provided API key is not valid."):
        self.message = message
        super().__init__(self.message)


class FileUploadingError(Exception):
    """Exception raised for an uploading file."""
    def __init__(self, message="Error during uploading file."):
        self.message = message
        super().__init__(self.message)
        
class EnvelopeSendingError(Exception):
    """Exception raised for an uploading file."""
    def __init__(self, message="Error during sending envelope."):
        self.message = message
        super().__init__(self.message)


class InvalidRecipientStructureError(Exception):
    """Exception raised when an action is required by the recipient"""
    def __init__(self, message="Invalid Recipient Structure : The provided recipient structure is not valid"):
        self.message = message
        super().__init__(self.message)
        
class InvalidHostError(Exception):
    """Exception raised for an invalid host"""
    def __init__(self, message="Invalid Host error : The provided Host is not valid"):
        self.message = message
        super().__init__(self.message)
        
class InvalidFontFamilyError(Exception):
    """Exception raised for an invalid font family"""
    def __init__(self, message="Invalid Font Family : The provided font family is available at this moment."):
        self.message = message
        super().__init__(self.message)
        
class InvalidDropDownOptions(Exception):
    """Exception raised for an invalid dropdown options."""
    def __init__(self, message="Invalid Dropdown options : The provided dropdown header and title is invalid."):
        self.message = message
        super().__init__(self.message)
        
class InvalidEnvelopeError(Exception):
    """Exception raised for an invalid envelope id."""
    def __init__(self, message="Invalid Envelope ID"):
        self.message = message
        super().__init__(self.message)
        
if __name__ == "__main__":
    # Code to execute if run as a script
    print("Running as a script")
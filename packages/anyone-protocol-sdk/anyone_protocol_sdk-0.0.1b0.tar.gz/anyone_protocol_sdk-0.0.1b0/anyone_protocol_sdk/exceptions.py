class AnonError(Exception):
    """
    Base exception for all errors in the Anyone Protocol SDK.
    """
    def __init__(self, message, *args):
        super().__init__(message, *args)


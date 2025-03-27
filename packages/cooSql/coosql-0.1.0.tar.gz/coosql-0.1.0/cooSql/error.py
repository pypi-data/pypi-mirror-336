class Error(Exception):
    """Base error class for cooSql"""
    pass

class ParseError(Error):
    """Error raised when parsing fails"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"parse error {message}")

class InternalError(Error):
    """Error raised for internal errors"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"internal error {message}")

class WriteConflictError(Error):
    """Error raised when there's a write conflict"""
    def __init__(self):
        super().__init__("write conflict, try transaction")
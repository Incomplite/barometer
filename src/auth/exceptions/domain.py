class InvalidTokenError(Exception):
    def __init__(self):
        super().__init__("Invalid token")


class TokenExpiredError(Exception):
    def __init__(self):
        super().__init__("Token expires")

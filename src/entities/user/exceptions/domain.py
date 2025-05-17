class UserAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("User already exists")


class UserNotFoundError(Exception):
    def __init__(self):
        super().__init__("User not found")


class InvalidInputError(Exception):
    def __init__(self):
        super().__init__("Username cannot be None")

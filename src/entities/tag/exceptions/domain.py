class TagAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("Tag already exists")


class TagNotFoundError(Exception):
    def __init__(self):
        super().__init__("Tag not found")

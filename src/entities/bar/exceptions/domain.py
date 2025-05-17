class BarAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("Bar already exists")


class BarNotFoundError(Exception):
    def __init__(self):
        super().__init__("Bar not found")

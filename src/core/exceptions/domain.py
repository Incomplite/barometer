class UserAlreadyReviewedError(Exception):
    def __init__(self):
        super().__init__("User has already left a review")

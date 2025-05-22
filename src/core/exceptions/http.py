from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class UserAlreadyReviewedException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User has already left a review"

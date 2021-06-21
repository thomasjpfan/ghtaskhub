from enum import Enum


class Column(Enum):
    ACTIONABLE = "Actionable"
    WAITING_FOR_RESPONSE = "Waiting for Response"
    TO_REVIEW = "To Review"
    BUCKET = "Bucket List"
    DONE = "Done"

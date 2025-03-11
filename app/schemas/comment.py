from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str
    review_id: int  # ID отзыва, к которому относится комментарий
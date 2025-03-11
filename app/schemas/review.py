from pydantic import BaseModel


class ReviewCreate(BaseModel):
    text: str
    rating: int  # Рейтинг от 1 до 5
    product_id: int  # ID продукта, к которому относится отзыв
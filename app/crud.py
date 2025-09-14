"""CRUD-операции для работы с публикациями в базе данных."""
from sqlalchemy.orm import Session
from . import models, schemas


def get_posts(db: Session):
    """Получить список всех публикаций."""
    return db.query(models.Post).order_by(models.Post.id).all()


def create_post(db: Session, post_in: schemas.PostCreate):
    """Создать новую публикацию."""
    post = models.Post(title=post_in.title, content=post_in.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

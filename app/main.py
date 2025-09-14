"""Основной модуль приложения"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .logging_conf import logger

models.Base = models.Base if hasattr(models, 'Base') else None

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Blog')


def get_db():
    """Зависимость для предоставления сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/posts', response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    """Получить список публикаций."""
    posts = crud.get_posts(db)
    logger.info('GET /posts -> %d posts', len(posts))
    return posts


@app.post('/posts', response_model=schemas.PostOut, status_code=201)
def create_post(post_in: schemas.PostCreate, db: Session = Depends(get_db)):
    """Создать новую публикацию."""
    post = crud.create_post(db, post_in)
    logger.info('POST /posts -> created id=%s', post.id)
    return post

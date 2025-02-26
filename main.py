from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import logging
from sqlalchemy.orm import Session

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from database import get_db, redis_client, engine
import models

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="图书管理系统API")

# 定义数据模型
class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    price: float
    description: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        orm_mode = True

# 缓存装饰器
# 修改缓存装饰器，添加日志
def cache_response(expire=300):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 记录函数调用信息
            logger.debug(f"调用函数: {func.__name__}")
            logger.debug(f"参数: args={args}, kwargs={kwargs}")
            
            # 生成简单的缓存键
            func_name = func.__name__
            path_params = kwargs.get('book_id', '')
            query_params = kwargs.get('keyword', '')
            cache_key = f"{func_name}:{path_params}:{query_params}"
            logger.debug(f"缓存键: {cache_key}")
            
            # 尝试从缓存获取数据
            cached_data = redis_client.get(cache_key)
            if cached_data:
                logger.info(f"从缓存中获取数据: {cache_key}")
                return json.loads(cached_data)
            
            # 执行原始函数
            try:
                result = await func(*args, **kwargs)
                logger.debug(f"函数执行结果类型: {type(result)}")
            except Exception as e:
                logger.error(f"函数执行错误: {str(e)}", exc_info=True)
                raise
            
            # 处理序列化
            try:
                if isinstance(result, list):
                    serialized_data = [
                        {
                            key: str(value) if isinstance(value, datetime) else value
                            for key, value in item.__dict__.items()
                            if not key.startswith('_')
                        }
                        for item in result
                    ]
                else:
                    if hasattr(result, '__dict__'):
                        serialized_data = {
                            key: str(value) if isinstance(value, datetime) else value
                            for key, value in result.__dict__.items()
                            if not key.startswith('_')
                        }
                    else:
                        serialized_data = result
                
                logger.debug(f"序列化数据: {serialized_data}")
            except Exception as e:
                logger.error(f"序列化错误: {str(e)}", exc_info=True)
                raise
            
            # 存储到缓存
            try:
                redis_client.setex(
                    cache_key,
                    expire,
                    json.dumps(serialized_data)
                )
                logger.info(f"数据已缓存: {cache_key}")
            except Exception as e:
                logger.error(f"缓存存储错误: {str(e)}", exc_info=True)
                raise
            
            return result
        return wrapper
    return decorator

@app.get("/")
def read_root():
    return {"message": "欢迎使用图书管理系统API"}

@app.get("/books", response_model=List[Book])
# @cache_response(expire=60)
async def get_books(db: Session = Depends(get_db)):
    books = db.query(models.BookModel).all()
    return books

# 将搜索路由移到这里，确保它在 book_id 路由之前
@app.get("/books/search/")
# @cache_response(expire=60)
async def search_books(keyword: str, db: Session = Depends(get_db)):
    books = db.query(models.BookModel).filter(
        (models.BookModel.title.ilike(f"%{keyword}%")) |
        (models.BookModel.author.ilike(f"%{keyword}%"))
    ).all()
    return books

@app.get("/books/{book_id}", response_model=Book)
# @cache_response(expire=60)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="书籍未找到")
    return book

@app.post("/books", response_model=Book)
async def create_book(book: Book, db: Session = Depends(get_db)):
    db_book = models.BookModel(**book.dict(exclude={'id', 'create_time'}))
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    # 清除列表缓存
    redis_client.delete("get_books:():{}") 
    return db_book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: Book, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="书籍未找到")
    
    for key, value in book_update.dict(exclude={'id', 'create_time'}).items():
        setattr(book, key, value)
    
    db.commit()
    db.refresh(book)
    
    # 清除相关缓存
    redis_client.delete(f"get_book:({book_id},):{{}}")
    redis_client.delete("get_books:():{}") 
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="书籍未找到")
    
    db.delete(book)
    db.commit()
    
    # 清除相关缓存
    redis_client.delete(f"get_book:({book_id},):{{}}")
    redis_client.delete("get_books:():{}") 
    return {"message": "书籍已删除"}

@app.get("/books/search/")
# @cache_response(expire=60)
async def search_books(keyword: str, db: Session = Depends(get_db)):
    books = db.query(models.BookModel).filter(
        (models.BookModel.title.ilike(f"%{keyword}%")) |
        (models.BookModel.author.ilike(f"%{keyword}%"))
    ).all()
    return books
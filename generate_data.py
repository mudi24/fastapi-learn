from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BookModel, Base  # 添加 Base 的导入
from database import SQLALCHEMY_DATABASE_URL
import random
from datetime import datetime, timedelta

# 创建数据库连接
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# 创建数据库表
Base.metadata.create_all(bind=engine)  # 添加这行来创建表
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 示例数据
authors = [
    "莫言", "余华", "张爱玲", "王小波", "刘慈欣", "东野圭吾", 
    "村上春树", "乔治·马丁", "J.K.罗琳", "加西亚·马尔克斯"
]

book_titles_template = [
    "{}的世界", "{}之光", "{}传", "{}的故事", "{}札记",
    "{}回忆录", "{}笔记", "{}之门", "{}之夜", "{}密码"
]

genres = ["小说", "科幻", "文学", "传记", "历史", "悬疑", "奇幻", "散文"]

# 生成100条数据
def generate_books():
    books = []
    for i in range(100):
        # 随机生成书名
        title = random.choice(book_titles_template).format(
            random.choice(["春", "夏", "秋", "冬", "天", "地", "山", "海", "风", "雨"])
        )
        
        # 随机选择作者
        author = random.choice(authors)
        
        # 随机生成价格（29.9到199.9之间）
        price = round(random.uniform(29.9, 199.9), 2)
        
        # 随机生成描述
        description = f"这是一本{random.choice(genres)}类型的书籍，由{author}创作。"
        
        # 随机生成创建时间（过去一年内）
        days_ago = random.randint(0, 365)
        create_time = datetime.now() - timedelta(days=days_ago)
        
        # 创建书籍记录
        book = BookModel(
            title=title,
            author=author,
            price=price,
            description=description,
            create_time=create_time
        )
        books.append(book)
    
    return books

def main():
    # 生成并保存数据
    books = generate_books()
    db.bulk_save_objects(books)
    db.commit()
    print("成功生成100条书籍数据！")

if __name__ == "__main__":
    main()
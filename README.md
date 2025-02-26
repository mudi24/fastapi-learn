# FastAPI 图书管理系统

基于 FastAPI 框架开发的图书管理系统 API，实现了基本的图书 CRUD 操作，并集成了 SQLite 数据库存储和 Redis 缓存机制。

## 功能特点

- 完整的图书 CRUD 操作
- SQLite 数据库持久化存储
- Redis 缓存支持
- 自动生成 API 文档
- 支持图书搜索功能

## 环境要求

- Python 3.7+
- Redis

## 快速开始

### 1. 环境准备

首先确保已安装 Python 3.7+ 和 Redis。

安装 Redis（如果未安装）：
```bash
brew install redis
```

启动 Redis 服务：
```bash
brew services start redis
```

### 2. 项目设置

#### 2.1 创建虚拟环境
```bash
cd /Users/kaiyao/AI/fastapi-learn
python -m venv venv
source venv/bin/activate
```

#### 2.2 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 数据库初始化

生成测试数据：
```bash
python generate_data.py
```

### 4. 启动应用

```bash
uvicorn main:app --reload
```

## API 文档

启动应用后，可以通过以下地址访问 API 文档：

- Swagger UI：http://127.0.0.1:8000/docs
- ReDoc：http://127.0.0.1:8000/redoc

## API 接口示例

### 获取所有书籍
```bash
curl http://127.0.0.1:8000/books
```

### 获取单本书籍
```bash
curl http://127.0.0.1:8000/books/1
```

### 搜索书籍
```bash
curl "http://127.0.0.1:8000/books/search/?keyword=春"
```

### 创建新书籍
```bash
curl -X POST "http://127.0.0.1:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"title":"测试书籍","author":"测试作者","price":59.9,"description":"测试描述"}'
```

### 更新书籍
```bash
curl -X PUT "http://127.0.0.1:8000/books/1" \
     -H "Content-Type: application/json" \
     -d '{"title":"更新的书名","author":"更新的作者","price":69.9,"description":"更新的描述"}'
```

### 删除书籍
```bash
curl -X DELETE "http://127.0.0.1:8000/books/1"
```

## 项目结构

```
fastapi-learn/
├── main.py          # 主应用文件
├── database.py      # 数据库配置
├── models.py        # 数据库模型
├── generate_data.py # 测试数据生成脚本
└── requirements.txt # 项目依赖
```

## 注意事项

1. 确保 Redis 服务正在运行
2. 数据库文件 `books.db` 会自动在项目根目录创建
3. 修改代码后应用会自动重新加载
4. 缓存默认过期时间为60秒

## 停止服务

停止 FastAPI 应用：按 `Ctrl+C`

停止 Redis 服务：
```bash
brew services stop redis
```

退出虚拟环境：
```bash
deactivate
```
```
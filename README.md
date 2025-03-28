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

## 部署指南

### 1. 服务器准备
1. 安装必要的系统包：
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip redis-server nginx
```

2. 创建项目目录：
```bash
mkdir -p /var/www/fastapi-learn
cd /var/www/fastapi-learn
```

### 2. 项目部署

1. 克隆项目：
```bash
git clone <你的项目仓库URL> .
```

2. 创建虚拟环境：
```bash
python3.9 -m venv venv
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
pip install gunicorn
```

4. 创建系统服务配置文件：
```bash
sudo nano /etc/systemd/system/fastapi-learn.service
```

添加以下内容：
```ini
[Unit]
Description=FastAPI Book Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/fastapi-learn
Environment="PATH=/var/www/fastapi-learn/venv/bin"
ExecStart=/var/www/fastapi-learn/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b unix:/tmp/fastapi-learn.sock

[Install]
WantedBy=multi-user.target
```

5. 配置 Nginx：
```bash
sudo nano /etc/nginx/sites-available/fastapi-learn
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://unix:/tmp/fastapi-learn.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

6. 启用网站配置：
```bash
sudo ln -s /etc/nginx/sites-available/fastapi-learn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. 启动服务

1. 启动 Redis：
```bash
sudo systemctl start redis
sudo systemctl enable redis
```

2. 初始化数据库：
```bash
cd /var/www/fastapi-learn
source venv/bin/activate
python generate_data.py
```

3. 启动应用服务：
```bash
sudo systemctl start fastapi-learn
sudo systemctl enable fastapi-learn
```

### 4. 维护命令

- 查看应用日志：
```bash
sudo journalctl -u fastapi-learn
```

- 重启服务：
```bash
sudo systemctl restart fastapi-learn
```

- 查看服务状态：
```bash
sudo systemctl status fastapi-learn
```

### 5. 安全建议

1. 配置防火墙只开放必要端口：
```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable
```

2. 设置 SSL 证书（推荐使用 Let's Encrypt）：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

3. 定期更新系统和依赖：
```bash
sudo apt update && sudo apt upgrade
pip install --upgrade -r requirements.txt
```

### 6. 注意事项

1. 确保服务器防火墙配置正确
2. 定期备份数据库文件
3. 监控服务器资源使用情况
4. 配置日志轮转防止日志文件过大
5. 根据实际需求调整 Gunicorn 工作进程数
```

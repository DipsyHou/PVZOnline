# 使用 Python 3.10 slim 版本作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
# 防止 Python 生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
# 确保控制台输出不被缓冲
ENV PYTHONUNBUFFERED=1

# 更新 apt 并安装一些基础工具（如果以后需要 gcc 等编译依赖可以添加）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
# 使用阿里云镜像加速（可选，但在国内构建很有用）
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目代码
COPY . .

# 确保数据库目录存在 (SQLite 需要)
RUN mkdir -p database

# 暴露端口
EXPOSE 8000

# 启动命令
# 指向 backend.server:app，因为 server.py 在 backend 目录下
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]

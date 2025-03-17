# 使用官方 Python 基礎映像
FROM python:3.11

# 設置工作目錄
WORKDIR /app

# 複製當前目錄的內容到容器內的 /app 資料夾
COPY . /app

# 安裝依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 暴露應用運行的端口
EXPOSE 5000

# 啟動 FastAPI 應用
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

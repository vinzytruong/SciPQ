# SciQuery - Hệ thống Quản lý Bài báo Khoa học

SciQuery là một hệ thống quản lý bài báo khoa học được xây dựng bằng Flask và Neo4j, cho phép quản lý tác giả, lĩnh vực nghiên cứu và bài báo khoa học.

## Yêu cầu hệ thống

- Docker và Docker Compose
- Python 3.8 trở lên

## Cài đặt và Chạy

1. Clone repository:
```bash
git clone [repository-url]
cd SciPQ
```

2. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

3. Khởi động Neo4j bằng Docker Compose:
```bash
docker-compose up -d
```

4. Chạy ứng dụng:
```bash
cd SciQuery

python app.py
```

## Cấu hình

- Neo4j chạy trên port 7474 (HTTP)
- Flask API chạy trên port 5000
- Các thông tin kết nối Neo4j được cấu hình trong file `.env`
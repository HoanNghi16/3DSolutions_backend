# 3D Solutions Backend

Backend cho dự án 3D Solutions, được xây dựng bằng **Django** và **Django REST Framework**.  
Hệ thống cung cấp API cho frontend/web/app với kiến trúc tách biệt rõ ràng, dễ bảo trì và mở rộng.

---

## Công nghệ sử dụng

- **Python 3.x**
- **Django**
- **Django REST Framework (DRF)**
- **PostgreSQL**
- **psycopg2 / psycopg2-binary**
- **Virtual Environment (venv)**

---

### 1. Tạo virtual environment

```bash
python -m venv venv

```
### 2. Kích hoạt môi trường

# Window:

```bash
venv\Scripts\activate
```
# macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 4. Chạy server phát triển

```bash
python manage.py runserver
```

### 5. Tạo tài khoản admin

```bash
python manage.py createsuperuser
```



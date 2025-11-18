# Auto Find Photo

Ứng dụng quản lý và sao chép ảnh với giao diện đăng nhập/đăng ký.

## Cấu trúc dự án

```
Sort_Images/
├── main.py              # File khởi động chính
├── config.py            # Cấu hình và constants
├── utils.py             # Các hàm tiện ích
├── login_screen.py      # Màn hình đăng nhập/đăng ký
├── main_app.py          # Ứng dụng chính (sao chép ảnh)
├── asset/               # Thư mục chứa assets (icon, scripts)
└── venv/                # Virtual environment
```

## Mô tả các file

### `main.py`
File khởi động chính của ứng dụng. Chạy màn hình đăng nhập khi khởi động.

### `config.py`
Chứa các cấu hình và constants:
- Đường dẫn icon
- Kích thước cửa sổ
- Màu sắc giao diện
- Các text labels

### `utils.py`
Các hàm tiện ích được dùng chung:
- `set_window_icon()`: Thiết lập icon cho cửa sổ

### `login_screen.py`
Màn hình đăng nhập và đăng ký:
- Form đăng nhập (username, password)
- Form đăng ký (username, password, phone, email, invitation code)
- Xử lý validation và đăng nhập

### `main_app.py`
Ứng dụng chính sau khi đăng nhập:
- Chọn thư mục nguồn chứa ảnh
- Lọc ảnh theo tên
- Sao chép ảnh sang thư mục đích

## Cách chạy

```bash
python main.py
```

## Lợi ích của cấu trúc này

1. **Dễ bảo trì**: Mỗi module có trách nhiệm rõ ràng
2. **Tái sử dụng**: Các hàm utility có thể dùng ở nhiều nơi
3. **Dễ mở rộng**: Dễ thêm tính năng mới
4. **Tổ chức tốt**: Code được phân loại theo chức năng
5. **Dễ test**: Có thể test từng module riêng biệt


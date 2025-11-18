"""
Module lưu trữ thông tin đăng nhập
"""

import json
import os
from typing import Optional, Dict

STORAGE_FILE = "auth_data.json"


def save_auth_data(username: str, password: str = None, token: str = None, remember: bool = True):
    """
    Lưu thông tin đăng nhập
    
    Args:
        username: Tên đăng nhập
        password: Mật khẩu (có thể None nếu có token)
        token: Token xác thực (có thể None)
        remember: Có ghi nhớ hay không
    """
    if not remember:
        # Nếu không ghi nhớ, xóa file nếu có
        if os.path.exists(STORAGE_FILE):
            os.remove(STORAGE_FILE)
        return
    
    data = {
        "username": username,
        "remember": remember
    }
    
    # Chỉ lưu password nếu không có token (bảo mật kém hơn nhưng cần cho auto-login)
    if password:
        data["password"] = password
    
    # Ưu tiên lưu token nếu có
    if token:
        data["token"] = token
        # Xóa password nếu có token
        if "password" in data:
            del data["password"]
    
    try:
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi lưu thông tin đăng nhập: {e}")


def load_auth_data() -> Optional[Dict]:
    """
    Đọc thông tin đăng nhập đã lưu
    
    Returns:
        Dict chứa username, password/token nếu có, None nếu không có
    """
    if not os.path.exists(STORAGE_FILE):
        return None
    
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Kiểm tra xem có remember không
            if not data.get("remember", False):
                return None
            return data
    except Exception as e:
        print(f"Lỗi đọc thông tin đăng nhập: {e}")
        return None


def clear_auth_data():
    """Xóa thông tin đăng nhập đã lưu"""
    if os.path.exists(STORAGE_FILE):
        try:
            os.remove(STORAGE_FILE)
        except Exception as e:
            print(f"Lỗi xóa thông tin đăng nhập: {e}")


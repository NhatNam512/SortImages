"""
Client xử lý các API request
"""

import requests
from config import API_BASE_URL, API_REGISTER, API_LOGIN
from machine_id import get_machine_id


class APIError(Exception):
    """Exception cho lỗi API"""
    pass


def register_user(username: str, email: str, password: str, key: str) -> dict:
    """
    Đăng ký người dùng mới
    
    Args:
        username: Tên đăng nhập
        email: Email
        password: Mật khẩu
        key: Mã mời/giới thiệu
        
    Returns:
        dict: Response từ API
        
    Raises:
        APIError: Nếu có lỗi xảy ra
    """
    url = f"{API_BASE_URL}{API_REGISTER}"
    
    # Lấy machine ID
    machine_id = get_machine_id()
    
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "key": key,
        "machineName": machine_id
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Ném exception nếu status code không phải 2xx
        return {
            "success": True,
            "data": response.json() if response.content else {}
        }
    except requests.exceptions.Timeout:
        raise APIError("Kết nối timeout. Vui lòng thử lại sau.")
    except requests.exceptions.ConnectionError:
        raise APIError("Không thể kết nối đến server. Vui lòng kiểm tra kết nối internet.")
    except requests.exceptions.HTTPError as e:
        try:
            error_data = response.json()
            error_message = error_data.get("message", error_data.get("error", "Đăng ký thất bại"))
        except:
            error_message = f"Đăng ký thất bại: {response.status_code}"
        raise APIError(error_message)
    except Exception as e:
        raise APIError(f"Lỗi không xác định: {str(e)}")


def login_user(username: str, password: str) -> dict:
    """
    Đăng nhập người dùng
    
    Args:
        username: Tên đăng nhập
        password: Mật khẩu
        
    Returns:
        dict: Response từ API (có thể chứa token)
        
    Raises:
        APIError: Nếu có lỗi xảy ra
    """
    url = f"{API_BASE_URL}{API_LOGIN}"
    
    # Lấy machine ID
    machine_id = get_machine_id()
    
    payload = {
        "username": username,
        "password": password,
        "machineName": machine_id
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Ném exception nếu status code không phải 2xx
        return {
            "success": True,
            "data": response.json() if response.content else {}
        }
    except requests.exceptions.Timeout:
        raise APIError("Kết nối timeout. Vui lòng thử lại sau.")
    except requests.exceptions.ConnectionError:
        raise APIError("Không thể kết nối đến server. Vui lòng kiểm tra kết nối internet.")
    except requests.exceptions.HTTPError as e:
        try:
            error_data = response.json()
            error_message = error_data.get("message", error_data.get("error", "Đăng nhập thất bại"))
        except:
            error_message = f"Đăng nhập thất bại: {response.status_code}"
        raise APIError(error_message)
    except Exception as e:
        raise APIError(f"Lỗi không xác định: {str(e)}")


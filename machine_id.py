"""
Module lấy ID duy nhất của máy tính
"""

import os
import platform
import subprocess
import hashlib
import uuid


def get_machine_id() -> str:
    """
    Lấy ID duy nhất của máy tính (không đổi khi restart)
    
    Returns:
        str: Machine ID duy nhất
    """
    system = platform.system()
    
    if system == "Windows":
        return _get_windows_machine_id()
    elif system == "Darwin":  # macOS
        return _get_macos_machine_id()
    elif system == "Linux":
        return _get_linux_machine_id()
    else:
        # Fallback: dùng MAC address
        return _get_mac_address_id()


def _get_windows_machine_id() -> str:
    """Lấy machine ID trên Windows"""
    try:
        # Cách 1: Lấy CPU ID
        try:
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'ProcessorId'],
                capture_output=True,
                text=True,
                check=True
            )
            cpu_id = result.stdout.strip().split('\n')[1].strip()
            if cpu_id:
                return hashlib.md5(cpu_id.encode()).hexdigest()
        except:
            pass
        
        # Cách 2: Lấy Motherboard Serial Number
        try:
            result = subprocess.run(
                ['wmic', 'baseboard', 'get', 'serialnumber'],
                capture_output=True,
                text=True,
                check=True
            )
            serial = result.stdout.strip().split('\n')[1].strip()
            if serial and serial != "To be filled by O.E.M.":
                return hashlib.md5(serial.encode()).hexdigest()
        except:
            pass
        
        # Cách 3: Lấy Machine GUID từ registry
        try:
            result = subprocess.run(
                ['reg', 'query', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography', 
                 '/v', 'MachineGuid'],
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.split('\n'):
                if 'MachineGuid' in line:
                    guid = line.split()[-1]
                    if guid:
                        return hashlib.md5(guid.encode()).hexdigest()
        except:
            pass
        
    except Exception as e:
        print(f"Lỗi lấy machine ID Windows: {e}")
    
    # Fallback: MAC address
    return _get_mac_address_id()


def _get_macos_machine_id() -> str:
    """Lấy machine ID trên macOS"""
    try:
        # Lấy System UUID
        result = subprocess.run(
            ['system_profiler', 'SPHardwareDataType'],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'Hardware UUID' in line or 'UUID' in line:
                uuid_str = line.split(':')[-1].strip()
                if uuid_str:
                    return hashlib.md5(uuid_str.encode()).hexdigest()
    except Exception as e:
        print(f"Lỗi lấy machine ID macOS: {e}")
    
    # Fallback: MAC address
    return _get_mac_address_id()


def _get_linux_machine_id() -> str:
    """Lấy machine ID trên Linux"""
    try:
        # Đọc /etc/machine-id (systemd)
        if os.path.exists('/etc/machine-id'):
            with open('/etc/machine-id', 'r') as f:
                machine_id = f.read().strip()
                if machine_id:
                    return hashlib.md5(machine_id.encode()).hexdigest()
        
        # Fallback: /var/lib/dbus/machine-id
        if os.path.exists('/var/lib/dbus/machine-id'):
            with open('/var/lib/dbus/machine-id', 'r') as f:
                machine_id = f.read().strip()
                if machine_id:
                    return hashlib.md5(machine_id.encode()).hexdigest()
    except Exception as e:
        print(f"Lỗi lấy machine ID Linux: {e}")
    
    # Fallback: MAC address
    return _get_mac_address_id()


def _get_mac_address_id() -> str:
    """
    Lấy MAC address làm fallback (có thể thay đổi nếu thay card mạng)
    
    Returns:
        str: MD5 hash của MAC address
    """
    try:
        # Lấy MAC address của network adapter đầu tiên
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                       for elements in range(0, 2*6, 2)][::-1])
        return hashlib.md5(mac.encode()).hexdigest()
    except Exception as e:
        print(f"Lỗi lấy MAC address: {e}")
        # Fallback cuối cùng: random UUID (không tốt lắm)
        return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()


def get_machine_id_simple() -> str:
    """
    Cách đơn giản hơn: Lấy MAC address (phổ biến trên mọi OS)
    
    Returns:
        str: Machine ID dựa trên MAC address
    """
    mac = uuid.getnode()
    # Chuyển sang hex và hash
    mac_str = hex(mac).replace('0x', '')
    return hashlib.sha256(mac_str.encode()).hexdigest()[:32]


if __name__ == "__main__":
    # Test
    print(f"Machine ID: {get_machine_id()}")
    print(f"Machine ID (Simple): {get_machine_id_simple()}")


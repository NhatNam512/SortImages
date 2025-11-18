"""
Script tạo icon cho ứng dụng Sao chép ảnh nâng cao
Chạy script này để tạo file icon.ico và icon.png
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    print("Pillow chưa được cài đặt. Đang cài đặt...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True

def create_icon():
    """Tạo icon với biểu tượng ảnh và mũi tên copy"""
    
    # Tạo icon PNG 256x256
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Màu nền gradient (xanh dương nhạt)
    for i in range(size):
        alpha = int(200 + (55 * i / size))
        color = (70, 130, 180, alpha)  # Steel Blue
        draw.rectangle([(0, i), (size, i+1)], fill=color)
    
    # Vẽ khung ảnh (hình chữ nhật bo góc)
    margin = 40
    frame_size = size - 2 * margin
    corner_radius = 15
    
    # Khung ảnh chính
    frame_coords = [
        (margin + corner_radius, margin),
        (size - margin - corner_radius, margin),
        (size - margin, margin + corner_radius),
        (size - margin, size - margin - corner_radius),
        (size - margin - corner_radius, size - margin),
        (margin + corner_radius, size - margin),
        (margin, size - margin - corner_radius),
        (margin, margin + corner_radius)
    ]
    draw.polygon(frame_coords, fill=(255, 255, 255, 255))
    
    # Vẽ đường viền khung
    draw.rectangle([margin, margin, size - margin, size - margin], 
                   outline=(50, 100, 150, 255), width=3)
    
    # Vẽ biểu tượng ảnh (3 đường ngang)
    line_y = [margin + 60, margin + 100, margin + 140]
    for y in line_y:
        draw.rectangle([margin + 50, y, size - margin - 50, y + 8], 
                      fill=(100, 150, 200, 255))
    
    # Vẽ mũi tên copy (ở góc dưới bên phải)
    arrow_size = 50
    arrow_x = size - margin - 30
    arrow_y = size - margin - 30
    
    # Mũi tên tròn
    draw.ellipse([arrow_x - arrow_size//2, arrow_y - arrow_size//2,
                  arrow_x + arrow_size//2, arrow_y + arrow_size//2],
                 fill=(76, 175, 80, 255), outline=(50, 150, 50, 255), width=2)
    
    # Vẽ mũi tên
    arrow_points = [
        (arrow_x - 10, arrow_y - 5),
        (arrow_x + 10, arrow_y - 5),
        (arrow_x + 5, arrow_y),
        (arrow_x + 10, arrow_y - 5),
        (arrow_x + 10, arrow_y + 5),
        (arrow_x + 5, arrow_y)
    ]
    draw.polygon(arrow_points[:4], fill=(255, 255, 255, 255))
    
    # Lưu file PNG
    img.save('icon.png', 'PNG')
    print("[OK] Da tao icon.png")
    
    # Tạo các kích thước cho ICO (Windows yêu cầu nhiều kích thước)
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    
    for ico_size in sizes:
        resized = img.resize(ico_size, Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    # Lưu file ICO
    ico_images[0].save('icon.ico', format='ICO', sizes=[(s[0], s[1]) for s in sizes])
    print("[OK] Da tao icon.ico")
    
    print("\n[HOAN THANH] Icon da duoc tao:")
    print("   - icon.png (256x256)")
    print("   - icon.ico (nhieu kich thuoc)")
    print("\nChay lai ung dung de xem icon moi!")

if __name__ == "__main__":
    try:
        create_icon()
    except Exception as e:
        print(f"[LOI] Loi khi tao icon: {e}")
        print("\nHay thu cai dat Pillow thu cong:")
        print("   pip install pillow")


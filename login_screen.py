"""
Màn hình đăng nhập và đăng ký
"""

from tkinter import Tk, Label, Button, Entry, Frame, X, Canvas, Checkbutton, IntVar
from config import (
    LOGIN_WINDOW_TITLE, LOGIN_WINDOW_SIZE, LOGIN_BG_COLOR,
    LOGIN_LEFT_BG, LOGIN_RIGHT_BG, COLORS
)
from utils import set_window_icon
from api_client import login_user, register_user, APIError
from icon_loader import create_icon_label, get_icon_text
from auth_storage import save_auth_data, load_auth_data, clear_auth_data


def show_login_screen():
    """Hiển thị màn hình đăng nhập"""
    # Kiểm tra xem có thông tin đăng nhập đã lưu không
    saved_auth = load_auth_data()
    if saved_auth and saved_auth.get("remember"):
        # Tự động đăng nhập
        username = saved_auth.get("username")
        password = saved_auth.get("password")
        token = saved_auth.get("token")
        
        if username and (password or token):
            # Tạo cửa sổ ẩn để xử lý đăng nhập tự động
            temp_window = Tk()
            temp_window.withdraw()  # Ẩn cửa sổ
            
            # Thử đăng nhập tự động
            try:
                if password:
                    result = login_user(username, password)
                    if result.get("success"):
                        # Lưu lại token mới nếu có
                        new_token = result.get("data", {}).get("token")
                        if new_token:
                            save_auth_data(username, password, new_token, remember=True)
                elif token:
                    # Nếu có token, có thể skip login nhưng vẫn cần machine ID
                    # Để đảm bảo, vẫn gọi API login với password đã lưu
                    if password:
                        result = login_user(username, password)
                    else:
                        # Nếu không có password, giả sử token còn hợp lệ
                        result = {"success": True, "data": {"token": token}}
                else:
                    result = {"success": False}
                
                if result.get("success"):
                    # Đăng nhập thành công, vào thẳng trang chủ
                    temp_window.destroy()
                    import main_app
                    main_app.start_main_app()
                    return
            except Exception as e:
                # Nếu đăng nhập tự động thất bại, hiển thị màn hình đăng nhập
                print(f"Đăng nhập tự động thất bại: {e}")
            
            temp_window.destroy()
    
    # Hiển thị màn hình đăng nhập bình thường
    login_window = Tk()
    login_window.title(LOGIN_WINDOW_TITLE)
    login_window.geometry(LOGIN_WINDOW_SIZE)
    login_window.resizable(False, False)
    login_window.configure(bg=LOGIN_BG_COLOR)
    
    # Đặt icon
    set_window_icon(login_window)
    
    # Điền thông tin đã lưu nếu có
    saved_auth = load_auth_data()
    saved_username = saved_auth.get("username", "") if saved_auth else ""
    saved_password = saved_auth.get("password", "") if saved_auth else ""
    
    # Container chính
    main_container = Frame(login_window, bg=LOGIN_BG_COLOR)
    main_container.pack(fill="both", expand=True)
    
    # --- Phần bên trái: Đăng nhập ---
    left_frame = Frame(main_container, bg=LOGIN_LEFT_BG, width=500)
    left_frame.pack(side="left", fill="both", expand=True)
    left_frame.pack_propagate(False)
    
    # Nội dung đăng nhập
    login_content = Frame(left_frame, bg=LOGIN_LEFT_BG, padx=50, pady=40)
    login_content.pack(fill="both", expand=True)
    
    # Icon và branding
    icon_label = create_icon_label(login_content, "app", font_size=48, 
                                   bg_color=LOGIN_LEFT_BG, fg_color=COLORS["white"])
    icon_label.pack(anchor="w", pady=(20, 10))
    
    # Text "Bạn đã có tài khoản?"
    account_text = Label(login_content, text="Bạn đã có tài khoản? Đăng nhập ngay", 
                        font=("Arial", 12), bg=LOGIN_LEFT_BG, fg=COLORS["white"])
    account_text.pack(anchor="w", pady=(0, 30))
    
    # Username với icon và underline
    username_frame = Frame(login_content, bg=LOGIN_LEFT_BG)
    username_frame.pack(fill=X, pady=(0, 15))
    create_icon_label(username_frame, "user", font_size=16, 
                     bg_color=LOGIN_LEFT_BG, fg_color=COLORS["white"]).pack(side="left", padx=(0, 10))
    username_entry_frame = Frame(username_frame, bg=LOGIN_LEFT_BG)
    username_entry_frame.pack(side="left", fill=X, expand=True)
    login_username_entry = Entry(username_entry_frame, font=("Arial", 12), bg=LOGIN_LEFT_BG, fg=COLORS["white"], 
                                 insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    login_username_entry.pack(fill=X, ipady=5)
    Frame(username_entry_frame, bg="white", height=1).pack(fill=X, pady=(2, 0))
    if saved_username:
        login_username_entry.insert(0, saved_username)
    login_username_entry.focus()
    
    # Password với icon và underline
    password_frame = Frame(login_content, bg=LOGIN_LEFT_BG)
    password_frame.pack(fill=X, pady=(0, 15))
    create_icon_label(password_frame, "password", font_size=16, 
                     bg_color=LOGIN_LEFT_BG, fg_color=COLORS["white"]).pack(side="left", padx=(0, 10))
    password_entry_frame = Frame(password_frame, bg=LOGIN_LEFT_BG)
    password_entry_frame.pack(side="left", fill=X, expand=True)
    login_password_entry = Entry(password_entry_frame, font=("Arial", 12), bg=LOGIN_LEFT_BG, fg=COLORS["white"],
                                 insertbackground="white", show="*", relief="flat", bd=0, highlightthickness=0)
    login_password_entry.pack(fill=X, ipady=5)
    Frame(password_entry_frame, bg="white", height=1).pack(fill=X, pady=(2, 0))
    if saved_password:
        login_password_entry.insert(0, saved_password)
    
    # Checkbox "Ghi nhớ tài khoản"
    remember_var = IntVar(value=1 if saved_auth and saved_auth.get("remember") else 1)
    remember_check = Checkbutton(login_content, text="Ghi nhớ tài khoản", 
                                font=("Arial", 10), bg=LOGIN_LEFT_BG, fg=COLORS["white"],
                                activebackground=LOGIN_LEFT_BG, activeforeground=COLORS["white"],
                                selectcolor=COLORS["darker_bg"], variable=remember_var)
    remember_check.pack(anchor="w", pady=(0, 25))
    
    # Label thông báo đăng nhập
    login_status_label = Label(login_content, text="", font=("Arial", 9), bg=LOGIN_LEFT_BG, fg="red")
    login_status_label.pack(anchor="w", pady=(0, 10))
    
    # Nút đăng nhập (màu đỏ)
    def handle_login():
        username = login_username_entry.get().strip()
        password = login_password_entry.get()
        
        if not username:
            login_status_label.config(text="Vui lòng nhập tên đăng nhập!", fg="red")
            return
        if not password:
            login_status_label.config(text="Vui lòng nhập mật khẩu!", fg="red")
            return
        
        # Hiển thị loading
        login_status_label.config(text="Đang đăng nhập...", fg="blue")
        login_button.config(state="disabled")
        
        # Gọi API đăng nhập
        try:
            result = login_user(username, password)
            if result["success"]:
                login_status_label.config(text="Đăng nhập thành công!", fg="green")
                # Lưu thông tin đăng nhập nếu có ghi nhớ
                remember = remember_var.get() == 1
                token = result.get("data", {}).get("token")
                if remember:
                    save_auth_data(username, password, token, remember=True)
                else:
                    clear_auth_data()
                login_window.after(500, lambda: close_login_and_start_app(login_window))
            else:
                login_status_label.config(text="Đăng nhập thất bại!", fg="red")
                login_button.config(state="normal")
        except APIError as e:
            login_status_label.config(text=str(e), fg="red")
            login_button.config(state="normal")
        except Exception as e:
            login_status_label.config(text=f"Lỗi: {str(e)}", fg="red")
            login_button.config(state="normal")
    
    login_button = Button(login_content, text="Login Now", command=handle_login,
                         font=("Arial", 13, "bold"), bg=COLORS["red"], fg=COLORS["white"],
                         padx=50, pady=14, cursor="hand2", relief="flat", bd=0,
                         activebackground=COLORS["red_dark"], activeforeground=COLORS["white"])
    login_button.pack(anchor="w", pady=(0, 20))
    
    # Enter để đăng nhập
    login_password_entry.bind("<Return>", lambda e: handle_login())
    login_username_entry.bind("<Return>", lambda e: login_password_entry.focus())
    
    # --- Phần bên phải: Đăng ký ---
    right_frame = Frame(main_container, bg=LOGIN_RIGHT_BG, width=500)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)
    
    # Canvas cho wave decoration
    wave_canvas = Canvas(right_frame, bg=LOGIN_RIGHT_BG, highlightthickness=0)
    wave_canvas.pack(fill="both", expand=True)
    
    # Vẽ wave decoration (màu xanh nhạt)
    wave_canvas.create_oval(-200, 200, 800, 1000, fill=COLORS["teal"], outline="")
    wave_canvas.create_oval(-100, 300, 700, 900, fill=COLORS["teal_dark"], outline="")
    
    # Nội dung đăng ký
    register_content = Frame(wave_canvas, bg=LOGIN_RIGHT_BG)
    register_content.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)
    
    # Title
    register_title = Label(register_content, text="Đăng kí hoặc nâng cấp tài khoản",
                          font=("Arial", 16, "bold"), bg=LOGIN_RIGHT_BG, fg=COLORS["white"])
    register_title.pack(anchor="w", pady=(20, 30))
    
    # Username
    username_reg_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    username_reg_frame.pack(fill=X, pady=(0, 8))
    create_icon_label(username_reg_frame, "user", font_size=14, 
                     bg_color=LOGIN_RIGHT_BG, fg_color=COLORS["white"]).pack(side="left", padx=(0, 8))
    Label(username_reg_frame, text="Tên tài khoản", font=("Arial", 10), bg=LOGIN_RIGHT_BG, fg=COLORS["white"]).pack(side="left")
    
    username_entry_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    username_entry_frame.pack(fill=X, pady=(0, 15))
    register_username_entry = Entry(username_entry_frame, font=("Arial", 11), bg=LOGIN_RIGHT_BG, fg=COLORS["white"],
                                    insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    register_username_entry.pack(fill=X, ipady=5)
    Frame(username_entry_frame, bg="white", height=1).pack(fill=X, pady=(2, 0))
    
    # Password
    password_reg_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    password_reg_frame.pack(fill=X, pady=(0, 8))
    create_icon_label(password_reg_frame, "password", font_size=14, 
                     bg_color=LOGIN_RIGHT_BG, fg_color=COLORS["white"]).pack(side="left", padx=(0, 8))
    Label(password_reg_frame, text="Mật khẩu", font=("Arial", 10), bg=LOGIN_RIGHT_BG, fg=COLORS["white"]).pack(side="left")
    
    password_entry_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    password_entry_frame.pack(fill=X, pady=(0, 15))
    register_password_entry = Entry(password_entry_frame, font=("Arial", 11), bg=LOGIN_RIGHT_BG, fg=COLORS["white"],
                                    insertbackground="white", show="*", relief="flat", bd=0, highlightthickness=0)
    register_password_entry.pack(fill=X, ipady=5)
    Frame(password_entry_frame, bg="white", height=1).pack(fill=X, pady=(2, 0))
    
    # Email
    email_reg_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    email_reg_frame.pack(fill=X, pady=(0, 8))
    create_icon_label(email_reg_frame, "email", font_size=14, 
                     bg_color=LOGIN_RIGHT_BG, fg_color=COLORS["white"]).pack(side="left", padx=(0, 8))
    Label(email_reg_frame, text="Email", font=("Arial", 10), bg=LOGIN_RIGHT_BG, fg=COLORS["white"]).pack(side="left")
    
    email_entry_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    email_entry_frame.pack(fill=X, pady=(0, 15))
    register_email_entry = Entry(email_entry_frame, font=("Arial", 11), bg=LOGIN_RIGHT_BG, fg=COLORS["white"],
                                 insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    register_email_entry.pack(fill=X, ipady=5)
    Frame(email_entry_frame, bg="white", height=1).pack(fill=X, pady=(2, 0))
    
    # Invitation code
    invite_reg_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    invite_reg_frame.pack(fill=X, pady=(0, 8))
    create_icon_label(invite_reg_frame, "invite", font_size=14, 
                     bg_color=LOGIN_RIGHT_BG, fg_color=COLORS["white"]).pack(side="left", padx=(0, 8))
    Label(invite_reg_frame, text="Mã giới thiệu", font=("Arial", 10), bg=LOGIN_RIGHT_BG, fg=COLORS["white"]).pack(side="left")
    
    invite_entry_frame = Frame(register_content, bg=LOGIN_RIGHT_BG)
    invite_entry_frame.pack(fill=X, pady=(0, 20))
    register_invite_code_entry = Entry(invite_entry_frame, font=("Arial", 11), bg=LOGIN_RIGHT_BG, fg=COLORS["white"],
                                       insertbackground="white", relief="flat", bd=0, highlightthickness=0)
    register_invite_code_entry.pack(fill=X, ipady=5)
    Frame(invite_entry_frame, bg="white", height=1).pack(fill=X, pady=(2, 0))
    
    # Label thông báo đăng ký
    register_status_label = Label(register_content, text="", font=("Arial", 9), bg=LOGIN_RIGHT_BG, fg="red", wraplength=400)
    register_status_label.pack(pady=(0, 10))
    
    # Nút đăng ký (màu xanh nhạt)
    def handle_register():
        username = register_username_entry.get().strip()
        password = register_password_entry.get()
        email = register_email_entry.get().strip()
        invite_code = register_invite_code_entry.get().strip()
        
        # Validation
        if not username:
            register_status_label.config(text="Vui lòng nhập tên đăng nhập!", fg="red")
            return
        if not password:
            register_status_label.config(text="Vui lòng nhập mật khẩu!", fg="red")
            return
        if len(password) < 6:
            register_status_label.config(text="Mật khẩu phải có ít nhất 6 ký tự!", fg="red")
            return
        if not email:
            register_status_label.config(text="Vui lòng nhập email!", fg="red")
            return
        if "@" not in email or "." not in email:
            register_status_label.config(text="Email không hợp lệ!", fg="red")
            return
        if not invite_code:
            register_status_label.config(text="Vui lòng nhập mã giới thiệu!", fg="red")
            return
        
        # Hiển thị loading
        register_status_label.config(text="Đang đăng ký...", fg="blue")
        register_button.config(state="disabled")
        
        # Gọi API đăng ký
        try:
            result = register_user(username, email, password, invite_code)
            if result["success"]:
                register_status_label.config(text="Đăng ký thành công! Vui lòng đăng nhập.", fg="green")
                # Chuyển sang tab đăng nhập sau 1.5 giây
                login_window.after(1500, lambda: (
                    login_username_entry.delete(0, "end"),
                    login_username_entry.insert(0, username),
                    login_password_entry.delete(0, "end"),
                    login_username_entry.focus()
                ))
                register_button.config(state="normal")
            else:
                register_status_label.config(text="Đăng ký thất bại!", fg="red")
                register_button.config(state="normal")
        except APIError as e:
            register_status_label.config(text=str(e), fg="red")
            register_button.config(state="normal")
        except Exception as e:
            register_status_label.config(text=f"Lỗi: {str(e)}", fg="red")
            register_button.config(state="normal")
    
    register_button = Button(register_content, text="Tạo tài khoản", command=handle_register,
                            font=("Arial", 11, "bold"), bg=COLORS["teal"], fg=LOGIN_RIGHT_BG,
                            padx=30, pady=10, cursor="hand2", relief="flat", bd=0,
                            activebackground=COLORS["teal_dark"], activeforeground=LOGIN_RIGHT_BG)
    register_button.pack(pady=10)
    
    # Enter để đăng ký
    register_invite_code_entry.bind("<Return>", lambda e: handle_register())
    
    login_window.mainloop()


def close_login_and_start_app(login_window):
    """Đóng cửa sổ đăng nhập và khởi động ứng dụng chính"""
    try:
        login_window.quit()  # Dừng mainloop trước
        login_window.destroy()  # Sau đó destroy window
    except:
        pass
    # Import ở đây để tránh circular import
    import main_app
    main_app.start_main_app()


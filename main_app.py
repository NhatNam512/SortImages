"""
Ứng dụng chính - Sao chép ảnh nâng cao
"""

import os
import shutil
from tkinter import (
    Tk, Label, Button, Entry, filedialog, Listbox, END,
    Scrollbar, RIGHT, Y, LEFT, BOTH, Frame, X, Canvas
)
from config import MAIN_APP_TITLE, MAIN_APP_SIZE, MAIN_APP_BG, MAIN_APP_CARD_BG, COLORS
from utils import set_window_icon
from icon_loader import create_icon_label
from auth_storage import clear_auth_data


def start_main_app():
    """Khởi tạo và chạy ứng dụng chính"""
    root = Tk()
    root.title(MAIN_APP_TITLE)
    root.geometry(MAIN_APP_SIZE)
    root.resizable(True, True)
    root.configure(bg=MAIN_APP_BG)
    
    # Đặt icon
    set_window_icon(root)
    
    # Biến để lưu trữ dữ liệu
    image_list = []
    source_folder = ""
    
    # --- Chọn thư mục nguồn ---
    def select_source_folder():
        nonlocal source_folder
        folder = filedialog.askdirectory(title="Chọn thư mục chứa ảnh")
        if folder:
            source_folder = folder
            folder_name = os.path.basename(source_folder)
            source_display.config(text=f"📂 {folder_name}", fg=COLORS["white"])
            status_label.config(text=f"Thư mục nguồn: {source_folder}", fg=COLORS["white"])
            listbox.delete(0, END)
            count_label.config(text="(0 ảnh)", fg=COLORS["gray"])
    
    # --- Lọc ảnh theo tên ---
    def filter_images():
        nonlocal image_list
        listbox.delete(0, END)
        image_list = []
        if not source_folder:
            status_label.config(text="Vui lòng chọn thư mục nguồn trước!", fg=COLORS["red"])
            return
        # Lấy tên nhập
        names_input = name_entry.get().strip()
        if not names_input or names_input == "Nhập tên ảnh (cách nhau bằng dấu phẩy)":
            status_label.config(text="Vui lòng nhập tên ảnh muốn copy!", fg=COLORS["red"])
            return
        names = [n.strip() for n in names_input.split(",") if n.strip()]
        # Lọc file trong folder
        for file in os.listdir(source_folder):
            if file in names or os.path.splitext(file)[0] in names:
                full_path = os.path.join(source_folder, file)
                if os.path.isfile(full_path):
                    image_list.append(full_path)
                    listbox.insert(END, file)
        count_label.config(text=f"({len(image_list)} ảnh)", 
                          fg=COLORS["white"] if image_list else COLORS["gray"])
        status_label.config(text=f"Tìm thấy {len(image_list)} ảnh", fg=COLORS["green"])
    
    # --- Chọn thư mục đích và copy ---
    def copy_images():
        if not image_list:
            status_label.config(text="Không có ảnh để copy!", fg=COLORS["red"])
            return
        dest_folder = filedialog.askdirectory(title="Chọn thư mục đích")
        if not dest_folder:
            return
        status_label.config(text="Đang sao chép...", fg=COLORS["teal"])
        copy_button.config(state="disabled")
        try:
            for file in image_list:
                shutil.copy(file, dest_folder)
            status_label.config(text=f"✅ Sao chép {len(image_list)} ảnh xong!", fg=COLORS["green"])
        except Exception as e:
            status_label.config(text=f"❌ Lỗi: {str(e)}", fg=COLORS["red"])
        finally:
            copy_button.config(state="normal")
    
    # --- Header ---
    header_frame = Frame(root, bg=MAIN_APP_BG, padx=30, pady=20)
    header_frame.pack(fill=X)
    
    # Title và logout button
    title_frame = Frame(header_frame, bg=MAIN_APP_BG)
    title_frame.pack(fill=X, pady=(0, 10))
    
    title_label = Label(title_frame, text="Auto Find Photo", 
                       font=("Arial", 24, "bold"), bg=MAIN_APP_BG, fg=COLORS["white"])
    title_label.pack(side=LEFT)
    
    def logout():
        clear_auth_data()
        root.destroy()
        import login_screen
        login_screen.show_login_screen()
    
    logout_button = Button(title_frame, text="Đăng xuất", command=logout,
                          font=("Arial", 10), bg=COLORS["red"], fg=COLORS["white"],
                          padx=15, pady=6, cursor="hand2", relief="flat", bd=0,
                          activebackground=COLORS["red_dark"], activeforeground=COLORS["white"])
    logout_button.pack(side=RIGHT)
    
    # --- Card container ---
    card_container = Frame(root, bg=MAIN_APP_BG, padx=30, pady=10)
    card_container.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Card chính
    main_card = Frame(card_container, bg=MAIN_APP_CARD_BG, padx=30, pady=25)
    main_card.pack(fill=BOTH, expand=True)
    
    # Section: Chọn thư mục
    folder_section = Frame(main_card, bg=MAIN_APP_CARD_BG)
    folder_section.pack(fill=X, pady=(0, 20))
    
    Label(folder_section, text="📁 Thư mục nguồn", 
          font=("Arial", 12, "bold"), bg=MAIN_APP_CARD_BG, fg=COLORS["white"]).pack(anchor="w", pady=(0, 10))
    
    folder_button_frame = Frame(folder_section, bg=MAIN_APP_CARD_BG)
    folder_button_frame.pack(fill=X)
    
    select_source_button = Button(folder_button_frame, text="Chọn thư mục nguồn", 
                                  command=select_source_folder, 
                                  font=("Arial", 11, "bold"), bg=COLORS["teal"], fg=COLORS["white"],
                                  padx=20, pady=10, cursor="hand2", relief="flat", bd=0,
                                  activebackground=COLORS["teal_dark"], activeforeground=COLORS["white"])
    select_source_button.pack(side=LEFT, padx=(0, 10))
    
    source_display = Label(folder_button_frame, text="Chưa chọn thư mục", 
                          font=("Arial", 10), bg=MAIN_APP_CARD_BG, fg=COLORS["gray"],
                          anchor="w", wraplength=500)
    source_display.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))
    
    
    # Section: Tìm kiếm ảnh
    search_section = Frame(main_card, bg=MAIN_APP_CARD_BG)
    search_section.pack(fill=X, pady=(0, 20))
    
    Label(search_section, text="🔍 Tìm kiếm ảnh", 
          font=("Arial", 12, "bold"), bg=MAIN_APP_CARD_BG, fg=COLORS["white"]).pack(anchor="w", pady=(0, 10))
    
    search_input_frame = Frame(search_section, bg=MAIN_APP_CARD_BG)
    search_input_frame.pack(fill=X)
    
    name_entry = Entry(search_input_frame, font=("Arial", 11), bg=COLORS["darker_bg"], 
                       fg=COLORS["white"], insertbackground=COLORS["white"],
                       relief="flat", bd=0, highlightthickness=1, 
                       highlightbackground=COLORS["teal"], highlightcolor=COLORS["teal"])
    name_entry.pack(side=LEFT, fill=X, expand=True, ipady=10, padx=(0, 10))
    name_entry.insert(0, "Nhập tên ảnh (cách nhau bằng dấu phẩy)")
    name_entry.config(fg=COLORS["gray"])
    
    def on_entry_focus_in(event):
        if name_entry.get() == "Nhập tên ảnh (cách nhau bằng dấu phẩy)":
            name_entry.delete(0, END)
            name_entry.config(fg=COLORS["white"])
    
    def on_entry_focus_out(event):
        if not name_entry.get():
            name_entry.insert(0, "Nhập tên ảnh (cách nhau bằng dấu phẩy)")
            name_entry.config(fg=COLORS["gray"])
    
    name_entry.bind("<FocusIn>", on_entry_focus_in)
    name_entry.bind("<FocusOut>", on_entry_focus_out)
    
    filter_button = Button(search_input_frame, text="Tìm kiếm", command=filter_images,
                          font=("Arial", 11, "bold"), bg=COLORS["red"], fg=COLORS["white"],
                          padx=25, pady=10, cursor="hand2", relief="flat", bd=0,
                          activebackground=COLORS["red_dark"], activeforeground=COLORS["white"])
    filter_button.pack(side=RIGHT)
    
    # Section: Danh sách ảnh
    list_section = Frame(main_card, bg=MAIN_APP_CARD_BG)
    list_section.pack(fill=BOTH, expand=True, pady=(0, 20))
    
    list_header = Frame(list_section, bg=MAIN_APP_CARD_BG)
    list_header.pack(fill=X, pady=(0, 10))
    
    Label(list_header, text="📋 Danh sách ảnh đã tìm thấy", 
          font=("Arial", 12, "bold"), bg=MAIN_APP_CARD_BG, fg=COLORS["white"]).pack(side=LEFT)
    
    count_label = Label(list_header, text="(0 ảnh)", 
                       font=("Arial", 10), bg=MAIN_APP_CARD_BG, fg=COLORS["gray"])
    count_label.pack(side=LEFT, padx=(10, 0))
    
    # Frame cho listbox và scrollbar
    listbox_frame = Frame(list_section, bg=COLORS["darker_bg"], relief="flat", bd=0)
    listbox_frame.pack(fill=BOTH, expand=True)
    
    scrollbar = Scrollbar(listbox_frame, bg=COLORS["darker_bg"], 
                         troughcolor=COLORS["darker_bg"],
                         activebackground=COLORS["teal"])
    scrollbar.pack(side=RIGHT, fill=Y)
    
    listbox = Listbox(listbox_frame, font=("Arial", 10), bg=COLORS["darker_bg"], 
                     fg=COLORS["white"], selectbackground=COLORS["teal"],
                     selectforeground=COLORS["white"], relief="flat", bd=0,
                     highlightthickness=0, yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
    scrollbar.config(command=listbox.yview)
    
    
    # Section: Actions
    action_section = Frame(main_card, bg=MAIN_APP_CARD_BG)
    action_section.pack(fill=X)
    
    copy_button = Button(action_section, text="💾 Sao chép sang thư mục đích", 
                         command=copy_images, font=("Arial", 12, "bold"), 
                         padx=30, pady=12, bg=COLORS["green"], fg=COLORS["white"],
                         cursor="hand2", relief="flat", bd=0,
                         activebackground="#45a049", activeforeground=COLORS["white"])
    copy_button.pack(pady=(0, 10))
    
    status_label = Label(action_section, text="Sẵn sàng", font=("Arial", 10), 
                         bg=MAIN_APP_CARD_BG, fg=COLORS["gray"], wraplength=800)
    status_label.pack(pady=5)
    
    root.mainloop()


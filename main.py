import os
import shutil
from tkinter import Tk, Label, Button, Entry, filedialog, Listbox, END, Scrollbar, RIGHT, Y, LEFT, BOTH

# --- Khởi tạo cửa sổ ---
root = Tk()
root.title("Sao chép ảnh nâng cao")
root.geometry("600x450")

image_list = []
source_folder = ""

# --- Chọn thư mục nguồn ---
def select_source_folder():
    global source_folder
    folder = filedialog.askdirectory(title="Chọn thư mục chứa ảnh")
    if folder:
        source_folder = folder
        status_label.config(text=f"Thư mục nguồn: {source_folder}")
        listbox.delete(0, END)

# --- Lọc ảnh theo tên ---
def filter_images():
    global image_list
    listbox.delete(0, END)
    image_list = []
    if not source_folder:
        status_label.config(text="Vui lòng chọn thư mục nguồn trước!")
        return
    # Lấy tên nhập
    names_input = name_entry.get()
    if not names_input:
        status_label.config(text="Vui lòng nhập tên ảnh muốn copy!")
        return
    names = [n.strip() for n in names_input.split(",") if n.strip()]
    # Lọc file trong folder
    for file in os.listdir(source_folder):
        if file in names or os.path.splitext(file)[0] in names:
            full_path = os.path.join(source_folder, file)
            if os.path.isfile(full_path):
                image_list.append(full_path)
                listbox.insert(END, file)
    status_label.config(text=f"Tìm thấy {len(image_list)} ảnh")

# --- Chọn thư mục đích và copy ---
def copy_images():
    if not image_list:
        status_label.config(text="Không có ảnh để copy!")
        return
    dest_folder = filedialog.askdirectory(title="Chọn thư mục đích")
    if not dest_folder:
        return
    for file in image_list:
        shutil.copy(file, dest_folder)
    status_label.config(text=f"Sao chép {len(image_list)} ảnh xong!")

# --- Giao diện ---
Label(root, text="Nhập tên ảnh (cách nhau bằng dấu ,)").pack(pady=5)
name_entry = Entry(root, width=60)
name_entry.pack(pady=5)

select_source_button = Button(root, text="Chọn thư mục nguồn", command=select_source_folder)
select_source_button.pack(pady=5)

filter_button = Button(root, text="Lọc ảnh theo tên", command=filter_images)
filter_button.pack(pady=5)

# Listbox + scrollbar
frame_list = Listbox(root, width=70, height=10)
frame_list.pack(pady=10)

listbox = Listbox(root, width=70, height=10)
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
listbox.pack(pady=10, fill=BOTH, expand=True)

copy_button = Button(root, text="Sao chép sang thư mục đích", command=copy_images)
copy_button.pack(pady=10)

status_label = Label(root, text="")
status_label.pack(pady=5)

root.mainloop()

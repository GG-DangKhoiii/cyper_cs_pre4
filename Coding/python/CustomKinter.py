import customtkinter as ctk

# Tạo cửa sổ chính
DK = ctk.CTk()

# yêu cầu 1: tạo kích thước cho giao diện
#DK.geometry("700x300")

# yêu cầu 1: khóa kích thước của giao diện 
#DK.resizable(False,False)


DK.title("dangkhoiii") 


khung = ctk.CTkFrame(DK)
khung.pack(padx=20, pady=20, expand=True, fill="both")

thanhtruot = ctk.CTkScrollbar(khung)
thanhtruot.pack(side="right", fill="y")


canvas = ctk.CTkCanvas(khung, yscrollcommand=thanhtruot.set)
canvas.pack(side="left", fill="both", expand=True)
thanhtruot.configure(command=canvas.yview)

product_frame = ctk.CTkFrame(canvas)
canvas.create_window((0, 0), window=product_frame, anchor="nw")

iphone = ["iPhone 12", "iPhone 13", "iPhone 14", "iPhone 15", "iPhone SE", "iPhone 11", "iPhone XR", "iPhone 8", "iPhone XS", "iPhone 7","iPhone 6", "iPhone 5" ]


for i, product in enumerate(iphone):
    button = ctk.CTkButton(product_frame, text=product)
    button.grid(row=i // 4, column=i % 4, padx=10, pady=10)  


product_frame.update_idletasks() 
canvas.config(scrollregion=canvas.bbox("all")) 

# Chạy ứng dụng GUI
DK.mainloop()

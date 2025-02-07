import customtkinter as ctk
from PIL import Image, ImageTk  


DK = ctk.CTk()

# Đặt kích thước cửa sổ là 300x500 pixel theo yêu cầu ở slide 1 
#DK.geometry("500x300")
# Khóa kích thước của giao diện trong yêu cầu ở slide 1 
#DK.resizable(False, False)


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


iphone = ["iPhone 17", "iPhone 16", "iPhone 15", "iPhone 14", "iPhone 13", "iPhone 12", "iPhone 11", "iPhone 10", "iPhone 8", "iPhone 7", "iPhone 6", "iPhone 5"]
iphone_images = {
    "iPhone 17": "images/ip17.jpg",  
    "iPhone 16": "images/ip16.jpg", 
    "iPhone 15": "images/ip15.jpg",
    "iPhone 14": "images/ip14.jpg",
    "iPhone 13": "images/ip13.jpg",
    "iPhone 12": "images/ip12.jpg",
    "iPhone 11": "images/ip11.jpg",
    "iPhone 10": "images/ip10.jpg",
    "iPhone 8": "images/ip8.jpg",
    "iPhone 7": "images/ip7.jpg",
    "iPhone 6": "images/ip6.jpg",
    "iPhone 5": "images/ip5.jpg"
}


img_storage = {}


def show_image(product_name):
    image_path = iphone_images.get(product_name)
    if image_path:
        img = Image.open(image_path) 
        img = img.resize((200, 200))  
        img = ImageTk.PhotoImage(img)  
        img_storage[product_name] = img  
        image_label.configure(image=img)
        image_label.image = img  


image_label = ctk.CTkLabel(DK)
image_label.pack(padx=20, pady=20)


button_images = {}
for i, product in enumerate(iphone):
    img = Image.open(iphone_images[product]) 
    img = img.resize((100, 100))  
    img = ImageTk.PhotoImage(img)  
    button_images[product] = img 
    button = ctk.CTkButton(product_frame, image=img, text=product, compound="top", command=lambda p=product: show_image(p))
    button.grid(row=i // 4, column=i % 4, padx=10, pady=10)  

product_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))


DK.mainloop()

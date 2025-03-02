import requests
import json
import random
import time
from pprint import pprint

url = "https://ecomws.didongviet.vn/fe/v1/products"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}


params = {
    "category_ids": [4],  
    "orderBy": "position",
    "orderType": "ASC",
    "page": 1,
    "limit": 10
}


iphone_list = []
max_products = 1000  
max_pages = 5  

for page in range(1, max_pages + 1):
    if len(iphone_list) >= max_products:
        print("Đã thu thập đủ số lượng sản phẩm!")
        break

    # Cập nhật số trang trong params
    params["page"] = page

    # Gửi yêu cầu lấy dữ liệu từ API
    response = requests.get(url, headers=headers, params=params)

    # Kiểm tra lỗi HTTP
    if response.status_code != 200:
        print(f"Lỗi {response.status_code} khi lấy dữ liệu từ trang {page}")
        continue

    # Chuyển dữ liệu sang JSON
    try:
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))  
    except json.JSONDecodeError:
        print(f"Lỗi giải mã JSON từ API!")
        continue

    #  Kiểm tra dữ liệu hợp lệ
    if "data" not in data or "data" not in data["data"]:
        print(f"Không tìm thấy danh sách sản phẩm trên trang {page}!")
        continue

    items = data["data"]["data"]  

    # Lặp qua từng sản phẩm và trích xuất thông tin
    for item in items:
        iphone_item = {
            "product_id": item.get("product_id"),
            "product": item.get("product"),
            "slug": item.get("slug"),
            "url": f"https://didongviet.vn/{item.get('url')}", 
            "thumbnail": f"https://didongviet.vn/{item.get('thumbnail')}",
            "position": item.get("position"),
            "page_title": item.get("page_title"),
            "price": item.get("price")
        }
        iphone_list.append(iphone_item)

  
    print(f"Đã lấy {len(items)} sản phẩm từ trang {page}")

    # Dừng ngẫu nhiên 1 - 5 giây để tránh bị chặn
    delay = random.randint(1, 5)
    print(f" Chờ {delay} giây trước khi tiếp tục...")
    time.sleep(delay)

# Ghi danh sách iPhone vào file JSON
with open("iphone_data.json", "w", encoding="utf-8") as file:
    json.dump(iphone_list, file, ensure_ascii=False, indent=4)

print("Ghi dữ liệu thành công vào iphone_data.json!")

# Lọc các sản phẩm iPhone trong khoảng giá
min_price = 10000000  # 10 triệu VND
max_price = 25000000 # 20 triệu VND


# Chuyển đổi giá thành số nguyên & lọc sản phẩm theo khoảng giá
filtered_iphones = [
    {"product": iphone["product"], "price": int(iphone["price"])}
    for iphone in iphone_list
    if iphone["price"] and min_price <= int(iphone["price"]) <= max_price  
]

# In danh sách iPhone đã lọc
print("iphone_filtered =", end=" ")
pprint(filtered_iphones)


#Yeucau2
tree_types = {
    "Top Left": "Skeweded Binary Tree",
    "Top Right": "Compelte Binary Tree",
    "Bottom Left": "Full Binary Tree",
    "Bottom Right": "Perfect Binary Tree"
}

print("Danh sách các loại cây trong hình:")
for position, tree_name in tree_types.items():
    print(f"- {position}: {tree_name}")

#yeucau345

class Node:
    def __init__(self, price, product):
        self.key = price  # Giá để sắp xếp
        self.product = product
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, price, product):
        if self.root is None:
            self.root = Node(price, product)
        else:
            self._insert_recursive(self.root, price, product)

    def _insert_recursive(self, node, price, product):
        if price < node.key:
            if node.left is None:
                node.left = Node(price, product)
            else:
                self._insert_recursive(node.left, price, product)
        else:
            if node.right is None:
                node.right = Node(price, product)
            else:
                self._insert_recursive(node.right, price, product)

    """PHƯƠNG THỨC DUYỆT CÂY"""
    def traverse(self, type):
        if type == 1:  # Preorder
            print("\n Preorder Traversal:")
            self.preorder(self.root)
        elif type == 2:  # Inorder
            print("\n Inorder Traversal:")
            self.inorder(self.root)
        elif type == 3:  # Postorder
            print("\n Postorder Traversal:")
            self.postorder(self.root)

    """ PREORDER: Root → Left → Right """
    def preorder(self, node):
        if node:
            print(f"{node.product} ({node.key} VND)", end=" → ")
            self.preorder(node.left)
            self.preorder(node.right)

    """ INORDER: Left → Root → Right """
    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(f"{node.product} ({node.key} VND)", end=" → ")
            self.inorder(node.right)

    """ POSTORDER: Left → Right → Root """
    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(f"{node.product} ({node.key} VND)", end=" → ")

# Xây dựng BST
bst = BinaryTree()
for iphone in filtered_iphones:
    bst.insert(iphone["price"], iphone["product"])

# Duyệt cây theo 3 kiểu
bst.traverse(1)  # Preorder
bst.traverse(2)  # Inorder
bst.traverse(3)  # Postorder





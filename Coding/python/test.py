# Đây là đoạn code python, dùng để tìm ra phần tử nhỏ thứ k trong cây nhị phân?
# Hãy điền vào ô trống để đoạn code hoạt động được.
from typing import Optional
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class Solution:
    def find_kth_smallest_element(self, root: Optional[TreeNode], k: int) -> int:
        if not root:
            return -1
 
        left_size = count_nodes(root.left)

        if left_size + 1 == k:
            return root.val
        elif left_size >= k:
            return self.find_kth_smallest_element(root.left, k)
        else:
            return self.find_kth_smallest_element(root.right, k - left_size - 1)


def count_nodes(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    return 1 + count_nodes(root.left) + count_nodes(root.right)


def insert(root: Optional[TreeNode], val: int) -> TreeNode:
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

# Tạo cây BST bằng cách chèn lần lượt các giá trị
def create_tree():
    root = None
    values = [5, 3, 7, 2, 4, 8]  # Các giá trị cần chèn vào BST
    for val in values:
        root = insert(root, val)
    return root

# Test
root = create_tree()
k = 3
solution = Solution()
result = solution.find_kth_smallest_element(root, k)
print(f"Phần tử nhỏ thứ {k} trong BST là: {result}")
# Đây là đoạn code python, dùng để kiểm tra xem cây nhị phân có cân bằng hay không?
# Hãy điền vào ô trống để đoạn code hoạt động được.

from typing import Optional
class TreeNode:
   def __init__(self, val: int):
       self.val = val
       self.left: Optional[TreeNode] = None
       self.right: Optional[TreeNode] = None


class Solution:
    def is_balanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        
 
        left_height = height(root.left)
        right_height = height(root.right)

        if abs(left_height - right_height) > 1:
            return False

        return self.is_balanced(root.left) and self.is_balanced(root.right)


def height(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    return 1 + max(height(root.left), height(root.right))




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
    values = [5, 3, 7, 2, 1]  # Các giá trị cần chèn vào BST
    for val in values:
        root = insert(root, val)
    return root

# Test
root = create_tree()
solution = Solution()
result = solution.is_balanced(root)
print(f"cây có cân bằng không?: đáp án  {result}")
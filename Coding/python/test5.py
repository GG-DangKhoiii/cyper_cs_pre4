# Đây là đoạn code python, dùng để tìm ra xem cây nhị phân có đường dẫn nào có tổng bằng k hay không?
# Hãy điền vào ô trống để đoạn code hoạt động được.
from typing import Optional

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

class Solution:
    def find_path_sum_to_k(self, root: Optional[TreeNode], k: int) -> bool:
        if not root:
            return False
        
        # Điền vào ô trống để kiểm tra nếu k đã bằng 0
        if k == 0:
            return True

        if root.val == k and not root.left and not root.right:
            return True

        return self.find_path_sum_to_k(root.left, k - root.val) or self.find_path_sum_to_k(root.right, k - root.val)

    
        # Test với cây đã cho
def create_tree():
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.right.right = TreeNode(1)
    return root

root = create_tree()
solution = Solution()
k = 55
result = solution.find_path_sum_to_k(root, k)
print(f"Có đường nào tổng bằng {k} không? Đáp án: {result}")
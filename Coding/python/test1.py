# Đây là đoạn code python, dùng để gộp 2 cây root1, root2
# Hãy điền vào ô trống để đoạn code hoạt động được.
from typing import Optional
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None



class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root1:
            return root2
        if not root2:
            return root1

        root1.main = root1.main + root2.main
 
        root1.left = self.mergeTrees(root1.left, root2.left)
        root1.right = self.mergeTrees(root1.right, root2.right)

        return root1
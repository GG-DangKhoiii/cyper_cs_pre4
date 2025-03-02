from typing import Optional
class TreeNode:
   def __init__(self, val: int):
       self.val = val
       self.left: Optional[TreeNode] = None
       self.right: Optional[TreeNode] = None

class Solution:
    def max_depth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

 
        left_depth = self.max_depth(root.left)
        right_depth = self.max_depth(root.right)
        max_depth = max(left_depth, right_depth) + 1

        return max_depth


def create_tree():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    return root

root = create_tree()
solution = Solution()
print("Tổng nhị phân của cây là:", solution.max_depth(root))
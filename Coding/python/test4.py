# Cho trước gốc của một cây nhị phân và một số nguyên targetSum, hãy trả về True 
# nếu cây có một đường từ gốc đến lá sao cho tổng giá trị trên đường đi đó 
# bằng targetSum. 

# Hãy điền vào ô trống để đoạn code thực thi.
from typing import Optional
class TreeNode:
   def __init__(self, val: int):
       self.val = val
       self.left: Optional[TreeNode] = None
       self.right: Optional[TreeNode] = None

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if root is None:
            return False
        if root.left is None and root.right is None:
            return root.val == targetSum
        def sum(node,s,S):
            if node.left is None and node.right is None:
                S.append(s)
            if node.left is not None:
                sum(node.left,s+node.left.val,S)
            if node.right is not None:
                sum(node.right,s+node.right.val,S)
            return S
        return targetSum in sum(root, root.val, [])


    
    
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
targetSum = 22
result = solution.hasPathSum(root, targetSum)
print(f"Có đường nào tổng bằng {targetSum} không? Đáp án: {result}")
 
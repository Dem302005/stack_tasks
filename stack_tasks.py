from collections import deque
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(values: list) -> Optional[TreeNode]:
    """Допоміжна функція: дерево з масиву в форматі LeetCode (обхід по рівнях, None = null)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

# 1
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack

# 2
def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    result, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        result.append(node.val)
        node = node.right
    return result

# 3
class MinStack:
    def __init__(self):
        self._stack = []

    def push(self, val: int) -> None:
        current_min = val if not self._stack else min(val, self._stack[-1][1])
        self._stack.append((val, current_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def getMin(self) -> int:
        return self._stack[-1][1]

# 4
class MyQueue:
    def __init__(self):
        self._in = []
        self._out = []

    def push(self, x: int) -> None:
        self._in.append(x)

    def _move(self) -> None:
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())

    def pop(self) -> int:
        self._move()
        return self._out.pop()

    def peek(self) -> int:
        self._move()
        return self._out[-1]

    def empty(self) -> bool:
        return not self._in and not self._out

# 5
def decode_string(s: str) -> str:
    stack = []
    cur, num = "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, num))
            cur, num = "", 0
        elif ch == "]":
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur

# 6
def eval_rpn(tokens: List[str]) -> int:
    def divide(a: int, b: int) -> int:
        q = abs(a) // abs(b)
        return q if (a < 0) == (b < 0) else -q

    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": divide,
    }
    stack = []
    for t in tokens:
        if t in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[t](a, b))
        else:
            stack.append(int(t))
    return stack[0]

# 7
def longest_valid_parentheses(s: str) -> int:
    stack = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best

if __name__ == "__main__":
    # 1
    assert is_valid("()") is True
    assert is_valid("()[]{}") is True
    assert is_valid("(]") is False
    assert is_valid("([)]") is False
    assert is_valid("{[]}") is True
    assert is_valid("(") is False
    assert is_valid("]") is False
    # 2
    assert inorder_traversal(build_tree([1, None, 2, 3])) == [1, 3, 2]
    assert inorder_traversal(build_tree([])) == []
    assert inorder_traversal(build_tree([1])) == [1]
    # 3
    ms = MinStack()
    ms.push(-2); ms.push(0); ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2
    # 4
    q = MyQueue()
    q.push(1); q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    assert q.empty() is False
    assert q.pop() == 2
    assert q.empty() is True
    # 5
    assert decode_string("3[a]2[bc]") == "aaabcbc"
    assert decode_string("3[a2[c]]") == "accaccacc"
    assert decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert decode_string("10[a]") == "a" * 10
    # 6
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert eval_rpn(["7", "-2", "/"]) == -3
    # 7
    assert longest_valid_parentheses("(()") == 2
    assert longest_valid_parentheses(")()())") == 4
    assert longest_valid_parentheses("") == 0
    assert longest_valid_parentheses("()(()") == 2

    print("Усі тести пройдено")
import pandas as pd

class AVLNode:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = [value]  # Store a list of values for the same key
        self.left = left
        self.right = right
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def update_height(self, node):
        if not node:
            return 0
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self.update_height(z)
        self.update_height(y)

        return y

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def insert(self, root, key, value):
        if not root:
            return AVLNode(key, value)

        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            # Duplicate keys are allowed, store multiple values in a list
            root.value.append(value)
            return root

        self.update_height(root)

        # Check and balance the tree
        balance = self.balance_factor(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def insert_node(self, key, value):
        self.root = self.insert(self.root, key, value)

    def dfs(self, start_date, end_date):
        expenditures = []
        stack = [self.root]

        while stack:
            current = stack.pop()
            if current:
                date = int(current.key)
                if start_date <= date <= end_date:
                    expenditures.extend(current.value)
                if date >= start_date:
                    stack.append(current.left)
                if date <= end_date:
                    stack.append(current.right)

        return expenditures

    def bfs(self, start_date, end_date):
        expenditures = []
        queue = [self.root]

        while queue:
            current = queue.pop(0)
            if current:
                date = int(current.key)
                if start_date <= date <= end_date:
                    expenditures.extend(current.value)
                if date >= start_date:
                    queue.append(current.left)
                if date <= end_date:
                    queue.append(current.right)

        return expenditures


    def search(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def search_by_key(self, key):
        node = self.search(self.root, key)
        return node.value if node else None

def main():
    avl = AVLTree()

    headers = ['date', 'expenditure', 'category']
    df = pd.read_csv('data_A.csv', names=headers)

    for index, row in df.iterrows():
        avl.insert_node(str(row['date']), (int(row['expenditure']), str(row['category'])))

    target_start = int(input("시작 날짜 입력: "))
    target_end = int(input("종료 날짜 입력: "))

    ## DFS
    print("--------DFS---------")
    print("\n-----지출 내역------")
    for expenditure, category in avl.dfs(target_start, target_end):
        print(f"지출금액(원): {expenditure}, 카테고리: {category}")

    ## BFS
    print("\n\n--------BFS--------")
    print("\n-----지출 내역------")    
    for expenditure, category in avl.bfs(target_start, target_end):
        print(f"지출금액(원): {expenditure}, 카테고리: {category}")


    '''
    target = str(input("시작날짜 입력: "))
    result = avl.search_by_key(target)
    if result:
        for value in result:
            print(f"비용: {value[0]}, 카테고리: {value[1]}")
    else:
        print(f"{target}에 해당하는 데이터가 없습니다.")
    '''
        
if __name__ == "__main__":
    main()
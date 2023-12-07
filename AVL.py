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
        self.comparison_count_dfs = 0
        self.comparison_count_bfs = 0

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
        category_totals = {}  # 카테고리별 누적 합계를 저장할 딕셔너리

        stack = [self.root]

        while stack:
            self.comparison_count_dfs+=1
            current = stack.pop()
            if current:
                self.comparison_count_dfs+=1
                date = int(current.key)
                if start_date <= date <= end_date:
                    self.comparison_count_dfs+=1
                    for value in current.value:
                        self.comparison_count_dfs+=1
                        expenditure, category = value
                        expenditures.append((expenditure, category))  # 지출 내역을 리스트에 추가
                        if category in category_totals:
                            self.comparison_count_dfs+=1
                            category_totals[category] += expenditure
                        else:
                            self.comparison_count_dfs+=1
                            category_totals[category] = expenditure

                if date >= start_date:
                    self.comparison_count_dfs+=1
                    stack.append(current.left)
                if date <= end_date:
                    self.comparison_count_dfs+=1
                    stack.append(current.right)

        print("\n[       DFS       ]")
        print("-----지출 내역------")        
        for expenditure, category in expenditures:
            print(f"지출금액(원): {expenditure}, 카테고리: {category}")

        print("\n----누적 지출금액----")
        for category, total_expenditure in category_totals.items():
            print(f"카테고리: {category}, 누적 지출금액(원): {total_expenditure}")

        return expenditures, category_totals,self.comparison_count_dfs

    def bfs(self, start_date, end_date):
        expenditures = []
        category_totals = {}  # 카테고리별 누적 합계를 저장할 딕셔너리
        queue = [self.root]

        while queue:
            self.comparison_count_bfs+=1
            current = queue.pop(0)
            if current:
                self.comparison_count_bfs+=1
                date = int(current.key)
                if start_date <= date <= end_date:
                    self.comparison_count_bfs+=1
                    for value in current.value:
                        self.comparison_count_bfs+=1
                        expenditure, category = value
                        expenditures.append((expenditure, category))  # 지출 내역을 리스트에 추가
                        if category in category_totals:
                            self.comparison_count_bfs+=1
                            category_totals[category] += expenditure
                        else:
                            self.comparison_count_bfs+=1
                            category_totals[category] = expenditure
                if date >= start_date:
                    self.comparison_count_bfs+=1
                    queue.append(current.left)
                if date <= end_date:
                    self.comparison_count_bfs+=1
                    queue.append(current.right)

        print("\n\n[       BFS       ]")
        print("-----지출 내역------")          
        for expenditure, category in expenditures:
            print(f"지출금액(원): {expenditure}, 카테고리: {category}")

        print("\n----누적 지출금액----")
        for category, total_expenditure in category_totals.items():
            print(f"카테고리: {category}, 누적 지출금액(원): {total_expenditure}")

        return expenditures, category_totals, self.comparison_count_bfs

def main():
    avl = AVLTree()

    headers = ['date', 'expenditure', 'category']
    df = pd.read_csv('data_A.csv', names=headers)

    for index, row in df.iterrows():
        avl.insert_node(str(row['date']), (int(row['expenditure']), str(row['category'])))

    target_start = int(input("시작 날짜 입력: "))
    target_end = int(input("종료 날짜 입력: "))

    ## DFS
    dfs_expenditures, dfs_category_totals, dfs_compare_count = avl.dfs(target_start, target_end)

    max_category_dfs = max(dfs_category_totals, key=dfs_category_totals.get)
    max_expenditure_dfs = dfs_category_totals[max_category_dfs]
    total_expenditure_dfs = sum(dfs_category_totals.values())
    percentage_dfs = (max_expenditure_dfs / total_expenditure_dfs) * 100 if total_expenditure_dfs > 0 else 0

    print(f"\n'{target_start}'~'{target_end}' 중 가장 많은 지출 분야는 {percentage_dfs:.2f}% 비율로 {max_category_dfs}분야입니다.")

    print("-----------------")
    print(f"\nDFS 비교 연산 횟수: {dfs_compare_count}")

    ## BFS
    bfs_expenditures, bfs_category_totals, bfs_compare_count = avl.bfs(target_start, target_end)

    max_category_bfs = max(bfs_category_totals, key=bfs_category_totals.get)
    max_expenditure_bfs = bfs_category_totals[max_category_bfs]
    total_expenditure_bfs = sum(bfs_category_totals.values())
    percentage_bfs = (max_expenditure_bfs / total_expenditure_bfs) * 100 if total_expenditure_bfs > 0 else 0

    print(f"\n'{target_start}'~'{target_end}' 중 가장 많은 지출 분야는 {percentage_bfs:.2f}% 비율로 {max_category_bfs}분야입니다.")

    print("-----------------")
    print(f"\nBFS 비교 연산 횟수: {bfs_compare_count}")        

if __name__ == "__main__":
    main()
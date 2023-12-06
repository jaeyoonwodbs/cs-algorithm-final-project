import pandas as pd

class Node:
    def __init__(self, key, height, left=None, right=None):
        self.key = key
        self.height = height
        self.left = left
        self.right = right

class AVL:
    def __init__(self):
        self.root = None
    def height(self, n):
        if n == None:
            return 0
        return n.height

    def put(self, key):
        self.root = self.put_item(self.root, key)

    def put_item(self, n, key):
        if n == None:
            return  Node(key, 1)
        if n.key > key:
            n.left = self.put_item(n.left, key)
        elif n.key < key:
            n.right = self.put_item(n.right, key)
        n.height = max(self.height(n.left), self.height(n.right))+1
        return self.balance(n)

    def balance(self, n):

        if self.bf(n) > 1: # 왼쪽 서브트리 불균형
            if self.bf(n.left) < 0: # 노드 n의 왼쪽 자식의 오른쪽 서브트리가 높은 경우
                n.left = self.rotate_left(n.left) # LR
            n = self.rotate_right(n) # LL

        elif self.bf(n) < -1: # 오른쪽 서브트리 불균형
            if self.bf(n.right) > 0: # 노드 n의 오른쪽 자식의 왼쪽 서브트리가 높은 경우
                n.right = self.rotate_right(n.right) #RL
            n = self.rotate_left(n) #RR
        return n

    def bf(self, n):
        return self.height(n.left)-self.height(n.right)

    def rotate_right(self, n): #오른쪽 회전
        x = n.left
        n.left = x.right
        x.right = n
        n.height = max(self.height(n.left), self.height(n.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    def rotate_left(self, n): #왼쪽 회전
        x = n.right
        n.right = x.left
        x.left = n
        n.height = max(self.height(n.left), self.height(n.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    def preorder(self, n):
        print(str(n.key),' ', end="")
        if n.left:
            self.preorder(n.left)
        if n.right:
            self.preorder(n.right)
    def inorder(self, n):
        if n.left:
            self.inorder(n.left)
        print(str(n.key), ' ', end="")
        if n.right:
            self.inorder(n.right)

def main():
    avl = AVL()

    headers=['date','expenditure','category']
    df=pd.read_csv('account_book.csv',names=headers)
    
    for index, row in df.iterrows():
        avl.put(int(row['expenditure']))
    
    avl.inorder(avl.root)
    print("\n")

    #수정예정!!

if __name__=="__main__":
    main()
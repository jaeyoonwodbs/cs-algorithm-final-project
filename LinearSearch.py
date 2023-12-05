#Sequential Search
class Hash:
    def __init__(self):
        self.hash_table = {}

    def push(self, key, value1, value2):
        if key in self.hash_table:
            self.hash_table[key].append([value1, value2])
        else:
            self.hash_table[key] = [[value1, value2]]

    def get_values(self, key):
        return self.hash_table[key]

    def linear_search(self, target):
        if target in self.hash_table:
            return self.hash_table[target]
        return None
    
import pandas as pd

def main():
    hash_table = Hash()
    
    headers=['date','expenditure','category']
    df = pd.read_csv('account_book.csv', names=headers)
    
    # 해시테이블 생성: 1개의 key값에 여러개의 value값 갖게 함. (날짜, 금액, 카테고리) 순으로 삽입
    for index, row in df.iterrows():
        hash_table.push(int(row['date']), int(row['expenditure']), int(row['category']))
        
    target = int(input("날짜 입력: "))

    found_data = hash_table.linear_search(target)

    if found_data is not None:
        for entry in found_data:
            print(f"지출금액(원): {entry[0]}, 카테고리: {entry[1]}")
    else:
        print("해당 날짜의 데이터가 없습니다.")

if __name__ == "__main__":
    main()

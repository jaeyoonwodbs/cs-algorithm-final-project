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
            original_entries = self.hash_table[target]
            result = {}
            for entry in original_entries:
                category = entry[1]
                expenditure = entry[0]
                if category in result:
                    result[category] += expenditure
                else:
                    result[category] = expenditure
            return original_entries, result
        return None, None

import pandas as pd

def main():
    hash_table = Hash()
    
    headers=['date','expenditure','category']
    df = pd.read_csv('account_book.csv', names=headers)
    
    # 해시테이블 생성: 1개의 key값에 여러개의 value값 갖게 함. (날짜, 금액, 카테고리) 순으로 삽입
    for index, row in df.iterrows():
        hash_table.push(str(row['date']), int(row['expenditure']), int(row['category']))
        
    target = str(input("날짜 입력: "))

    original_entries, cumulative_expenditures = hash_table.linear_search(target)

    if original_entries is not None:
        print("-----지출 내역------")
        for entry in original_entries:
            print(f"지출금액(원): {entry[0]}, 카테고리: {entry[1]}")
        
        print("\n-----누적 지출금액-----")
        for category, cumulative_expenditure in cumulative_expenditures.items():
            print(f"카테고리: {category}, 누적 지출금액(원): {cumulative_expenditure}")
    else:
        print("해당 날짜의 지출이 없습니다.")

if __name__ == "__main__":
    main()

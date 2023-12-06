class Hash:
    def __init__(self):
        self.hash_table = {}

    def push(self, key, value1, value2):
        if key in self.hash_table:
            self.hash_table[key].append([value1, value2])
            self.hash_table[key] = sorted(self.hash_table[key], key=lambda x: x[1])  # Sort entries based on category
        else:
            self.hash_table[key] = [[value1, value2]]

    def get_values(self, key):
        return self.hash_table[key]

    def binary_search(self, entries, target_category):
        low, high = 0, len(entries) - 1
        cumulative_sum = 0  # To keep track of the cumulative sum

        while low <= high:
            mid = (low + high) // 2
            mid_category = entries[mid][1]

            if mid_category == target_category:
                # Calculate cumulative sum for the found category
                for i in range(mid + 1):
                    cumulative_sum += entries[i][0]
                return cumulative_sum
            elif mid_category < target_category:
                low = mid + 1
            else:
                high = mid - 1

        return 0  # Return 0 if the category is not found

import pandas as pd

def main():
    hash_table = Hash()
    
    headers=['date','expenditure','category']
    df = pd.read_csv('account_book.csv', names=headers)
    
    # 해시테이블 생성: 1개의 key값에 여러개의 value값 갖게 함. (날짜, 금액, 카테고리) 순으로 삽입
    for index, row in df.iterrows():
        hash_table.push(str(row['date']), int(row['expenditure']), int(row['category']))
        
    target=str(input("날짜 입력: "))

    if target in hash_table.hash_table:
        original_entries = hash_table.hash_table[target]
        
        print("-----지출 내역------")
        for entry in original_entries:
            print(f"지출금액(원): {entry[0]}, 카테고리: {entry[1]}")
        
        print("\n-----누적 지출금액-----")
        cumulative_expenditures = {}
        for entry in original_entries:
            category = entry[1]
            cumulative_expenditure = hash_table.binary_search(original_entries, category)
            cumulative_expenditures[category] = cumulative_expenditure
        
        for category, cumulative_expenditure in cumulative_expenditures.items():
            print(f"카테고리: {category}, 누적 지출금액(원): {cumulative_expenditure}")
    else:
        print("해당 날짜의 지출이 없습니다.")

if __name__ == "__main__":
    main()
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

    def binary_search(self, keys, target, start, end):
        while start <= end:
            mid = (start + end) // 2
            if keys[mid] == target:
                return mid
            elif keys[mid] < target:
                start = mid + 1
            else:
                end = mid - 1
        return start

    def search_range(self, target_start, target_end):
        result = {}
        original_entries = []

        keys = sorted(self.hash_table.keys())  

        start_index = self.binary_search(keys, target_start, 0, len(keys) - 1)
        end_index = self.binary_search(keys, target_end, 0, len(keys) - 1)

        for key in keys[start_index : end_index + 1]:
            entries = self.hash_table[key]
            original_entries.extend(entries)
            for entry in entries:
                category = entry[1]
                expenditure = entry[0]
                if category in result:
                    result[category] += expenditure
                else:
                    result[category] = expenditure

        return original_entries, result

import pandas as pd

def main():
    hash_table = Hash()

    headers = ['date', 'expenditure', 'category']
    df = pd.read_csv('data_A.csv', names=headers)

    for index, row in df.iterrows():
        hash_table.push(str(row['date']), int(row['expenditure']), str(row['category']))

    target_start = str(input("시작 날짜 입력: "))
    target_end = str(input("종료 날짜 입력: "))

    original_entries, cumulative_expenditures = hash_table.search_range(target_start, target_end)

    if original_entries:
        print("-----지출 내역------")
        for entry in original_entries:
            print(f"지출금액(원): {entry[0]}, 카테고리: {entry[1]}")

        print("\n-----누적 지출금액-----")
        for category, cumulative_expenditure in cumulative_expenditures.items():
            print(f"카테고리: {category}, 누적 지출금액(원): {cumulative_expenditure}")
        
        # Calculate category with the highest expenditure
        max_category = max(cumulative_expenditures, key=cumulative_expenditures.get)
        max_expenditure = cumulative_expenditures[max_category]
        total_expenditure = sum(cumulative_expenditures.values())
        percentage = (max_expenditure / total_expenditure) * 100

        print(f"\n'{target_start}'~'{target_end}' 중 가장 많은 지출 분야는 {percentage:.2f}% 비율로 {max_category}분야입니다.")
    else:
        print("해당 기간의 지출이 없습니다.")

if __name__ == "__main__":
    main()

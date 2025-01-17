'''
Created on 2025/01/10

@author: Anali
'''
import json
import os

# テストデータ
test_data = {
    "name": "Test User",
    "age": 30,
    "city": "Tokyo",
    "hobbies": ["reading", "traveling", "cooking"]
}

# 保存先のパス
save_path = os.path.join("C:/workspace2/MyPythonProject", "test_data.json")

# JSONファイルに保存
with open(save_path, 'w', encoding='utf-8') as file:
    json.dump(test_data, file, ensure_ascii=False, indent=4)

print(f"テストデータが {save_path} に保存されました。")

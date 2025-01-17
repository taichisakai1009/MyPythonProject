import google.generativeai as genai
import sys
import io
import os
import json

# 標準出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 環境変数からAPIキーを取得
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEYが環境変数に設定されていません")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 履歴ファイルのパス
history_file = 'chat_history.json'

# 履歴を読み込む
if os.path.exists(history_file):
    with open(history_file, 'r', encoding='utf-8') as file:
        history = json.load(file)
else:
    history = []

input_text = sys.argv[1] if len(sys.argv) > 1 else ""
last_four_chars = input_text[-4:] #最後の4文字を取得
# .lower()で全て小文字に変換
if last_four_chars.lower() == "exit":
    if os.path.exists(history_file):
        os.remove(history_file)
    print("会話を終了し、履歴ファイルを消去しました。")
    sys.exit(0)

chat = model.start_chat(history=history)
response = chat.send_message(input_text)

# 応答と履歴の更新 期待される形式にしないとエラー
history.append({'role': 'user', 'parts': [{'text': input_text}]})
history.append({'role': 'model', 'parts': [{'text': response.text}]})

# 履歴をファイルに保存
with open(history_file, 'w', encoding='utf-8') as file:
    json.dump(history, file, ensure_ascii=False, indent=4)

print(response.text)

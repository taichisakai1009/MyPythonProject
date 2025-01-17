'''
Created on 2025/01/09

@author: Anali
'''
import mysql.connector
import sys
import io
import os

# 標準出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 履歴ファイルのパス
# history_file = 'chat_history.json'

# 履歴を読み込む(会話中だったら取得しない)
# if os.path.exists(history_file):
#     sys.exit(0)

def get_comments():
    # データベース接続
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Taichi235711",
        database="orderSystemDB",
        charset="utf8mb4"  # UTF8エンコーディング
    )
    cursor = conn.cursor()
    
    cursor.execute("SET NAMES 'utf8mb4';")

    # データ取得
    cursor.execute("SELECT * FROM comments where comment_id <= 90")
    comments = cursor.fetchall()

    # コンソール出力
    print("---- コメント一覧 ----")
    for comment in comments:
        print(f"ID: {comment[0]}, コメント: {comment[1]}, 日付: {comment[2]}")
        
    print("この感想を基に、次の質問に答えてください。")

    # 接続を閉じる
    conn.close()
    return comments  # 必要なら返す


# 関数呼び出し
if __name__ == "__main__":
    get_comments()

import matplotlib.pyplot as plt
import sys

# コマンドライン引数を受け取る
args = sys.argv[1:]  # スクリプト名を除く

# 引数を数値リストに変換
hours = list(map(float, args[0].split(',')))  # x軸のデータ
visitor_count = list(map(float, args[1].split(',')))  # y軸のデータ

# 折れ線グラフを描画
plt.plot(hours, visitor_count, marker='o', linestyle='-', color='b', label='Visitor Count')

# グラフのタイトルとラベルを設定
plt.title('Visitor Count per Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Visitors')

# グリッド線を表示
plt.grid(True)

# 凡例を表示
plt.legend()

# グラフを表示
plt.show()

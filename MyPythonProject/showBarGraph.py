import matplotlib.pyplot as plt
from packaging.version import Version  # setuptools互換
import japanize_matplotlib
import matplotlib.dates as mdates
import sys
from datetime import datetime

# コマンドライン引数を受け取る
args = sys.argv[1:]  # スクリプト名を除く

# 引数を数値リストに変換
hours = list(map(str, args[0].split(',')))  # x軸のデータ
visitor_count = list(map(float, args[1].split(',')))  # y軸のデータ

print("py.hours:", hours, "py.visitor_count:", visitor_count)

# 時刻データをdatetimeオブジェクトに変換
time_data = [datetime.strptime(hour, "%H:%M") for hour in hours]

# グラフの作成
fig, ax = plt.subplots(figsize=(10, 6))

# 横幅が細い棒グラフを作成
ax.bar(time_data, visitor_count, width=0.03)  # widthで棒の横幅を設定

# 横軸のフォーマットを設定
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # 時間表示をHH:MM形式に
ax.xaxis.set_major_locator(mdates.HourLocator())  # 1時間ごとに目盛りを設定

# 縦軸（y-axis）を整数表示に設定
from matplotlib.ticker import MaxNLocator
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# グラフのタイトルとラベル
plt.title("今日の混雑状況")
plt.xlabel("時刻")
plt.ylabel("利用者数（人）")

# グラフを表示
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

print("グラフ表示")

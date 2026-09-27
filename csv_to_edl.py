import csv
import re

# --- 設定 ---
CSV_FILE = "markers.csv"       # 入力するCSVファイル名
EDL_FILE = "markers.edl"       # 出力するEDLファイル名
FPS = "60"                     # フレームレート (例: 24, 30, 60 などプロジェクトに合致させる)

import csv

CSV_FILE = "markers.csv"
EDL_FILE = "markers.edl"

def fix_tc(tc):
    """タイムコードを 00:00:00:00 に絶対整形する関数"""
    parts = tc.strip().split(':')
    if len(parts) == 2:      # 分:秒 (例 01:23) -> 00:01:23:00
        return f"00:{parts[0].zfill(2)}:{parts[1].zfill(2)}:00"
    elif len(parts) == 3:    # 時:分:秒 (例 00:01:23) -> 00:01:23:00
        return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:{parts[2].zfill(2)}:00"
    elif len(parts) == 4:    # すでに 00:00:00:00
        return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:{parts[2].zfill(2)}:{parts[3].zfill(2)}"
    return "00:00:00:00"

def convert_csv_to_edl():
    markers = []

    # UTF-8で読み込み
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # 1行目をスキップ

        for row in reader:
            if not row or len(row) < 1:
                continue

            tc_raw = row[0]
            name = row[1].strip() if len(row) > 1 else "Cut"
            color = row[2].strip().capitalize() if len(row) > 2 else "Blue"

            tc_in = fix_tc(tc_raw)
            markers.append((tc_in, name, color))

    # UTF-8 (BOMなし) で書き出し
    with open(EDL_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("TITLE: DAVINCI_MARKERS\n")
        f.write("FCM: NON-DROP FRAME\n\n")

        for idx, (tc, name, color) in enumerate(markers, 1):
            num = f"{idx:03d}"
            f.write(f"{num}  001      V     C        {tc} {tc} {tc} {tc}\n")
            f.write(f" |C:ResolveColor_{color} |M:{name} |D:1\n\n")

    print(f"✨ 完璧なEDLができました！: {EDL_FILE}")

if __name__ == "__main__":
    convert_csv_to_edl()

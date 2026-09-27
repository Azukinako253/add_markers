import csv
import sys

# DaVinci Resolve Scripting APIのパスを追加
resolve_script_api = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
if resolve_script_api not in sys.path:
    sys.path.append(resolve_script_api)

import DaVinciResolveScript as dvr

# 設定
FPS = 30  # タイムラインのフレームレート（あなたのプロジェクトに合わせて変更してください）
CSV_PATH = r"C:\Users\kenjiro\Desktop\Davinci_Projects\add_markers\markers.csv"
  # ★ここをあなたのCSVのパスに変える

def time_to_frames(time_str, fps=FPS):
    """
    時間文字列（例: 1:40 または 0:01:40）をフレーム数に変換
    """
    parts = time_str.strip().split(":")
    if len(parts) == 2:  # 分:秒
        minutes = int(parts[0])
        seconds = float(parts[1])
        total_seconds = minutes * 60 + seconds
    elif len(parts) == 3:  # 時:分:秒
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")
    return int(total_seconds * fps)

# DaVinci Resolveに接続
resolve = dvr.scriptapp("Resolve")
if not resolve:
    raise RuntimeError("DaVinci Resolveに接続できませんでした。Resolveが起動しているか確認してください。")

project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
if not project:
    raise RuntimeError("プロジェクトが開かれていません。")

timeline = project.GetCurrentTimeline()
if not timeline:
    raise RuntimeError("タイムラインが開かれていません。")

# CSVからマーカーを追加
marker_count = 0
with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frame = time_to_frames(row["time"])
        name = row["name"]
        note = row["note"]
        color = row["color"]

        # マーカーを追加
        timeline.AddMarker(frame, color, name, note, 1)
        marker_count += 1
        print(f"マーカー追加: {row['time']} ({frame}フレーム) - {name} - {color}")

print(f"\n完了！ {marker_count}個のマーカーを追加しました。")

import csv

CSV_FILE = "calling_english_lyrics.csv"
SRT_FILE = "calling_english_lyrics.srt"

def tc_to_srt_time(tc):
    """
    どんな形式のタイムコードでもSRT形式 (00:00:00,000) に変換する超頑丈な関数
    """
    parts = tc.strip().split(':')

    # 0:00:10 などの場合
    if len(parts) == 3:
        h, m, s = map(int, parts)
        f = 0
    # 00:00:10:12 などの場合
    elif len(parts) == 4:
        h, m, s, f = map(int, parts)
    # 00:10 などの場合
    elif len(parts) == 2:
        h = 0
        m, s = map(int, parts)
        f = 0
    else:
        return "00:00:00,000"

    # フレーム(24fps想定)をミリ秒に変換
    ms = int(f * (1000 / 24))

    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def generate_srt():
    with open(CSV_FILE, "r", encoding="utf-8-sig") as infile, \
         open(SRT_FILE, "w", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        header = next(reader, None)  # 1行目(Start, End, Text)をスキップ

        idx = 1
        for row in reader:
            if not row or len(row) < 3:
                continue

            start_tc = row[0].strip()
            end_tc = row[1].strip()
            text = row[2].strip()

            srt_start = tc_to_srt_time(start_tc)
            srt_end = tc_to_srt_time(end_tc)

            outfile.write(f"{idx}\n")
            outfile.write(f"{srt_start} --> {srt_end}\n")
            outfile.write(f"{text}\n\n")
            idx += 1

    print(f"✨ 字幕ファイル '{SRT_FILE}' の作成が完了しました！")

if __name__ == "__main__":
    generate_srt()

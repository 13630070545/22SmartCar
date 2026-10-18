
import csv
import os
import math

INPUT_FILE = "sensor_data.csv"
OUTPUT_FILE = "cleaned_data.csv"
OUTPUT_DIR = "out"  # 输出目录

data = []
times = []
cleaned = []

print("=== 传感器数据分析 ===")

# --- 读取数据 ---
reader = csv.DictReader(open(INPUT_FILE, "r"))

for row in reader:
    t = float(row["time"])
    v = float(row["value"])
    times.append(t)
    data.append(v)

print("共读取 %d 条数据" % len(data))

# --- 计算平均值 ---
total = 0
for v in data:
    total += v
mean = total / len(data)

# --- 计算标准差 ---
acc = 0
for v in data:
    acc += (v - mean)**2

std = math.sqrt(acc / len(data))

# --- 剔除离群值 ---
for v in data:
    if abs(v - mean) <= 2 * std:
        cleaned.append(v)

        

# --- 输出清洗后的数据 ---
output_path = os.path.join("/", OUTPUT_DIR, OUTPUT_FILE)
f = open(output_path, "w")
writer = csv.writer(f)
writer.writerow(["time", "value"])
for v in cleaned:
    writer.writerow([v])

print("均值 mean = %.4f" % mean)
print("标准差 std = %.4f" % std)
print("清洗后剩余 %d 条" % len(cleaned))
print("已保存到 %s" % output_path)

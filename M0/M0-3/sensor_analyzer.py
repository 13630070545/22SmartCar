
import csv
import os
import math

INPUT_FILE = "sensor_data.csv"
OUTPUT_FILE = "cleaned_data.csv"

data = []
times = []
cleaned = []

print("=== 传感器数据分析 ===")

# --- 读取数据 ---
try:
    with open(INPUT_FILE, "r", encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file)

        for row in reader:
            t = float(row["time"])
            v = float(row["value"])
            if not math.isfinite(t) or not math.isfinite(v):
                raise ValueError("time 和 value 不能是 NaN 或无穷大")

            times.append(t)
            data.append(v)

except FileNotFoundError:
    print("错误：找不到输入文件：", INPUT_FILE) #找不到文件
    raise SystemExit(1)

except KeyError as error:
    print("错误：CSV 中缺少必要列：", error) #缺列
    raise SystemExit(1)

except (ValueError, TypeError) as error:
    print(f"错误：CSV 第 {reader.line_num} 行数据无效：{error}") 
    raise SystemExit(1)

except OSError as error:
    print(f"错误：无法读取输入文件 {INPUT_FILE}：{error}")
    raise SystemExit(1)


print("共读取 %d 条数据" % len(data))

if not data:
    print("错误：CSV 中没有可供分析的数据") #空数据
    raise SystemExit(1)

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
for t, v in zip(times, data):
    if abs(v - mean) <= 2 * std:
        cleaned.append((t, v))

        

# --- 输出清洗后的数据 ---
output_path = OUTPUT_FILE

try:
    with open(output_path, "w", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["time", "value"])

        for t, v in cleaned:
            writer.writerow([t, v])

except OSError as error:
    print(f"错误：无法写入输出文件 {output_path}：{error}") #写入失败
    raise SystemExit(1)

print("均值 mean = %.4f" % mean)
print("标准差 std = %.4f" % std)
print("清洗后剩余 %d 条" % len(cleaned))
print("已保存到 %s" % output_path)

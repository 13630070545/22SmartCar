import yaml
import csv
import math

def parse_number(value, line_no, column_name):
    if value is None or value.strip() == "":
        raise ValueError(
            f"CSV 第 {line_no} 行，列 {column_name} 的值为空" #f+{}可以达到替换的效果
        )

    try:
        number = float(value)
    except ValueError:
        raise ValueError(
            f"CSV 第 {line_no} 行，列 {column_name} 不是数字：{value}"
        )

    if not math.isfinite(number): #判断数字的有限性，有限时返回ture，取反保证下方报错成立
        raise ValueError(
            f"CSV 第 {line_no} 行，列 {column_name} 必须是有限数值：{value}"
        )

    return number  #处理行号和列名，防止乱七八糟的值来当



CONFIG_PATH = "config.yaml"#读取配置文件

try:
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)
except FileNotFoundError:
    print("错误：找不到配置文件：", CONFIG_PATH)   #处理配置文件不存在
    raise SystemExit(1)

except yaml.YAMLError:
    print("错误：配置文件的 YAML 格式不正确，请检查缩进和冒号")  #格式错误或文件为空
    raise SystemExit(1)

if cfg is None:
    print("错误：配置文件为空，或只有注释") #继续处理空文件is None
    raise SystemExit(1)

csv_path = cfg["input_csv"]
col_x = cfg["columns"]["x"]
col_y = cfg["columns"]["y"]

xs = []
ys = []

try:
    with open(csv_path) as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            raise ValueError("CSV 文件为空，或没有表头")

        if col_x not in reader.fieldnames:
            raise KeyError(col_x)

        if col_y not in reader.fieldnames:
            raise KeyError(col_y)

        for row in reader:
            line_no = reader.line_num
            xs.append(parse_number(row[col_x], line_no, col_x))  #调用定义的读数据函数
            ys.append(parse_number(row[col_y], line_no, col_y))

        for row in reader:
            line_no = reader.line_num
            xs.append(parse_number(row[col_x], line_no, col_x))
            ys.append(parse_number(row[col_y], line_no, col_y))

except FileNotFoundError:
    print("错误：找不到 CSV 文件：", csv_path) #文件不存在
    raise SystemExit(1)  
except KeyError as error:
    print("错误：CSV 中找不到列：", error) #缺列
    raise SystemExit(1)
except ValueError as error:
    print("错误：", error)
    raise SystemExit(1)



def calculate_correlation(xs,ys):
    n = len(xs)

    if n != len(ys):
        raise ValueError("两列数据的数量必须相同")

    if n < 2:
        raise ValueError("计算相关系数至少需要两组数据")

    sum_x = 0.0
    sum_y = 0.0
    for i in range(n):
        sum_x = sum_x + xs[i]
        sum_y = sum_y + ys[i]    #求和


    mean_x = sum_x / n
    mean_y = sum_y / n    #求平均数

    dx = 0.0
    dy = 0.0
    prod = 0.0
    for i in range(n):
        a = xs[i] - mean_x
        b = ys[i] - mean_y   #求偏差
        dx = dx + a * a    
        dy = dy + b * b
        prod = prod + a * b  #分子
    if dx == 0 or dy == 0:
        raise ValueError("某一列的值全部相同，无法计算相关系数")

    denom = math.sqrt(dx * dy)  #原式忘记开方
    r = prod / denom
    return n ,mean_x,mean_y, r


try:
    n, mean_x, mean_y, r = calculate_correlation(xs, ys)

    print("n =", n)
    print("mean_x =", mean_x)
    print("mean_y =", mean_y)
    print("r =", r)
except ValueError as error:  
    print("错误：", error)
    raise SystemExit(1)    #错误输出
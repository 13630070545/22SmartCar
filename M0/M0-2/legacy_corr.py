import yaml
import csv
import math
import numpy as np

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

try:
    csv_path = cfg["input_csv"]
    col_x = cfg["columns"]["x"]
    col_y = cfg["columns"]["y"]
except KeyError as error:
    print("错误：配置文件缺少配置项：", error)
    raise SystemExit(1)

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
            
except FileNotFoundError:
    print("错误：找不到 CSV 文件：", csv_path) #文件不存在
    raise SystemExit(1)  
except KeyError as error:
    print("错误：CSV 中找不到列：", error) #缺列
    raise SystemExit(1)
except ValueError as error:
    print("错误：", error)
    raise SystemExit(1)



def calculate_correlation(xs, ys):
    n = len(xs)

    if n != len(ys):
        raise ValueError("两列数据的数量必须相同")

    if n < 2:
        raise ValueError("计算相关系数至少需要两组数据")

    if not all(math.isfinite(x) for x in xs):
        raise ValueError("第一列包含非有限数值")

    if not all(math.isfinite(y) for y in ys):
        raise ValueError("第二列包含非有限数值")

   
    offset_x = xs[0]
    offset_y = ys[0] #用首项作为参考

    shifted_x = [x - offset_x for x in xs] #平移， 留下有差异的部分，放大数据间的差异（对数据差异小的数据有效果）
    shifted_y = [y - offset_y for y in ys]

    # 正负极大值相减可能溢出，此时放弃该列的平移
    if not all(math.isfinite(x) for x in shifted_x): #检查平移后的数值是否有限，平移后溢出将直接缩放
        offset_x = 0.0
        shifted_x = xs[:]

    if not all(math.isfinite(y) for y in shifted_y):
        offset_y = 0.0
        shifted_y = ys[:]

    
    scale_x = max(abs(x) for x in shifted_x)
    scale_y = max(abs(y) for y in shifted_y)  #缩放，避免值溢出，也能增加精度

    if scale_x == 0 or scale_y == 0:
        raise ValueError("某一列的值全部相同，无法计算相关系数")

    scaled_x = [x / scale_x for x in shifted_x]
    scaled_y = [y / scale_y for y in shifted_y]

    mean_x_scaled = math.fsum(scaled_x) / n  #求平均
    mean_y_scaled = math.fsum(scaled_y) / n

    
    centered_x = [x - mean_x_scaled for x in scaled_x]  #求偏差
    centered_y = [y - mean_y_scaled for y in scaled_y]

    
    dx = math.fsum(a * a for a in centered_x)  #求分子
    dy = math.fsum(b * b for b in centered_y)
    prod = math.fsum(
        centered_x[i] * centered_y[i] for i in range(n)
    )

    if dx == 0 or dy == 0:
        raise ValueError("某一列的方差为零，无法计算相关系数")

    denom = math.sqrt(dx) * math.sqrt(dy) #求分母
    r = prod / denom

    
    mean_x = offset_x + mean_x_scaled * scale_x  #还原平均值
    mean_y = offset_y + mean_y_scaled * scale_y

    return n, mean_x, mean_y, r

try:
    n, mean_x, mean_y, r = calculate_correlation(xs, ys)

    print("n =", n)
    print("mean_x =", mean_x)
    print("mean_y =", mean_y)
    print("r =", r)

    numpy_r = float(np.corrcoef(xs, ys)[0, 1])
    print("NumPy r =", numpy_r)



    if math.isfinite(r) and math.isfinite(numpy_r):
        difference = abs(r - numpy_r)
        print("绝对误差 =", difference)
        print("精度检查：", "通过" if difference <= 1e-6 else "未通过")
    else:
        print("精度检查：结果中有非有限数值，无法比较")


except ValueError as error:  
    print("错误：", error)
    raise SystemExit(1)    #错误输出

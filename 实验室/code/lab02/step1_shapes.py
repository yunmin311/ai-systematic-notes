import numpy as np

a = np.arange(12).reshape(3, 4)   # 3 行 4 列
b = np.array([10, 20, 30])        # 长度 3 的一维数组

print("a.shape =", a.shape)
print("b.shape =", b.shape)

try:
    print(a + b)
except ValueError as e:
    print("报错:", e)

# 修法:把 b 变成 (3,1),让它按「列」广播到每一行
b2 = b.reshape(-1, 1)
print("b2.shape =", b2.shape)
print("a + b2 =")
print(a + b2)

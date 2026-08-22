import numpy as np

K = np.array([[1, 0, 1, 0],      # 猫
              [0, 1, 0, 1],      # 追
              [1, 0, 0, 1]])     # 老鼠
V = np.array([[10, 0],           # 猫
              [0, 10],           # 追
              [5, 5]])           # 老鼠
q = np.array([1, 0, 1, 0])       # 查询:老鼠
d_k = K.shape[1]                 # = 4

scores = q @ K.T
print("① 打分 (q·K^T)      =", scores)

scaled = scores / np.sqrt(d_k)
print("② 缩放 (÷√d_k, √4=2) =", scaled)

e = np.exp(scaled - scaled.max())        # 减最大值,防溢出,不改变结果
weights = e / e.sum()
print("③ softmax 权重       =", np.round(weights, 4))
print("   权重之和           =", round(weights.sum(), 6))

out = weights @ V
print("④ 加权求和 → 输出    =", np.round(out, 4))
print()
print("讲义第 9 节用两位小数手算得到 [6.65, 3.45];代码的精确值见上。")

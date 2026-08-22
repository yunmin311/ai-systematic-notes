import numpy as np

K = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]])
Q = K.copy()                     # 自注意力:每个词都当一次查询
d_k = K.shape[1]

scores = (Q @ K.T) / np.sqrt(d_k)
print("缩放后的分数矩阵(行=谁在查,列=查谁):")
print(np.round(scores, 3))

mask = np.triu(np.ones_like(scores, dtype=bool), k=1)   # 上三角 = 未来
masked = scores.copy()
masked[mask] = -np.inf
print("\n加上因果掩码之后(-inf 表示不许看):")
print(masked)

e = np.exp(masked - masked.max(axis=1, keepdims=True))
w = e / e.sum(axis=1, keepdims=True)
print("\nsoftmax 之后的权重矩阵:")
print(np.round(w, 4))
print("\n每一行之和:", np.round(w.sum(axis=1), 6))

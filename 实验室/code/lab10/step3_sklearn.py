import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([50, 60, 80, 100, 120, 150], dtype=float).reshape(-1, 1)  # sklearn 要二维
y = np.array([155, 182, 235, 290, 348, 430], dtype=float)

model = LinearRegression()
model.fit(X, y)                                  # 就这一行,训练完成了

print(f"sklearn 给出:  w = {model.coef_[0]:.4f}   b = {model.intercept_:.4f}")
print(f"第 1 步手算:   w = 2.7565   b = 16.0561")
print(f"R² = {model.score(X, y):.6f}   ← 1.0 表示完全贴合\n")

# 多个特征时,闭式解的手写公式会变麻烦,而 sklearn 的接口不变
X2 = np.array([[50, 2], [60, 2], [80, 3], [100, 3], [120, 4], [150, 4]], dtype=float)  # 面积 + 卧室数
m2 = LinearRegression().fit(X2, y)
print(f"两个特征时:    面积系数 {m2.coef_[0]:.3f}   卧室系数 {m2.coef_[1]:.3f}   截距 {m2.intercept_:.3f}")
print(f"R² = {m2.score(X2, y):.6f}")
print("\n注意卧室数的系数——它很小甚至可能为负,因为面积和卧室数高度相关。")
print("这不代表卧室不重要,是多重共线性的典型表现;这时单个系数没法单独解读。")

import numpy as np

# 六套房:面积(㎡) → 总价(万元)
X = np.array([50, 60, 80, 100, 120, 150], dtype=float)
y = np.array([155, 182, 235, 290, 348, 430], dtype=float)

x_bar, y_bar = X.mean(), y.mean()

# 最小二乘闭式解:w = Σ(x-x̄)(y-ȳ) / Σ(x-x̄)²
w = ((X - x_bar) * (y - y_bar)).sum() / ((X - x_bar) ** 2).sum()
b = y_bar - w * x_bar
print(f"闭式解直接给出:  w = {w:.4f}   b = {b:.4f}")
print(f"也就是:  总价 ≈ {w:.2f} × 面积 + {b:.1f}\n")

pred = w * X + b
print("面积     真实     预测     残差(预测-真实)")
for xi, yi, pi in zip(X, y, pred):
    print(f"{xi:5.0f}  {yi:7.1f}  {pi:7.1f}  {pi - yi:+8.2f}")

mse = ((pred - y) ** 2).mean()
print(f"\nMSE(均方误差) = {mse:.2f}")
print(f"残差之和 = {(pred - y).sum():.2f}   ← 几乎为 0,这是最小二乘的必然结果")
print(f"\n外推:95㎡ → {w * 95 + b:.1f} 万元")

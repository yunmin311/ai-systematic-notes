import numpy as np

X = np.array([50, 60, 80, 100, 120, 150], dtype=float)
y = np.array([155, 182, 235, 290, 348, 430], dtype=float)

# 先做标准化:两列都换成标准分(减均值、除标准差)
# 原因很实在——原始尺度下 w 的梯度是 b 的上百倍,一个学习率顾不住两个旋钮。
x_bar, x_std = X.mean(), X.std()
y_bar, y_std = y.mean(), y.std()
Xs = (X - x_bar) / x_std
ys = (y - y_bar) / y_std

w, b = 0.0, 0.0          # 两个旋钮都从 0 起步
lr = 0.1                 # 步长:每轮沿梯度方向挪多远

print("轮次      w        b        MSE       dw")
for epoch in range(0, 61):
    pred = w * Xs + b
    err = pred - ys
    mse = (err ** 2).mean()
    dw = (2 / len(Xs)) * (err * Xs).sum()      # MSE 对 w 的偏导
    db = (2 / len(Xs)) * err.sum()             # MSE 对 b 的偏导
    if epoch % 10 == 0:
        print(f"{epoch:4d}  {w:8.4f}  {b:8.4f}  {mse:8.4f}  {dw:9.4f}")
    w -= lr * dw                               # 往梯度的反方向挪一小步
    b -= lr * db

# 把标准化尺度下的 w、b 换算回「万元 / ㎡」
w_real = w * y_std / x_std
b_real = y_bar + y_std * b - w_real * x_bar
print(f"\n换算回原单位:  w = {w_real:.4f}   b = {b_real:.4f}")

w_closed = ((X - x_bar) * (y - y_bar)).sum() / ((X - x_bar) ** 2).sum()
b_closed = y_bar - w_closed * x_bar
print(f"第 1 步闭式解:  w = {w_closed:.4f}   b = {b_closed:.4f}")
print(f"两者相差:      w {abs(w_real - w_closed):.5f}   b {abs(b_real - b_closed):.5f}")

import numpy as np

rng = np.random.default_rng(0)
x = rng.uniform(-1, 1, 200)
y = 3 * x + 2 + rng.normal(0, 0.1, 200)      # 真实参数 w=3, b=2

w, b, lr = 0.0, 0.0, 0.1
for step in range(1, 201):
    # ① 前向:算预测
    pred = w * x + b
    # ② 算损失(均方误差)
    loss = ((pred - y) ** 2).mean()
    # ③ 算梯度(这一步就是框架要替代的)
    dw = (2 * (pred - y) * x).mean()
    db = (2 * (pred - y)).mean()
    # ④ 更新参数
    w -= lr * dw
    b -= lr * db
    if step % 50 == 0:
        print(f"step {step:3d}  loss={loss:.5f}  w={w:.4f}  b={b:.4f}")

print("\n手写版最终: w =", round(w, 4), " b =", round(b, 4))

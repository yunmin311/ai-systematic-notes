import numpy as np
np.random.seed(0)

# XOR:两个输入不一样才输出 1。它没法用一条直线分开,逼着网络必须有隐藏层。
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)

# 2 → 4(隐藏层)→ 1 的小网络
W1 = np.random.randn(2, 4); b1 = np.zeros((1, 4))
W2 = np.random.randn(4, 1); b2 = np.zeros((1, 1))
lr = 0.5

def sigmoid(t): return 1 / (1 + np.exp(-t))
def dsigmoid(a): return a * (1 - a)          # sigmoid 的导数,用输出就能算

for epoch in range(10001):
    # ---- 前向:输入一层层传到最后 ----
    a1 = sigmoid(X @ W1 + b1)
    a2 = sigmoid(a1 @ W2 + b2)
    loss = ((a2 - y) ** 2).mean()

    if epoch % 2000 == 0:
        acc = ((a2 > 0.5).astype(int) == y).mean()
        print(f"第 {epoch:5d} 轮   损失 {loss:.4f}   准确率 {acc * 100:3.0f}%")

    # ---- 反向:误差从最后一层往回传,顺便算出每个权重该改多少 ----
    d2 = (a2 - y) * dsigmoid(a2)                 # 输出层:错多少
    dW2 = a1.T @ d2 / len(X)
    db2 = d2.mean(axis=0, keepdims=True)
    d1 = (d2 @ W2.T) * dsigmoid(a1)              # 把误差传回隐藏层
    dW1 = X.T @ d1 / len(X)
    db1 = d1.mean(axis=0, keepdims=True)
    W2 -= lr * dW2; b2 -= lr * db2               # 往梯度的反方向挪
    W1 -= lr * dW1; b1 -= lr * db1

print("\n训练完之后,四条都过一遍:")
for xi, yi in zip(X, y):
    out = sigmoid(sigmoid(xi @ W1 + b1) @ W2 + b2)[0, 0]
    print(f"   {xi.astype(int)} → 预测 {out:.3f}   真实 {yi[0]:.0f}   "
          f"{'✓' if (out > 0.5) == bool(yi[0]) else '✗'}")
print(f"\n一共 {W1.size + W2.size + b1.size + b2.size} 个可调参数 —— 真实模型是它的几十亿倍,但更新规则一模一样。")

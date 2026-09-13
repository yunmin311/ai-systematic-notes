weights = [1, 2, 3, 3]            # ← 混入了一条错误记录
prices  = [4.2, 7.9, 12.1, 50]    # ← 3kg 收了 50 元?!

def loss(w):
    total = 0
    for x, y in zip(weights, prices):
        error = y - w * x
        total += error ** 2
    return total / len(weights)

best_w, best_loss = 0, loss(0)
for i in range(20001):
    w = i * 0.001
    if loss(w) < best_loss:
        best_w, best_loss = w, loss(w)

print(f"学到的参数 w = {best_w:.3f},损失 = {best_loss:.4f}")
print(f"预测 5kg 运费:{best_w * 5:.2f} 元")

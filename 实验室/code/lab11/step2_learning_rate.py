def loss(w): return (w - 3) ** 2 + 2
def grad(w): return 2 * (w - 3)

def run(lr, steps=12, w0=0.0):
    w = w0
    trace = [w]
    for _ in range(steps):
        w = w - lr * grad(w)          # 就这一行:往梯度的反方向挪
        trace.append(w)
    return w, trace

print("学习率太小 / 正好 / 太大 / 过头,都从 w=0 跑 12 步:\n")
for lr, name in [(0.03, "太小  0.03"), (0.30, "正好  0.30"),
                 (0.90, "震荡  0.90"), (1.05, "过头  1.05")]:
    w, trace = run(lr)
    path = " → ".join(f"{t:.2f}" for t in trace[:7])
    print(f"lr = {name}   最终 w = {w:>9.4f}   最终损失 = {loss(w):>10.4f}")
    print(f"   前 6 步: {path}")
    print()

print("判据:每步的更新量是 lr × 梯度。这个例子里梯度 = 2(w-3),")
print("所以一步之后,误差(w-3)会变成原来的 (1 - 2×lr) 倍:")
for lr in (0.03, 0.30, 0.90, 1.05):
    r = 1 - 2 * lr
    if r >= 1 or r <= -1:   verdict = "发散——越跑越远"
    elif r < 0:             verdict = "震荡,但还在收敛"
    elif r < 0.5:           verdict = "收敛快"
    else:                   verdict = "收敛慢——步子太小"
    print(f"   lr={lr:<5} → 每步误差 ×{r:>6.2f}   {verdict}")

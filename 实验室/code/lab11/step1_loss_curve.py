# 把「训练」这件事拆到最简:只有一个旋钮 w
# 损失 = (w - 3)² + 2       ← 谷底在 w=3、损失=2,这是我们事先就知道的正确答案
def loss(w):
    return (w - 3) ** 2 + 2

def grad(w):
    return 2 * (w - 3)          # 损失对 w 的导数:正的表示 w 该往小调

print("  w      损失     梯度(往哪调)")
w = 0.0
while w <= 6.01:
    print(f"{w:5.1f}  {loss(w):8.3f}  {grad(w):+8.3f}")
    w += 0.5

best = min([(loss(x / 10), x / 10) for x in range(0, 61)])
print(f"\n扫一遍找到的最低点:  w = {best[1]:.1f}   损失 = {best[0]:.3f}")
print("这就是「穷举」——能找到答案,但 w 要是有一万个,这条路就走不通了。")

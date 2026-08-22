# step4_experiments.py —— 改参数,观察输出如何变化
# 运行方法:每完成一个 TODO 就跑一次  python step4_experiments.py
# 三个实验分别对应讲义 12.7 节的三个改动,一次只做一个,做完改回来再做下一个。

weights = [1, 2, 3]           # 实验 A:在两个列表末尾各加一个元素 → [1,2,3,3] 和 [...,50]
prices  = [4.2, 7.9, 12.1]    #        模拟“数据里混进一条错误记录”,观察 w 被拉到多大

def loss(w):
    total = 0
    for x, y in zip(weights, prices):
        error = y - w * x
        total += error ** 2
    return total / len(weights)

best_w, best_loss = 0, loss(0)
for i in range(20001):        # 实验 B:把 20001 改成 3001(只搜到 w=3.0),看 w 卡在哪
    w = i * 0.001             # 实验 C:把 0.001 改成 0.5(步子迈大),看精度掉到多少
    if loss(w) < best_loss:
        best_w, best_loss = w, loss(w)

print(f"学到的参数 w = {best_w:.3f},损失 = {best_loss:.4f}")
print(f"预测 5kg 运费:{best_w * 5:.2f} 元")

# 记录你的观察(直接写在下面的注释里):
# 实验 A:w 变成了 ____,预测变成了 ____ 元。一条脏数据的破坏力:____
# 实验 B:w 停在了 ____。说明:搜索范围不覆盖答案时,____
# 实验 C:w 只能取到 ____。说明:搜索粒度决定 ____

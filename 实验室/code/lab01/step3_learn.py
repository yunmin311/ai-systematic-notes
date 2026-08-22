# step3_learn.py —— 学习法:规律(参数 w)由数据自动决定
# 运行方法:python step3_learn.py
# 对应讲义:第 1 章 12.4 节

weights = [1, 2, 3]           # 数据:重量(kg),长度为 3 的列表
prices  = [4.2, 7.9, 12.1]    # 数据:实付运费(元),与上面一一对应

def loss(w):
    """算参数 w 的损失:预测得越离谱,返回值越大(均方误差)"""
    total = 0
    for x, y in zip(weights, prices):   # zip:每次取一对 (重量, 运费)
        error = y - w * x               # 公式里的 y_i − w·x_i
        total += error ** 2             # 平方(** 2)后累加,对应 Σ
    return total / len(weights)         # 除以样本数 n,取平均

# “学习” = 在候选参数里挑损失最小的那个(最笨但最直观的方法)
best_w, best_loss = 0, loss(0)
for i in range(20001):                  # 试遍 0.000, 0.001, …, 20.000
    w = i * 0.001
    if loss(w) < best_loss:             # 谁的损失更小,谁就是当前最优
        best_w, best_loss = w, loss(w)

print(f"学到的参数 w = {best_w:.3f},损失 = {best_loss:.4f}")
print(f"预测 5kg 运费:{best_w * 5:.2f} 元")

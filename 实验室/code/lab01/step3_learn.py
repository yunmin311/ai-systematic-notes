weights = [1, 2, 3]           # 数据:重量(kg)
prices  = [4.2, 7.9, 12.1]    # 数据:实付运费(元)

def loss(w):
    """算参数 w 的损失:预测越离谱,返回值越大"""
    total = 0
    for x, y in zip(weights, prices):   # 每次取一对 (重量, 运费)
        error = y - w * x               # 误差 = 真实 − 预测
        total += error ** 2             # 平方后累加
    return total / len(weights)         # 取平均

print(f"L(3.5) = {loss(3.5):.4f}")
print(f"L(4)   = {loss(4):.4f}")

import numpy as np
np.random.seed(0)

D = 32
LAYERS = 40

def make_sublayer():
    """一层子层(注意力 / 前馈)。缩放到谱范数 0.5:
       也就是说,单独过一层,信号会少一半。"""
    W = np.random.randn(D, D)
    return W * (0.5 / np.linalg.norm(W, 2))

def layernorm(x, eps=1e-5):
    """把每个位置的向量拉回「均值 0、方差 1」。注意它保证的是方差为 1,
       所以拉完之后向量的长度恒等于 √D —— 不长不短,正好是一个稳定的标尺。"""
    mu = x.mean(axis=-1, keepdims=True)
    sd = x.std(axis=-1, keepdims=True)
    return (x - mu) / (sd + eps)

W = make_sublayer()
x0 = np.random.randn(D); x0 /= np.linalg.norm(x0)

a, b, c = x0.copy(), x0.copy(), x0.copy()
print("同一个子层连堆 40 层,三种接法的信号强度(初始 = 100%):\n")
print("   层数    裸堆(无残差)   只加残差     残差 + 层归一化")
for i in range(1, LAYERS + 1):
    a = W @ a                              # 裸堆
    b = b + W @ b                          # 只加残差
    c = layernorm(c + W @ c)               # 残差 + 归一化(Transformer 的做法)
    if i in (1, 2, 5, 10, 20, 40):
        print(f"   {i:>4}   {np.linalg.norm(a)/np.linalg.norm(x0)*100:>12.6f}%"
              f"  {np.linalg.norm(b)/np.linalg.norm(x0)*100:>11.2f}%"
              f"  {np.linalg.norm(c)/np.linalg.norm(x0)*100:>14.4f}%")

print("\n三列三种命运,一个都不能少:")
print(f"   裸堆:       只剩 {np.linalg.norm(a)/np.linalg.norm(x0)*100:.6f}% —— 每层乘 0.5,40 层下来信号归零。")
print( "               浅层学到的东西传不到深层,梯度也传不回来。这就是「梯度消失」。")
print(f"   只加残差:   涨到 {np.linalg.norm(b)/np.linalg.norm(x0)*100:,.0f}% —— 走了另一个极端。")
print( "               残差是 (I + W),每层最多放大到 1.5 倍,层数一多就失控。")
print( "               所以「加个残差」本身不是解药,它只是把消失换成了爆炸。")
print(f"   残差+归一化:{np.linalg.norm(c)/np.linalg.norm(x0)*100:.4f}% —— 40 层之后纹丝不动。")
print(f"               这一列的数值和上面两列不同,是因为归一化的稳定点是 √32 = {np.sqrt(D):.3f},")
print( "               不是 1。真正要看的是它从第 1 层到第 40 层没变过——不涨也不落。")

print("\n这解释了 D15 为什么把「残差 + 层归一化」写成一个词:")
print("   残差负责「有一条系数为 1 的直达通道,梯度不用连乘几十个矩阵」;")
print("   归一化负责「把每层的结果拉回同一个尺度」,不让残差把数值堆上天。")
print("   两个一起用,才有「能堆几十上百层」这件事。")

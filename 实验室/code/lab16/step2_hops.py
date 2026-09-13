import numpy as np
np.random.seed(0)

D = 16
T = 20
print(f"序列长度 {T} 个词,每个词用 {D} 维向量表示\n")

X = np.random.randn(T, D)

# ---- 路线一:RNN,靠着循环一步步传 ----
Wh = np.random.randn(D, D) / np.sqrt(D)
Wh *= 0.9 / np.max(np.abs(np.linalg.eigvals(Wh)))   # 谱半径 0.9

def rnn_last(X):
    h = np.zeros(D)
    for x in X:
        h = np.tanh(Wh @ h + x)
    return h

# ---- 路线二:注意力,一步看全篇 ----
def attn_last(X):
    scores = X @ X.T / np.sqrt(D)                   # 每个词和每个词的匹配分数
    scores -= scores.max(axis=1, keepdims=True)
    A = np.exp(scores); A /= A.sum(axis=1, keepdims=True)   # softmax 成权重
    return (A @ X)[-1]                              # 取最后一个位置

# ---- 测量:改动第 1 个词,看最后那个词受影响多大 ----
def influence(fn):
    base = fn(X)
    Xp = X.copy(); Xp[0] += 1.0                     # 只动第 1 个词
    return np.abs(fn(Xp) - base).max()

inf_rnn, inf_attn = influence(rnn_last), influence(attn_last)

print("把「第 1 个词」改动 1.0,看它对「第 20 个词」的影响:")
print(f"   RNN       影响 = {inf_rnn:.6f}")
print(f"   注意力    影响 = {inf_attn:.6f}")
print(f"   相差       {inf_attn / inf_rnn:,.0f} 倍\n")

print("连接两个位置要走几步:")
print(f"   RNN       {T-1} 步 —— 第 1 个词的信息必须一站一站往右挪,每站都衰减一点")
print( "   注意力    1 步 —— 每对位置之间都是直连,第 20 个词可以一步回头看第 1 个词\n")

print("还有第二堵墙,不在『传多远』而在『能不能同时算』:")
print(f"   RNN       第 2 个词必须等第 1 个算完。{T} 个词就得排队 {T} 轮,长度越长越慢。")
print( "   注意力    整张分数矩阵一次算完(A @ X 就是一次矩阵乘),所有位置同时出结果。")
print( "\n两堵墙合起来,就是 D09 说的:注意力靠「任意两位置直连 + 可并行」甩开了 RNN,")
print( "成了今天所有大模型的地基。")

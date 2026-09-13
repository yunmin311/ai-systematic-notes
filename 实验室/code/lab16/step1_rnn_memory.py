import numpy as np
np.random.seed(0)

D = 8

Wx = np.random.randn(D, D) / np.sqrt(D)   # 输入 → 这一刻的记忆
Wh = np.random.randn(D, D) / np.sqrt(D)   # 上一刻的记忆 → 这一刻的记忆(下面会缩放)
Wh *= 0.9 / np.max(np.abs(np.linalg.eigvals(Wh)))   # 缩放到谱半径 0.9
b = np.zeros(D)

def rnn(X):
    h = np.zeros(D)                                   # 开工前记忆是空的
    hs = []
    for x in X:
        h = np.tanh(Wx @ x + Wh @ h + b)              # 新记忆 = 揉进「这个词」+「旧记忆」
        hs.append(h.copy())
    return np.array(hs)

seq = np.random.randn(6, D)
hs = rnn(seq)
print("每读一个词,记忆(前三维)就刷新一次:")
for t, h in enumerate(hs, 1):
    print(f"   读完第 {t} 个词: {np.round(h[:3], 4)}")

# ---- 关键:让记忆自己往下传,看它还剩多少 ----
# 演示用的循环矩阵换成正交矩阵 × 谱半径:这样每传一步,强度正好乘谱半径,
# 衰减/增长看得最干净(随机矩阵的特征值是复数,会出现先涨后落的假象)。
def trace(s, steps=20):
    Q, _ = np.linalg.qr(np.random.randn(D, D))        # 正交矩阵:不放大也不缩小
    W = Q * s                                         # 每乘一次,强度就乘 s
    h0 = np.random.randn(D); h0 /= np.linalg.norm(h0)
    h, out = h0.copy(), []
    for _ in range(steps):
        h = W @ h
        out.append(np.linalg.norm(h))
    return out

print("\n只让记忆自己往下传(不加新输入),看它还剩多少:")
print("   传了几步    谱半径 0.9     谱半径 1.05")
a, c = trace(0.9), trace(1.05)
for t in (1, 2, 3, 5, 8, 12, 16, 20):
    print(f"   {t:>6}      {a[t-1]*100:>9.4f}%    {c[t-1]*100:>11.2f}%")

print(f"\n谱半径 0.9:  传 20 步后只剩 {a[19]*100:.4f}% —— 记忆在衰减,开头的信息传不到结尾。")
print(f"谱半径 1.05: 传 20 步后变成 {c[19]*100:.1f}% —— 记忆在放大,几十步后数值就溢出了。")
print("\n这就是 D09 说的第一堵墙,而且它比「记不住」更麻烦:")
print("循环权重必须被拿捏在 1 附近——小一点,开头的信息传到句尾就淡没了(梯度消失);")
print("大一点,上百步之后数值直接溢出(梯度爆炸)。真实句子就是上百步,这个平衡很难维持。")
print("LSTM/GRU 用一个「门」动态控制每步忘多少、记多少,就是为了缓解这件事。")
print("注意力换了思路:任意两个位置一步直连,压根不需要传——这是它取代 RNN 的根本原因。")

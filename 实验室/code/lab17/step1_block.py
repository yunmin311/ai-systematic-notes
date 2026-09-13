import numpy as np
np.random.seed(0)

T, D, H = 6, 16, 4        # 6 个词,每个 16 维,注意力分 4 个头

def layernorm(x, eps=1e-5):
    mu = x.mean(axis=-1, keepdims=True)
    sd = x.std(axis=-1, keepdims=True)
    return (x - mu) / (sd + eps)

def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

dh = D // H
Wq = np.random.randn(D, D) / np.sqrt(D)
Wk = np.random.randn(D, D) / np.sqrt(D)
Wv = np.random.randn(D, D) / np.sqrt(D)
Wo = np.random.randn(D, D) / np.sqrt(D)
W1 = np.random.randn(D, 4 * D) / np.sqrt(D)   # 前馈层:先放大 4 倍
W2 = np.random.randn(4 * D, D) / np.sqrt(4 * D)  # 再压回来

def attention(x):
    """多头注意力:把 D 维切成 H 份,每份各自算一遍,最后拼回来"""
    Q, K, V = x @ Wq, x @ Wk, x @ Wv
    # 切成 H 个头: (T, D) -> (H, T, dh)
    split = lambda m: m.reshape(T, H, dh).transpose(1, 0, 2)
    q, k, v = split(Q), split(K), split(V)
    score = q @ k.transpose(0, 2, 1) / np.sqrt(dh)          # 每个头各算一份分数
    out = softmax(score) @ v
    return out.transpose(1, 0, 2).reshape(T, D) @ Wo        # 拼回 (T, D)

def ffn(x):
    """前馈层:每个位置各自独立地过一遍两层小网络,不看别人"""
    return np.maximum(0, x @ W1) @ W2

x = np.random.randn(T, D)
print("一个 Transformer 块的四件套:\n")
print(f"   输入                 {x.shape}")

a = attention(x)
print(f"   ① 多头注意力          {a.shape}   ← 横向交流:每个词看全句")
x = layernorm(x + a)
print(f"   ② 残差 + 层归一化      {x.shape}   ← 把输入原样加回来,再拉回规整分布")

f = ffn(x)
print(f"   ③ 前馈层              {f.shape}   ← 纵向加工:每个词自己消化(先放大 4 倍再压回)")
x = layernorm(x + f)
print(f"   ④ 残差 + 层归一化      {x.shape}")

print(f"\n进出的形状完全一样:{x.shape} —— 这就是能一层层往上堆的全部原因。")
print("\n两个子层分工很清楚:")
print("   注意力 = 横向的(词与词之间交流),前馈 = 纵向的(每个词自己加工)。")
print("   注意力里那句 reshape/transpose 就是「多头」:把 16 维切成 4 份各 4 维,")
print("   每份独立算一遍注意力,最后拼回来 —— 相当于让模型从 4 个角度同时看这句话。")

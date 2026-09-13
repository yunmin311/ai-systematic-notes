import numpy as np
from collections import Counter
np.random.seed(0)

corpus = [
    "猫 喜欢 吃 鱼",     "猫 喜欢 睡 觉",     "猫 喜欢 晒太阳",
    "猫 抓 老鼠",        "猫 在 沙发 上 睡",
    "狗 喜欢 吃 骨头",   "狗 喜欢 跑 步",     "狗 喜欢 摇 尾巴",
    "狗 看 家",          "狗 在 院子 里 跑",
]
nxt = {}
for line in corpus:
    ws = line.split()
    for i in range(len(ws) - 1):
        nxt.setdefault(ws[i], Counter())[ws[i + 1]] += 1

# 看「猫」后面那个词的分布——这是模型给出的原始概率
keys = list(nxt["猫"].keys())
p0 = np.array([nxt["猫"][k] for k in keys], dtype=float)
p0 /= p0.sum()
print("模型认为「猫」后面最可能跟的词:")
for k, v in zip(keys, p0):
    bar = "█" * int(v * 40)
    print(f"   {k:<5} {v:6.1%}  {bar}")

def with_temp(p, T):
    """温度只作用在「怎么采」这一步:把对数概率除以 T 再重新归一化"""
    logits = np.log(p + 1e-12) / T
    e = np.exp(logits - logits.max())
    return e / e.sum()

print("\n同一个分布,加上不同温度之后(模型本身一点没变):")
print("   温度       喜欢      抓       在      熵(越高越随机)")
for T in [0.2, 0.5, 1.0, 2.0, 5.0]:
    q = with_temp(p0, T)
    H = -(q * np.log(q + 1e-12)).sum()
    print(f"   {T:<6} {q[0]:>8.1%} {q[1]:>8.1%} {q[2]:>8.1%}   {H:>8.3f}")

print("\n温度不改变模型学到了什么,只改变「从分布里怎么抽」。")
print("   T < 1  分布变尖 —— 高概率的词更容易被抽中,输出更确定、更保守")
print("   T = 1  原样采样")
print("   T > 1  分布被抹平 —— 低概率的词也有机会,输出更发散、更容易跑偏")
print("   T → 0  退化成「永远选概率最大的那个」,同一个问题每次答案都一样")

# ---- 用采样次数把上面的话变成能数的东西 ----
print("\n每种温度下真抽 200 次,看首选词占了多大比例:")
print("(候选只有 3 个,所以别数「出现几种」——那个数最多到 3,看不出差别;要看占比)")
for T in [0.1, 0.5, 1.0, 2.0, 5.0]:
    q = with_temp(p0, T)
    picks = [keys[i] for i in np.random.choice(len(keys), size=200, p=q)]
    c = Counter(picks)
    top_k, top_v = c.most_common(1)[0]
    detail = "、".join(f"{k}×{v}" for k, v in c.most_common())
    print(f"   T={T:<4} 首选「{top_k}」占 {top_v/200:5.1%}   ({detail})")

print("\n这就是 API 里那个 temperature 参数的全部含义:")
print("   调低 → 稳定、可复现,适合抽取信息、写代码、做分类;")
print("   调高 → 多样、有惊喜,适合头脑风暴、写文案;")
print("   同一个问题答案飘忽不定,多半是温度开高了 —— 它是采样,本来就不保证一样。")

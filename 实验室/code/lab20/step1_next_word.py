import numpy as np
from collections import defaultdict, Counter
np.random.seed(0)

# 一个极小的语料。真实模型见的是几万亿字,这里只有 10 句——
# 但要看的机制完全一样:统计「谁跟在谁后面」,然后照着概率往下接。
corpus = [
    "猫 喜欢 吃 鱼",     "猫 喜欢 睡 觉",     "猫 喜欢 晒太阳",
    "猫 抓 老鼠",        "猫 在 沙发 上 睡",
    "狗 喜欢 吃 骨头",   "狗 喜欢 跑 步",     "狗 喜欢 摇 尾巴",
    "狗 看 家",          "狗 在 院子 里 跑",
]

nxt = defaultdict(Counter)
for line in corpus:
    ws = line.split()
    for i in range(len(ws) - 1):
        nxt[ws[i]][ws[i + 1]] += 1

print("模型学到的是这样一张表(每个词后面可能跟什么):")
for w in ["猫", "喜欢", "吃", "狗"]:
    total = sum(nxt[w].values())
    items = "、".join(f"{k}({v}/{total})" for k, v in nxt[w].most_common())
    print(f"   {w:<4} → {items}")

def probs(word):
    """把计数变成概率分布——这就是语言模型每一步的输出"""
    c = nxt[word]
    total = sum(c.values())
    if total == 0:
        return [], np.array([])
    return list(c.keys()), np.array([v / total for v in c.values()])

def generate(start="猫", steps=6, temperature=1.0):
    """接龙:预测下一个词 → 采样一个 → 接到末尾 → 再预测"""
    out = [start]
    for _ in range(steps):
        keys, p = probs(out[-1])
        if len(keys) == 0:
            out.append("[句尾]")          # 没有后继 = 这句话说完了
            break
        if temperature != 1.0:            # 温度只改「怎么采」,不改模型学到的这张表
            logits = np.log(p + 1e-12) / temperature
            p = np.exp(logits - logits.max())
            p = p / p.sum()
        out.append(keys[np.random.choice(len(keys), p=p)])
    return " ".join(out)

print("\n让它接龙三次(起点都是「猫」):")
for i in range(3):
    print(f"   {i+1}. {generate()}")

print("\n三次结果不一样,但每次都通顺——因为模型输出的是概率分布,")
print("每一步都是从分布里抽一个,抽到什么有随机性。")
print("这就是同一个问题每次答案会变的原因:不是它「改主意」了,是采样在起作用。")

print("\n那句 [句尾] 也值得注意:词表里没有词的后面什么也不跟,模型就停在那里。")
print("真实模型专门有一个「结束」符号来表示该收尾了——")
print("否则它会一直往下编,永远停不下来。")

print("\n真实的大语言模型做的还是同一件事,只是三样东西被放大了:")
print("   · 表从「上一个词 → 下一个词」升级成「前面所有词 → 下一个词」")
print("   · 词表从 12 个词变成几万到十几万个 token")
print("   · 参数从这张几百个数的表变成几千亿个权重")
print("机制没变:给定前面的文字,算下一个词的概率,采样,接到末尾,重复。")

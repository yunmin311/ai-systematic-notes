import numpy as np

# 造一个「有规律」的小语料。规律不是写在注释里,而是靠重复的句式让统计能抓到:
#   三种动物 × 三种食物,都用同一个句式 -> 动物出现在相似的位置,食物也出现在相似的位置。
pets  = ["猫", "狗", "兔子"]
foods = ["鱼", "骨头", "胡萝卜"]

corpus = [f"{p} 吃 {f}" for p in pets for f in foods]      # 9 句
corpus += [f"{p} 是 宠物" for p in pets]                    # 3 句
print(f"语料 {len(corpus)} 句,词表 {len(set(w for s in corpus for w in s.split()))} 个词")
print("前 4 句:", " / ".join(corpus[:4]), "\n")

words = sorted({w for line in corpus for w in line.split()})
idx = {w: i for i, w in enumerate(words)}
V = len(words)

# ---- ① 统计共现:窗口内一起出现就算一次 ----
WIN = 2
C = np.zeros((V, V))
for line in corpus:
    ws = line.split()
    for i, w in enumerate(ws):
        for j in range(max(0, i - WIN), min(len(ws), i + WIN + 1)):
            if i != j:
                C[idx[w], idx[ws[j]]] += 1

show = ["猫", "狗", "兔子", "鱼", "骨头", "胡萝卜"]
print("共现矩阵(行 = 当前词,列 = 它的邻居):")
print("          " + "".join(f"{w:>6}" for w in show))
for w in show:
    print(f"   {w:<5} " + "".join(f"{int(C[idx[w], idx[x]]):>6}" for x in show))
print("\n注意 猫、狗、兔子 三行的数字完全一样 —— 它们在语料里的位置是等价的。")

# ---- ② SVD 把共现矩阵压成 2 维词向量 ----
U, S, _ = np.linalg.svd(C, full_matrices=False)
emb = U[:, :2] * S[:2]
print(f"\n前两个奇异值 {S[0]:.2f} / {S[1]:.2f} 承载了矩阵的主要结构。")

# ---- ③ 看谁和谁近 ----
def nearest(word, k=3):
    v = emb[idx[word]]
    sims = [(w, float(v @ emb[idx[w]] / (np.linalg.norm(v) * np.linalg.norm(emb[idx[w]]))))
            for w in words if w != word]
    return sorted(sims, key=lambda t: -t[1])[:k]

print("\n每个词的最近邻居(余弦相似度):")
for w in ["猫", "狗", "兔子", "鱼", "骨头", "胡萝卜", "吃"]:
    ns = "、".join(f"{n} {s:.3f}" for n, s in nearest(w))
    print(f"   {w:<5} → {ns}")

print("\n值得盯的几行:")
print("   · 猫、狗、兔子互为最近邻 —— 没人告诉模型它们都是动物,")
print("     只因为它们出现在同样的句式位置,坐标就长到了一起。")
print("   · 鱼、骨头、胡萝卜 也聚在一起 —— 它们是「被吃的那个」。")
print("   · 但「吃」的最近邻是 宠物 和 是(0.953),不是任何一类食物。")
print("     它和每个动物、每种食物都连过一次,连得太均匀,反而谁也不偏向——")
print("     这也说明:一个词连接范围太广时,它的坐标会变得「中庸」,判别力反而弱。")
print("\n这就是 Embedding 的原理:统计谁和谁一起出现,相似的上下文长出相似的坐标。")
print("真实词向量只是把语料从 12 句换成几万亿句,把维度从 2 换成几百上千。")

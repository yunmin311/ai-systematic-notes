import numpy as np

docs = {
  "说明书": "睡眠灯 A1 支持三档亮度。轻触顶部圆环可以在低亮、中亮、高亮之间循环切换。"
            "长按圆环两秒进入夜灯模式,亮度自动降到最低。"
            "灯体侧面有一个色温滑条,可以从暖黄调到冷白。",
  "售后政策": "睡眠灯 A1 整机保修两年,灯珠保修三年,均从签收之日起算。"
              "人为损坏、进水、私自拆机不在保修范围内。"
              "保修期内寄修运费由我们承担,寄回请保留快递单号。",
  "常见问题": "有用户反馈灯体偶尔自动熄灭。这通常是开启了「人来灯亮」感应模式,"
              "十五分钟无人移动会自动关闭。长按色温滑条底端三秒可以关闭这个功能。",
}
print(f"原始资料 {len(docs)} 篇,共 {sum(len(v) for v in docs.values())} 字\n")

# ---- ① 切块:每块 40 字,相邻块重叠 10 字 ----
def chunk(text, size=40, overlap=10):
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i+size])
        i += size - overlap
    return out

chunks = [{"src": n, "idx": k, "text": c}
          for n, t in docs.items() for k, c in enumerate(chunk(t))]
print(f"切块:每块 40 字、重叠 10 字  →  {len(chunks)} 块")

# ---- ② 切词:用一份领域词表做「最长匹配」 ----
# 中文没有空格,不能直接按空格切。这里用一份词表,从左往右尽量匹配最长的词,
# 匹配不到就退回单字。真实系统用 jieba 之类的分词器,思路一样。
TERMS = sorted([
    "睡眠灯", "色温滑条", "人来灯亮", "感应模式", "快递单号", "人为损坏",
    "自动关闭", "自动熄灭", "循环切换", "夜灯模式", "保修范围", "保修期",
    "亮度", "低亮", "中亮", "高亮", "圆环", "轻触", "长按", "两秒", "灯体",
    "侧面", "滑条", "暖黄", "冷白", "整机", "保修", "灯珠", "签收", "进水",
    "拆机", "寄修", "运费", "承担", "保留", "用户", "反馈", "偶尔", "开启",
    "分钟", "无人", "移动", "底端", "三秒", "功能", "支持", "三档", "之间",
    "调到", "进入", "降到", "可以", "通常", "关闭", "怎么", "多久", "几年",
], key=len, reverse=True)

def tokenize(s):
    out, i = [], 0
    while i < len(s):
        for t in TERMS:
            if s.startswith(t, i):
                out.append(t); i += len(t); break
        else:
            out.append(s[i]); i += 1
    return out

print("\n切词示例(这就是中文检索和英文最大的不同):")
print("   长按色温滑条底端三秒 →", " / ".join(tokenize("长按色温滑条底端三秒")))

# ---- ③ 向量化:TF-IDF ----
vocab = sorted({w for c in chunks for w in tokenize(c["text"])})
vindex = {w: i for i, w in enumerate(vocab)}
df = {}
for c in chunks:
    for w in set(tokenize(c["text"])):
        df[w] = df.get(w, 0) + 1

def vec(text):
    v = np.zeros(len(vocab))
    for w in tokenize(text):
        if w in vindex:
            v[vindex[w]] += 1
    v /= (v.sum() + 1e-9)
    idf = np.array([np.log((1 + len(chunks)) / (1 + df.get(w, 0))) + 1 for w in vocab])
    v = v * idf
    return v / (np.linalg.norm(v) + 1e-9)

M = np.array([vec(c["text"]) for c in chunks])
print(f"\n词表 {len(vocab)} 个词,每块变成一个 {len(vocab)} 维向量。")

def search(q, k=2):
    sims = M @ vec(q)
    return [(chunks[i], sims[i]) for i in np.argsort(-sims)[:k]]

print("=" * 56)
for q in ["怎么调亮度", "保修几年", "灯总是自动关闭"]:
    print(f"\n问:{q}")
    for c, s in search(q):
        mark = "✓" if s > 0.001 else " "
        print(f"   {mark} 相似度 {s:.3f}  [{c['src']}#{c['idx']}] {c['text'][:30]}…")

print("\n" + "=" * 56)
q_bad = "质保期多久"
print(f"\n问:{q_bad}(故意换一个说法)")
for c, s in search(q_bad):
    print(f"     相似度 {s:.3f}  [{c['src']}#{c['idx']}] {c['text'][:30]}…")
print(f"   切词结果:{' / '.join(tokenize(q_bad))}")
print("   → 全是 0。因为「质保」不在词表里,和资料里的「保修」一个字都不重合。")
print("\n这正是 RAG 必须有 Embedding 模型的原因:")
print("   这种检索靠「字面重合」,换个同义词就彻底失效。")
print("   而 Embedding 把「保修」和「质保」映射到相邻位置,靠意思而不是靠字。")
print("   所以真实 RAG 是「向量检索为主 + 关键词检索兜底」的混合方案,各补各的短板。")

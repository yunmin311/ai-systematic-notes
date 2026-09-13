import numpy as np

# ---- 复用第 1 步的检索部分(完整版见 step1_retrieve.py)----
docs = {
  "说明书": "睡眠灯 A1 支持三档亮度。轻触顶部圆环可以在低亮、中亮、高亮之间循环切换。"
            "长按圆环两秒进入夜灯模式,亮度自动降到最低。",
  "售后政策": "睡眠灯 A1 整机保修两年,灯珠保修三年,均从签收之日起算。"
              "人为损坏、进水、私自拆机不在保修范围内。",
  "常见问题": "有用户反馈灯体偶尔自动熄灭。这通常是开启了「人来灯亮」感应模式,"
              "十五分钟无人移动会自动关闭。",
}
TERMS = sorted(["睡眠灯","感应模式","自动关闭","夜灯模式","保修范围","保修期","人为损坏",
    "亮度","低亮","中亮","高亮","圆环","轻触","长按","两秒","灯体","整机","保修","灯珠",
    "签收","进水","拆机","用户","反馈","偶尔","开启","分钟","无人","移动","功能","支持",
    "三档","之间","降到","进入","可以","通常","关闭","怎么","多久","几年","怎么调"],
    key=len, reverse=True)

def tokenize(s):
    out, i = [], 0
    while i < len(s):
        for t in TERMS:
            if s.startswith(t, i):
                out.append(t); i += len(t); break
        else:
            out.append(s[i]); i += 1
    return out

def chunk(t, size=40, overlap=10):
    return [t[i:i+size] for i in range(0, len(t), size - overlap)]

chunks = [{"src": n, "text": c} for n, t in docs.items() for c in chunk(t)]
vocab = sorted({w for c in chunks for w in tokenize(c["text"])})
vi = {w: i for i, w in enumerate(vocab)}
df = {}
for c in chunks:
    for w in set(tokenize(c["text"])):
        df[w] = df.get(w, 0) + 1

def vec(t):
    v = np.zeros(len(vocab))
    for w in tokenize(t):
        if w in vi: v[vi[w]] += 1
    v /= (v.sum() + 1e-9)
    v *= np.array([np.log((1+len(chunks))/(1+df.get(w,0)))+1 for w in vocab])
    return v / (np.linalg.norm(v) + 1e-9)

M = np.array([vec(c["text"]) for c in chunks])

def retrieve(q, k=2, thresh=0.05):
    """比第 1 步多一个门槛:相似度太低就不要,宁可没有上下文"""
    sims = M @ vec(q)
    top = np.argsort(-sims)[:k]
    return [chunks[i] for i in top if sims[i] >= thresh]

# ---- 组装提示词 ----
def build_prompt(q, ctx):
    if not ctx:
        return f"资料:\n(没有找到相关资料)\n\n问题:{q}"
    body = "\n".join(f"[{c['src']}] {c['text']}" for c in ctx)
    return (f"严格依据下面的资料回答问题。资料里没有的内容,直接回答「资料中没有提到」,"
            f"不要编。回答末尾标出用到的出处。\n\n资料:\n{body}\n\n问题:{q}")

# ---- 桩模型:真实场景这里是 API 调用 ----
# 它模拟一个「守规矩」的模型:只从资料里找答案,找不到就说不知道。
def stub_model(prompt, q):
    if "(没有找到相关资料)" in prompt:
        return "资料中没有提到。"
    body = prompt.split("资料:\n")[1].split("\n\n问题:")[0]
    qs = set(tokenize(q)) - {"怎么", "多久", "几年", "可以"}
    best, best_hit = None, 0
    for line in body.split("\n"):
        hit = len(qs & set(tokenize(line)))
        if hit > best_hit:
            best, best_hit = line, hit
    if best is None:
        return "资料中没有提到。"
    src = best.split("]")[0] + "]"
    return f"{best.split('] ', 1)[1]}\n(出处:{src})"

print("=" * 58)
for q in ["怎么调亮度", "保修几年", "质保期多久"]:
    ctx = retrieve(q)
    prompt = build_prompt(q, ctx)
    print(f"\n问:{q}")
    print(f"   检索到 {len(ctx)} 块")
    print(f"   提示词长度 {len(prompt)} 字")
    ans = stub_model(prompt, q).split("\n")
    for line in ans:
        print(f"   答:{line}")

print("\n" + "=" * 58)
print("\n三问的对比就是 RAG 的完整链路:")
print("   检索 → 拼提示词 → 生成。三步里任何一步出错,答案都会错。")
print("\n最后一问值得单独看:检索一个字都没命中,于是上下文是空的,")
print("模型照约定回答了「资料中没有提到」。")
print("这就是 RAG 治幻觉的机制 —— 不是让模型更聪明,是「给它材料、并允许它说不知道」。")
print("\n另外注意前两问的答案结尾都是断的(「…私自拆机」「…均从签收之日起算。人为损坏…」)。")
print("不是桩模型的问题 —— 块就是 40 字,答案自然也被截在 40 字。")
print("这就是切块大小真正的取舍:块小,检索准但答案可能残缺;")
print("块大,答得整但容易掺进不相干的内容。RAG 调参最花时间的地方就在这里。")
print("\n工程上最该盯的一环是「相似度门槛」(代码里的 thresh):")
print("   门槛太低,不相干的块也会被塞进提示词,模型就会顺着它编;")
print("   门槛太高,该答的也答不出来。这个数只能靠自己的数据一条条试出来。")

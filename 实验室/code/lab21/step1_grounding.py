import re

# 检索到的资料(真实系统里来自 RAG)
context = (
    "睡眠灯 A1 整机保修两年,灯珠保修三年,均从签收之日起算。"
    "人为损坏、进水、私自拆机不在保修范围内。"
    "保修期内寄修运费由我们承担。"
)

# 三版「模型回答」。前两版老实,第三版编了资料里没有的东西。
answers = {
    "A 有依据": "整机保修两年。人为损坏不在保修范围内。",
    "B 有依据(带改写)": "睡眠灯 A1 的灯珠保修期是三年,从签收那天开始算。",
    "C 编的":   "整机保修两年。另外我们还提供三年免费上门维修服务。",
}

def sentences(text):
    return [s for s in re.split(r"[。;!?]", text) if s.strip()]

def key_terms(s):
    """粗粒度取词:2 字以上的连续汉字片段,再切成二字组合当关键词"""
    raw = re.findall(r"[\u4e00-\u9fa5]{2,}", s)
    out = set()
    for seg in raw:
        if len(seg) == 2: out.add(seg)
        for i in range(len(seg) - 1): out.add(seg[i:i+2])
    return out

print("资料:")
print("   " + context, "\n")
print("把每版回答拆成句子,逐句看它的关键词能不能在资料里找到:\n")

for name, ans in answers.items():
    ss = sentences(ans)
    hits = 0
    detail = []
    for s in ss:
        terms = key_terms(s)
        found = {t for t in terms if t in context}
        ok = len(found) / max(len(terms), 1)
        hits += ok >= 0.5                        # 一半以上的词能在资料里找到,就算这句有依据
        detail.append(f"{'✓' if ok >= 0.5 else '✗'} {s}(命中 {ok:.0%})")
    print(f"   {name}:  有依据 {hits}/{len(ss)} 句")
    for d in detail:
        print("        " + d)
    print()

print("三版对照看出两件事:")
print("   ① B 版把「保修三年」改写成「保修期是三年,从签收那天开始算」——")
print("      字面完全不同,但关键词都落在资料里,照样判为有依据。这说明这套检测")
print("      算的是「有没有出处」,不是「是不是照抄」。")
print("   ② C 版的第二句整句判 ✗:「免费上门维修」在资料里一个字都找不到。")
print("      这就是幻觉的可检测形态 —— 不是它说得像不像,是它在资料里没有落脚点。")
print("   注意 B 版只有 53%,离 50% 这条线很近 —— 阈值稍微调一下结论就翻。")
print("   所以这套检测不能当唯一依据,它是个「报警器」,报出来的要人工看。")
print()
print("这就是 A06 说的「评估」能自动化的那一半:")
print("   有依据 / 没依据,可以机械判定;")
print("   但「答得好不好、有没有用」判不了,那部分只能人工抽样。")

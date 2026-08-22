def estimate_tokens(text):
    """粗估:中日韩字符按 1.5 个 Token 算,其余按每 4 个字符 1 个 Token 算。"""
    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other = len(text) - cjk
    return round(cjk * 1.5 + other / 4)

zh = "注意力机制的核心是:处理某个词时,按相关度给全句每个词加权,再把它们的信息汇总进来。"
en = ("The core of attention is: when processing a word, weight every word in the "
      "sentence by relevance, then aggregate their information.")

for name, t in [("中文", zh), ("英文", en)]:
    print(f"{name}: {len(t):3d} 字符  →  约 {estimate_tokens(t):3d} Token")

print()
print("中/英 Token 数之比:", round(estimate_tokens(zh) / estimate_tokens(en), 2))
print("(同一个意思,中文通常更费 Token——D12 第 10 节讲了原因)")

# 全参微调 vs LoRA,到底差多少参数。算的是一道纯算术题。

def full_params(layers, d, vocab=150000):
    """一个 Transformer 的可训练参数(不含词表):
       每层 = 注意力 4d² + 前馈 8d²(放大 4 倍再压回,两次都是 d×4d)"""
    per_layer = 4 * d * d + 8 * d * d
    return layers * per_layer, vocab * d      # 第二个数是词表(嵌入层)

def lora_params(layers, d, rank, targets_per_layer=4):
    """LoRA:不改原矩阵,只在旁边挂两个小矩阵 A(d×r) 和 B(r×d)。
       每挂一处新增 r*d + d*r = 2rd 个参数。"""
    return layers * targets_per_layer * 2 * rank * d

CONFIGS = [
    ("小模型 6 层 d=512",  6, 512),
    ("中模型 24 层 d=1024", 24, 1024),
    ("7B 级 32 层 d=4096", 32, 4096),
]

print(f"{'配置':<22}{'全参(主体)':>14}{'LoRA(r=8)':>12}{'占比':>9}")
rows = []
for name, L, d in CONFIGS:
    body, emb = full_params(L, d)
    lora = lora_params(L, d, rank=8)
    pct = lora / body
    rows.append((name, body, emb, lora, pct))
    print(f"{name:<22}{body:>14,}{lora:>12,}{pct:>8.3%}")

print("\n换几个 rank 和目标层数看看(以 7B 级那行的配置 L=32、d=4096 为例):")
BIG_L, BIG_D = 32, 4096
body, emb = full_params(BIG_L, BIG_D)
print(f"   目标层数     rank       LoRA 参数        占主体的比例")
for targets in [4, 8, 16, 32]:
    for r in [8, 32]:
        lp = lora_params(BIG_L, BIG_D, r, targets)
        print(f"   {targets:>8}     {r:>4}   {lp:>13,}   {lp/body:>12.3%}")

print("\n三个关键数字:")
body, emb, lora, pct = rows[-1][1], rows[-1][2], rows[-1][3], rows[-1][4]
print(f"   ① 全参要动 {body:,} 个参数(还不算词表 {emb:,});LoRA 只动 {lora:,} 个。")
print(f"      占比 {pct:.3%} —— 千分之一多一点。")
print(f"   ② 但训练时还要存梯度、优化器状态,全参微调的显存大约是参数的 3~4 倍。")
print(f"      LoRA 这些全都不需要,所以显存降得比参数比例还多。")
print(f"   ③ 推理时可以把 LoRA 权重直接加回原矩阵(B@A 加进 W),")
print(f"      所以部署时不增加任何延迟 —— 这一点常常被忽略。")

print("\n这就是「微调」在工程上真正便宜的地方:")
print("   它不是把整个模型重训一遍,而是在每个权重矩阵旁边挂一块小补丁。")
print("   原权重冻住不动,只学那块补丁 —— 这也解释了为什么便宜的同时")
print("   它的能力上限不如全参微调:补丁能改的东西,本来就有限。")

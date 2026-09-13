# 对齐阶段的起点不是「打分」,而是「两个回答里哪个更好」。
# 这一节把一批成对比较转成排名 —— 这就是 RLHF 里奖励模型吃的那份数据。

MODELS = ["回答 A", "回答 B", "回答 C", "回答 D"]

# 人工标注的成对偏好:(赢的, 输的)。注意标注员从没给过任何绝对分数。
MATCHES = [
    ("回答 A", "回答 B"), ("回答 A", "回答 B"), ("回答 A", "回答 C"),
    ("回答 B", "回答 C"), ("回答 B", "回答 D"),
    ("回答 C", "回答 D"), ("回答 C", "回答 D"), ("回答 C", "回答 D"),
    ("回答 A", "回答 D"),
]
WIN_LOSS = {m: [0, 0] for m in MODELS}      # 顺手统计每个回答的胜负场次
for w, l in MATCHES:
    WIN_LOSS[w][0] += 1
    WIN_LOSS[l][1] += 1

def elo(matches, K=32, rounds=60, base=1000.0):
    """Elo。每一轮结束后把分数整体平移回均值 1000——
       否则相同数据反复跑会一路发散(分数没有绝对零点,只有相对差距有意义)。"""
    score = {m: base for m in MODELS}
    for _ in range(rounds):
        for win, lose in matches:
            exp = 1 / (1 + 10 ** ((score[lose] - score[win]) / 400))   # 预期胜率
            delta = K * (1 - exp)                                     # 实际赢了(1),超出预期多少
            score[win] += delta
            score[lose] -= delta
        mean = sum(score.values()) / len(score)
        for m in score:
            score[m] += base - mean                                   # 整轮平移,保持居中
    return score

final = elo(MATCHES)
ranked = sorted(final.items(), key=lambda kv: -kv[1])

print("人工只标了「谁赢」,从没给过分数。这是 9 场比较:")
for w, l in MATCHES:
    print(f"   {w}  >  {l}")
print("\n每个回答的战绩:")
for m in MODELS:
    w, l = WIN_LOSS[m]
    print(f"   {m}   {w} 胜 {l} 负")

print("\n跑完 Elo,得到可以排序的分数(四者均值固定为 1000):")
print("   名次   模型        分数       跟第一名差")
top, bottom = ranked[0][1], ranked[-1][1]
for i, (m, s) in enumerate(ranked, 1):
    bar = "█" * min(44, max(1, int((s - bottom) / (top - bottom + 1e-9) * 44)))
    print(f"   {i:>2}    {m:<8}{s:>9.1f}     {s-top:>9.1f}  {bar}")

print(f"\n排名:{' > '.join(m for m, _ in ranked)}")

print("\n排名和战绩对不上,这一点最值得停一下看:")
print("   C 是 3 胜 2 负,B 是 2 胜 2 负 —— 胜场更多的 C 却排在 B 后面。")
print("   原因不复杂:B 和 C 交过手,B 赢了;而 C 那三场胜仗全是赢 D")
print("   (唯一 0 胜 5 负的那个),含金量低。")
print("   Elo 记的不是「赢了几场」,是「赢了谁」—— 这正是它比单纯数胜场")
print("   更适合处理偏好的地方:光看胜率会把「专挑软柿子」当成强。")

print("\n三件事要看清:")
print("   ① 输入只有「谁赢」这种相对判断,输出却是可以排序的分数。")
print("      这就是把「偏好」变成「目标函数」的那一步 —— 没有它,没法训练。")
print("   ② 分数的绝对大小没有意义,只有相对差距有意义。")
print("      代码里每轮把均值拉回 1000,就是因为这套分数没有绝对零点;")
print("      换成 500 或 2000 当中心,排名一模一样。")
print(f"   ③ A 拿到 {final['回答 A']:.0f} 分,比 D 高出 {final['回答 A']-final['回答 D']:.0f} 分。")
print("      差距这么大,是因为这批数据里 A 一场没输过。")
print("      少量比较就能拉开巨大差距,说明这种数据的信息量是有限的:")
print("      它够排出顺序,不够说清「好多少」。")
print()
print("对应到 D16 的第三阶段:")
print("   这批「谁赢」的数据 → 训练一个奖励模型 → 用奖励模型给模型的输出打分")
print("   → 分数高的被鼓励。整条链路能从相对判断出发,")
print("   靠的就是上面这个把「比较」变成「分数」的动作。")
print()
print("也正因为起点是人的偏好,而不是客观答案:")
print("   它适合解决「哪种答法更好」这类没有标准答案的问题,")
print("   也不可避免地把标注员的偏好一起学了进去。")

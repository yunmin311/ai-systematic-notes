# 一次请求由四部分组成。数字是示例,实际要用真实 tokenizer 数(lab-08 做过)。
parts = {
    "系统提示": 320,
    "检索资料": 1800,
    "历史对话": 2600,
    "用户问题": 40,
}
answer = 400                       # 模型生成的回答
BUDGET = 4000                      # 每次请求的输入预算上限

PRICE_IN = 1.5 / 1_000_000         # 假设:输入每百万 token 1.5 元
PRICE_OUT = 6.0 / 1_000_000        # 假设:输出每百万 token 6 元(输出通常贵好几倍)

total_in = sum(parts.values())

print("一次请求的构成(单位:token):")
for k, v in parts.items():
    bar = "█" * int(v / 50)
    print(f"   {k:<6} {v:>5}  {v/total_in:6.1%}  {bar}")
print(f"   {'合计':<6} {total_in:>5}   ← 预算只有 {BUDGET},已经超了")
print(f"   回答     {answer:>5}   ← 这部分算输出价,单价是输入的 4 倍\n")

def money(inp, out):
    return inp * PRICE_IN + out * PRICE_OUT

c = money(total_in, answer)
print(f"单次成本 = 输入 {total_in}×{PRICE_IN*1e6:.1f}元/M + 输出 {answer}×{PRICE_OUT*1e6:.1f}元/M")
print(f"         = {total_in*PRICE_IN:.6f} + {answer*PRICE_OUT:.6f} = {c:.6f} 元")
print(f"每天 1 万次请求 = {c*10000:.2f} 元 / 天,一个月约 {c*10000*30:.0f} 元\n")

need = total_in - BUDGET
print(f"要把输入从 {total_in} 压到 {BUDGET} 以内,得砍掉 {need} 个 token。三种砍法:")
print("   " + f"{'砍哪部分':<10}{'这部分共':>8}{'能砍掉':>8}{'占自身':>8}{'达标?':>8}   代价")
for name, price in [
    ("历史对话", "多轮上下文断了,来回指代会失效"),
    ("检索资料", "更容易幻觉——这正是 A06 要治的"),
    ("系统提示", "角色和规则丢了,输出风格立刻跑偏"),
]:
    avail = parts[name]
    take = min(avail, need)
    pct = take / avail
    ok = "✓" if take >= need else "✗ 不够"
    print(f"   {name:<10}{avail:>8}{take:>8}{pct:>7.0%}{ok:>8}   {price}")

print()
print("三行对照说明了这次决策的实质:")
print("   · 砍历史对话:砍掉 760,占它自己的 29%,还留着七成。")
print("   · 砍检索资料:同样砍 760,却占它 42% —— 要丢掉四成资料才凑够。")
print("   · 砍系统提示:全砍光(100%)也不够,还得再去别处凑 440。")
print()
print("所以这道题不是「哪个便宜砍哪个」,而是「哪部分的信息最不能丢」:")
print("   资料砍掉小一半,幻觉概率立刻上升;系统提示砍了,角色和规则直接丢。")
print("   砍历史最稳——因为历史可以压缩:保留最近几轮原文,前面用一句摘要代替。")
print()
print("这就是 A06 把成本、幻觉、评估放在同一章讲的原因:它们互相牵制,")
print("每一次省钱的选择,都会在另外两个指标上留下痕迹。")

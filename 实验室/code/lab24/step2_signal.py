# 上下文窗口里的「信噪比」:塞进去的东西越多,真正有用的那条占比越低。
# 这解释了为什么 RAG 不是「把资料全塞进去」,而是「只塞最相关的那几条」。

QUESTION = "睡眠灯保修几年?"

RELEVANT = "睡眠灯 A1 整机保修两年,灯珠保修三年,均从签收之日起算。"   # 真正有用的那条

NOISE = [
    "本店支持七天无理由退换,需保持包装完好。",
    "发货时间为付款后 48 小时内,节假日顺延。",
    "会员每消费一元累计一分,可在积分商城兑换。",
    "目前支持微信、支付宝两种支付方式。",
    "如需开发票,请在订单备注中填写抬头与税号。",
    "我们的客服在线时间为每天 9:00 到 21:00。",
    "部分地区可享受次日达,具体以下单页为准。",
]

TOK_PER_CHAR = 1.5      # 中文大约 1.5 字一个 token(与第 8 章的估算一致)

def report(n_noise):
    ctx = RELEVANT + "".join(NOISE[:n_noise])
    total = int(len(ctx) * TOK_PER_CHAR)
    useful = len(RELEVANT) / len(ctx)
    return n_noise, len(ctx), total, useful

print(f"问题:{QUESTION}\n")
print("往上下文里塞不同数量的无关资料,看有效信息占比怎么变:")
print("   无关条数   资料总字数   约多少 token   有效信息占比")
rows = [report(n) for n in [0, 1, 2, 4, 7]]
for n, chars, toks, useful in rows:
    bar = "█" * int(useful * 40)
    print(f"   {n:>6}   {chars:>9}   {toks:>11}   {useful:>9.1%}  {bar}")

first, last = rows[0], rows[-1]
print(f"\n只放那一条有用的:上下文 {first[1]} 字,有效信息占 {first[3]:.0%}。")
print(f"再塞 7 条无关的:上下文涨到 {last[1]} 字({last[2]} token),占比掉到 {last[3]:.0%}。")
print(f"token 涨了 {last[2]/first[2]:.1f} 倍,而真正有用的那条一点没变长。")

print("\n三点要连着看:")
print("   ① 钱:token 涨了,费用跟着涨,而且这部分是每轮都要重付的固定开销。")
print("   ② 效果:无关内容越多,模型越容易被带偏 —— 它不会「自动忽略」噪声,")
print("      而是把这一整段都当成「当前要说的事」。")
print("   ③ 关键信息的位置:真正有用的那条一旦被埋在中间,更容易被忽略。")
print()
print("所以「塞得越多越好」是错的。正确的做法是先把候选筛一遍,只留最相关的几条:")
print("   这就是 RAG 里「检索」那一步存在的全部理由(见 lab-19)。")
print("   反过来,如果筛不准,宁可少塞 —— 给 1 条对的,好过给 8 条里混 1 条对的。")

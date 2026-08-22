IN_PRICE, OUT_PRICE = 0.3, 1.5      # 每百万 Token 的美元价
in_tok, out_tok, calls = 2000, 300, 1000

in_cost = in_tok * calls / 1e6 * IN_PRICE
out_cost = out_tok * calls / 1e6 * OUT_PRICE

print(f"每天输入 {in_tok*calls/1e6:.1f}M Token  → ${in_cost:.2f}")
print(f"每天输出 {out_tok*calls/1e6:.1f}M Token  → ${out_cost:.2f}")
print(f"每天合计 ${in_cost+out_cost:.2f}   每月约 ${(in_cost+out_cost)*30:.0f}")
print()
print("输出量只有输入的 15%,但花费占比:",
      f"{out_cost/(in_cost+out_cost)*100:.0f}%")
print("原因:输出按 D17 说的逐个生成、无法并行,单价贵 5 倍")
print()
# 加上提示缓存:假设 1500 Token 的系统提示可缓存,缓存价按 1/10 计
cached = 1500
new_in = (in_tok - cached) * calls / 1e6 * IN_PRICE + cached * calls / 1e6 * IN_PRICE * 0.1
print(f"若 {cached} Token 的系统提示走缓存:每天输入 ${new_in:.2f}(原 ${in_cost:.2f})")
print(f"每月省下约 ${(in_cost-new_in)*30:.0f}")

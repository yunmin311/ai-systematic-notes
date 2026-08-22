IN_PRICE = 0.3
per_turn_new = 1000        # 每轮新增(提问 + 回答)
turns = 10

history, total_read, total_new = 0, 0, 0
print("轮次   本轮读入 Token   累计读入")
for t in range(1, turns + 1):
    read = history + per_turn_new
    total_read += read
    total_new += per_turn_new
    history += per_turn_new
    if t in (1, 2, 5, 10):
        print(f"{t:>3}    {read:>10,}    {total_read:>10,}")

print()
print(f"十轮里真正「新写」的内容: {total_new:,} Token")
print(f"十轮里实际被读入的总量:   {total_read:,} Token")
print(f"重读占比: {(1 - total_new/total_read)*100:.0f}%")
print(f"按 ${IN_PRICE}/百万计,这一场对话的输入侧花费 ${total_read/1e6*IN_PRICE:.4f}")

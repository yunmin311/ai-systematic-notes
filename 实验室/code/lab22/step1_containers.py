# 五块地基里的前三块:变量、容器、控制流。
# 任务很小:统计一句话里每个词出现了几次——这三块刚好都用上。

text = "猫 喜欢 吃 鱼 狗 喜欢 吃 骨头 猫 喜欢 睡 觉"
words = text.split()                 # 容器①:列表 —— 一串按顺序排的东西
print("切成词之后:", words)
print(f"一共 {len(words)} 个词\n")

counts = {}                          # 容器②:字典 —— 一个词对应一个次数
for w in words:                      # 控制流①:for —— 把列表里的东西挨个过一遍
    if w in counts:                  # 控制流②:if —— 分情况处理
        counts[w] += 1
    else:
        counts[w] = 1

print("每个词出现了几次:")
for w, n in counts.items():
    print(f"   {w:<4} {n} 次  {'█' * n}")

# 控制流③:while —— 反复做,直到条件不成立(这里手写一遍 max,看清它怎么找最大值)
nums = list(counts.values())
i, target = 0, 0
while i < len(nums):
    if nums[i] > target:
        target = nums[i]
    i += 1
best = []
for w, n in counts.items():
    if n == target:
        best.append(w)

print(f"\n出现最多的是「{'、'.join(best)}」,各 {target} 次。")
print("\n回头对一遍那五块地基:")
print("   变量   text / words / counts / target —— 给数据起名字")
print("   容器   列表(有序、按位置取)和字典(按名字取)—— 装东西的两种盒子")
print("   控制流 for 挨个过、if 分情况、while 反复做 —— 决定代码怎么走")
print("   这三块加起来,已经能写出「统计词频」这种真能干活的程序了。")

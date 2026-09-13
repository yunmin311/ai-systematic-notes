# Agent 和普通问答的差别,全在这一个循环里。
# 这里把「模型」写成一份脚本化的决定表,好把循环本身看清楚;
# 真实场景里每一次「想」都是一次模型调用。

TOOLS = {
    "get_weather":  lambda city: {"北京": 28, "上海": 22, "广州": 31}.get(city),
    "calculator":   lambda expr: eval(expr, {"__builtins__": {}}, {}),
}

# 模型每一步的「想」和「做」——按顺序排好,模拟一个会分步推进的 agent
PLAN = [
    ("要算温差,得先拿到北京的温度", ("get_weather", "北京")),
    ("北京 28 度。还缺上海的温度",   ("get_weather", "上海")),
    ("两个数都有了,做减法",         ("calculator", "28 - 22")),
]

def observe(tool, arg):
    """执行工具并返回「看到」的结果"""
    if tool not in TOOLS:
        return None, f"没有这个工具:{tool}"
    try:
        result = TOOLS[tool](arg)
    except Exception as e:
        return None, f"工具报错:{type(e).__name__}"
    if result is None:
        return None, "工具没找到对应数据"
    return result, None

task = "北京和上海的温差是多少?"
print(f"任务:{task}\n")
print("循环开始 —— 每一轮都是 想 → 做 → 看:\n")

trace = []
MAX_STEPS = 8
for step, (thought, (tool, arg)) in enumerate(PLAN, 1):
    if step > MAX_STEPS:
        print(f"   到达步数上限 {MAX_STEPS},停下")
        break
    print(f"   ── 第 {step} 轮 ──")
    print(f"   想   {thought}")
    print(f"   做   {tool}({arg!r})")
    result, err = observe(tool, arg)
    if err:
        print(f"   看   ✗ {err}")
        break
    print(f"   看   {result}")
    trace.append(result)
    print()

# 循环的出口:模型判断「够了,可以回答」
if len(trace) == 3:
    print("   想   三个数齐了,任务完成 → 输出答案,退出循环")

print("\n循环结束。整个过程回答的是一句话,但走了 3 轮:")
print("   普通问答:一次输入 → 一次输出,错了也就错了。")
print("   agent:  一次输入 → 多轮「想/做/看」,每轮都能根据看到的东西改主意。")
print()
print("差别不在模型多聪明,在外面套没套那个循环 ——")
print("模型还是那个模型,但它的输出现在能改变下一步的输入了。")
print()
print("循环本身只需要三样东西:")
print("   ① 一个能重复的步骤(这里就是 想/做/看)")
print("   ② 一个终止条件(任务完成,或者到了步数上限)")
print("   ③ 一份记忆(把每轮「看到」的记下来,否则下一轮等于失忆)")
print("   第三样最容易被忽略 —— 它其实就是上下文窗口在做的事。")

import json

# 给模型一张「表格模板」:三个字段,各是什么类型
SCHEMA = {"city": str, "temp": int, "condition": str}

# 桩模型第一次的四种输出。真实场景这里是一次 API 调用。
RAW = [
    '{"city": "北京", "temp": 28, "condition": "晴"}',
    '{"city": "上海", "temp": "22", "condition": "多云"}',
    '{"city": "广州", "condition": "小雨"}',
    '好的,北京今天 28 度,晴天。',
]

def check(text):
    """按 schema 校验。返回 (通过?, 问题描述或数据)"""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return False, f"不是合法 JSON({e.msg})"
    if not isinstance(data, dict):
        return False, "顶层不是对象"
    for field, typ in SCHEMA.items():
        if field not in data:
            return False, f"缺字段 {field}"
        # 注意 bool 是 int 的子类,要单独排除,否则 True 会被当成合格的整数
        if typ is int and isinstance(data[field], bool):
            return False, f"{field} 的布尔值不能当整数"
        if not isinstance(data[field], typ):
            return False, f"{field} 类型不对,要 {typ.__name__},给了 {type(data[field]).__name__}"
    return True, data

print("四种模型输出,逐个按 schema 过一遍:\n")
for i, raw in enumerate(RAW, 1):
    ok, info = check(raw)
    mark = "✓ 通过" if ok else "✗ 拦下"
    print(f"   {i}. {mark}   输入:{raw[:38]}")
    if not ok:
        print(f"        原因:{info}")

print("\n这就是结构化输出的全部价值:")
print("   自然语言有无数种写法(第 4 条那种),程序没法可靠地解析;")
print("   而 schema 把「要什么」写在前面,不合格的直接在程序这一侧就被挡住,")
print("   不用等到下游某个地方莫名其妙地崩掉。")

print("\n第 2 条值得单独看:它内容全对,只是 22 被引号包成了字符串。")
print("   人眼看不出问题,但程序拿到 '22' 去做加法会直接报错。")
print("   schema 校验就是把这类「看起来对」的东西提前拦住。")

# ---- 拦截之后怎么办:带着具体原因重试 ----
def fake_model_retry(feedback):
    """桩模型:被告知哪里错了,就改对。真实场景这里是把错误信息拼回提示词再调一次。"""
    if "缺字段 temp" in feedback: return '{"city": "广州", "temp": 26, "condition": "小雨"}'
    if "temp 类型不对" in feedback: return '{"city": "上海", "temp": 22, "condition": "多云"}'
    if "不是合法 JSON" in feedback: return '{"city": "北京", "temp": 28, "condition": "晴"}'
    return "{}"

print("\n重试机制:把「哪里不合格」告诉模型,让它改:")
for i, raw in enumerate(RAW, 1):
    ok, info = check(raw)
    if ok:
        print(f"   {i}. 一次通过")
        continue
    fixed = fake_model_retry(info)
    ok2, info2 = check(fixed)
    print(f"   {i}. 第 1 次被拦({info}) → 重试 → {'通过' if ok2 else '仍不合格:' + str(info2)}")

print("\n注意重试不是「再问一遍」,而是把具体错误回给模型。")
print("   只说「格式不对」它只能猜;说「缺字段 temp」它一次就能改对。")
print("   所以 schema 校验器的价值不只是拦截,还在于它产出的是可用的反馈。")

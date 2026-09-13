import json

# 工具表:每个工具有什么参数、参数是什么类型。这份「表」就是给模型看的 schema。
TOOLS = {
    "get_weather": {"desc": "查某个城市的天气", "params": {"city": str}},
    "send_email":  {"desc": "发一封邮件",       "params": {"to": str, "subject": str, "body": str}},
    "delete_file": {"desc": "删除一个文件",     "params": {"path": str}},
}

# 桩模型给出的三次「决定」——真实场景这里是模型返回的 tool_calls。
CALLS = [
    ('{"tool": "get_weather", "args": {"city": "北京"}}',           "正常一次调用"),
    ('{"tool": "get_weather", "args": {"city_name": "北京"}}',      "参数名写错了"),
    ('{"tool": "delete_file", "args": {"path": "/data/all.db"}}',   "合法但危险"),
]

def validate(call_text):
    """校验模型给的工具调用:工具存在吗?参数名和类型对吗?"""
    try:
        call = json.loads(call_text)
    except json.JSONDecodeError as e:
        return False, f"不是合法 JSON({e.msg})", None
    name = call.get("tool")
    if name not in TOOLS:
        return False, f"没有这个工具:{name}", None
    spec = TOOLS[name]["params"]
    args = call.get("args", {})
    # 先查「多出来的」再查「缺的」:参数名写错时,会同时多一个、缺一个,
    # 报「多了 city_name」比报「缺 city」更接近病因。
    extra = [k for k in args if k not in spec]
    if extra:
        return False, f"多了参数 {extra}(该工具只需要 {list(spec)})", None
    missing = [k for k in spec if k not in args]
    if missing:
        return False, f"缺参数 {missing}(该工具需要 {list(spec)})", None
    bad = [k for k, t in spec.items() if not isinstance(args[k], t)]
    if bad:
        return False, f"参数类型不对:{bad}", None
    return True, "校验通过", (name, args)

# 危险动作要人点头 —— 和治理逻辑放在同一层,不靠提示词求模型别调
DANGEROUS = {"delete_file"}
APPROVED = False

def execute(name, args):
    """桩实现:真实场景这里才是真的发请求 / 改数据。"""
    if name == "get_weather": return f"{args['city']} 今天 28 度,晴"
    if name == "send_email":  return f"已发送给 {args['to']}"
    if name == "delete_file": return f"已删除 {args['path']}"
    return "?"

print("模型给出的三次决定,逐层过一遍:\n")
for call_text, note in CALLS:
    ok, msg, payload = validate(call_text)
    print(f"   {note}")
    print(f"      模型说:{call_text}")
    if not ok:
        print(f"      ✗ 拦下:{msg}")
        print("      → 把这句话原样拼回提示词,让模型重出一次\n")
        continue
    name, args = payload
    if name in DANGEROUS and not APPROVED:
        print(f"      ⚠ 参数没问题,但 {name} 是危险动作 —— 执行前需要人确认")
        print(f"      → 这次不执行,记一条待批记录\n")
        continue
    print(f"      ✓ 执行:{execute(name, args)}\n")

print("三层各挡一类问题,顺序不能换:")
print("   ① 格式层  JSON 不合法 / 工具名不存在 —— 模型「说错了话」")
print("   ② 参数层  缺参数 / 多参数 / 类型不对 —— 模型「话说得不全」")
print("   ③ 权限层  合法但危险的动作 —— 模型「说对了但不该做」")
print()
print("第 3 层最容易被忽略,也最要紧:前两层靠 schema 就能自动挡,")
print("而「这个动作能不能做」是业务判断,只能由人来定、由代码来执行。")
print("把它写进提示词(「请不要删除文件」)是请求,不是约束 —— 模型可能不听。")
print("写成代码里的白名单 + 人确认,它才是真的挡得住。")

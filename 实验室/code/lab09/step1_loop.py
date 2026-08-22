# ---- 工具注册表:agent 只能调这里有的东西 ----
def read_file(name):
    return f"[{name} 的内容:共 3 行]"

def word_count(text):
    return f"{len(text.split())} 个词"

TOOLS = {"read_file": read_file, "word_count": word_count}

# ---- 模型的桩:真实场景里这里是一次 API 调用 ----
SCRIPT = [
    {"tool": "read_file", "args": ["notes.md"]},
    {"tool": "word_count", "args": ["[notes.md 的内容:共 3 行]"]},
    {"final": "notes.md 大约有 4 个词。"},
]
def fake_model(history):
    return SCRIPT[len(history)]      # 按历史长度取下一步

# ---- agent loop:整个「自主」就在这十行里 ----
history = []
for step in range(1, 6):
    action = fake_model(history)
    if "final" in action:
        print(f"[{step}] 完成 → {action['final']}")
        break
    fn = TOOLS.get(action["tool"])
    if fn is None:
        print(f"[{step}] 拒绝:未注册的工具 {action['tool']}")
        break
    result = fn(*action["args"])
    print(f"[{step}] 调用 {action['tool']}{tuple(action['args'])} → {result}")
    history.append(result)

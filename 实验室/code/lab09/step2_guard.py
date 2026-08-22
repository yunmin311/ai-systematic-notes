import datetime

def read_file(name):  return f"[{name} 的内容]"
def delete_file(name): return f"已删除 {name}"      # ← 危险动作
TOOLS = {"read_file": read_file, "delete_file": delete_file}

DANGEROUS = {"delete_file"}          # 需要人点头的动作
MAX_STEPS = 4                        # 步数上限
LOG = []

def log(kind, detail):
    LOG.append((datetime.datetime.now().strftime("%H:%M:%S"), kind, detail))

# 一个坏掉的模型:反复读同一个文件,第 3 步想删东西
def bad_model(history):
    if len(history) == 2:
        return {"tool": "delete_file", "args": ["notes.md"]}
    return {"tool": "read_file", "args": ["notes.md"]}

APPROVE = False                      # 模拟「人没点头」
history = []
for step in range(1, 100):
    if step > MAX_STEPS:
        print(f"[闸 1] 步数到上限 {MAX_STEPS},强制停止")
        log("halt", f"max_steps={MAX_STEPS}")
        break
    action = bad_model(history)
    name = action["tool"]
    if name in DANGEROUS and not APPROVE:
        print(f"[闸 2] 危险动作 {name} 被拦下:执行前需要人确认")
        log("blocked", name)
        history.append("(该动作被拒绝)")
        continue
    result = TOOLS[name](*action["args"])
    log("call", name)
    print(f"[{step}] {name} → {result}")
    history.append(result)

print("\n---- 日志(第五个抓手)----")
for t, k, d in LOG:
    print(f"{t}  {k:<8}{d}")

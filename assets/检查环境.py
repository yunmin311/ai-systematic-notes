"""检查环境.py —— 换电脑后跑一次,核对本课程要用的工具是否齐全。

为什么有这个脚本:课程库是可移植的,会在不同电脑上被打开。与其在首页维护
"某台机器的版本号"(换机就过时),不如在任何机器上跑一次这个脚本,当场看齐不齐。

用法:打开终端(PowerShell / 终端),cd 到本文件所在目录,运行:
      python 检查环境.py
本脚本不依赖任何第三方库,任何装了 Python 的电脑都能直接跑。
"""
import sys
import subprocess


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=15)
        lines = (r.stdout + r.stderr).strip().splitlines()
        return lines[0] if lines else "(无输出)"
    except Exception as e:
        return "未找到 / 出错:" + str(e)


print("=" * 48)
print("  本课程 · 环境自检")
print("=" * 48)
print(f"当前 Python  : {sys.version.split()[0]}   @ {sys.executable}")
print(f"py -3.10     : {run('py -3.10 --version')}    ← 课程统一用它建虚拟环境(最关键)")
print(f"pip(3.10)    : {run('py -3.10 -m pip --version')}")
print(f"node         : {run('node --version')}    ← 只有做前端 / 跑笔记流水线才需要")
print(f"git          : {run('git --version')}")
print("-" * 48)
print("对照:只要上面的 py -3.10 能打印出 3.10.x,就能开始学第 1 章。")
print("缺哪个再装哪个:Python→python.org  Node→nodejs.org  Git→git-scm.com")

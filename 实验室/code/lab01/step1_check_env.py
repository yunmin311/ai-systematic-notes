# step1_check_env.py —— 验证 Python 环境能正常干活
# 运行方法:在激活了 .venv 的终端里执行  python step1_check_env.py

import sys        # sys:和 Python 解释器本身对话的标准库模块
import platform   # platform:查询操作系统信息的标准库模块

print("Python 版本:", sys.version.split()[0])   # sys.version 是一大段文字,取开头的版本号
print("运行平台:", platform.system())            # Windows / Linux / Darwin(macOS)
print("如果能看到上面两行,说明 Python 已经跑起来了")

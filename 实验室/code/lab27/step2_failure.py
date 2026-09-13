# 循环跑起来不难,难的是工具失败的那几步。
# 这一节把三种应对各演示一遍,再说第四种不该做的。

def get_weather(city):
    data = {"北京": 28, "上海": 22}
    if city not in data:
        return None, "未收录该城市"
    return data[city], None

# 搜索知道的城市比天气工具多一些 —— 这正是「换工具」能救回来的前提。
WEB_DB = {"北京": 28, "上海": 22, "广州": 31}

def search_web(query):
    """桩搜索:从问句里认出城市名,并且只认带「气温」的问法。"""
    if "气温" not in query:
        return None, "没有找到相关结果"
    for city, temp in WEB_DB.items():
        if city in query:
            return f"{city}今日气温 {temp} 摄氏度", None
    return None, "没有找到相关结果"

TOOLS = {"get_weather": get_weather, "search_web": search_web}

def run(label, calls, verdict):
    """把一串尝试依次跑下来,一旦成功就停 —— 和真实循环一样。"""
    print(f"   {label}")
    for tool, arg in calls:
        result, err = TOOLS[tool](arg)
        print(f"      做   {tool}({arg!r})")
        if err:
            print(f"      看   ✗ {err}")
            continue
        print(f"      看   ✓ {result}")
        print(f"      → 成功,退出循环")
        break
    print(f"      评价 {verdict}\n")

print("任务:北京今天多少度?\n")
print("三种应对,各跑一遍:\n")

run("① 原样重试:同参数再问一次",
     [("get_weather", "北京市"), ("get_weather", "北京市")],
     "无用。工具是确定性的,同样的输入不会给出不同的结果,白费一轮。")

run("② 换个写法:从失败信息里猜自己哪儿不对",
     [("get_weather", "北京市"), ("get_weather", "北京")],
     "有效,而且最常见。失败信息说「未收录该城市」,提示可能是名称写法问题。")

run("③ 换工具:一个不通就试另一个",
     [("get_weather", "广州"), ("search_web", "广州 气温")],
     "有效。天气工具没有广州,搜索有 —— 这就是「能力有重叠」的价值。")

print("三种应对的区别,在循环里是三种不同的分支:")
print("   ① 原样重试  — 只在「可能是偶发故障」(网络抖动、限流)时才有意义。")
print("   ② 换个写法  — agent 最常用的一招:把失败信息当成线索,改自己的输入。")
print("   ③ 换工具    — 多一条路,成功率高很多;前提是工具能力有重叠。")

print("\n还有第四种,也是最危险的一种:编一个答案。")
print("   循环里如果写「重试 N 次还不行就自己说一个」,那等于把幻觉做成了默认行为。")
print("   正确的兜底只有一句:如实说「我没查到」。")
print()
print("所以判断一个 agent 好不好,不只看它成功时多能干,")
print("更要看它失败时怎么退场 ——")
print("   是老实说没查到,还是编一个听起来合理的数字。")
print("   前者是可用的工具,后者是要出事的工具。")

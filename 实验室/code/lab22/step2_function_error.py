# 后两块地基:函数 和 读报错。
# 函数 = 把一段会重复用的逻辑打包,起个名字,以后一行调用它。

def average(nums):
    """求平均数。传空列表进去会有惊喜。"""
    return sum(nums) / len(nums)

def word_count(text):
    """把第 1 步那段逻辑包成函数:给它一段文字,还回一个词频字典。"""
    counts = {}
    for w in text.split():
        counts[w] = counts.get(w, 0) + 1     # get(键, 默认值):键不在时就当它是 0
    return counts

print("函数用起来就一行:")
print(f"   average([4.2, 7.9, 12.1]) = {average([4.2, 7.9, 12.1]):.4f}")
print(f"   word_count('猫 吃 鱼 猫') = {word_count('猫 吃 鱼 猫')}")
print("   同一段逻辑,换个输入就能重用 —— 这就是函数的全部意义。")

print("\n再看最常见的一类报错:")
try:
    average([])
except ZeroDivisionError as e:
    print(f"   调用 average([]) 报错 →  {type(e).__name__}: {e}")

print("\n报错信息要从下往上看,一共三步:")
print("   ① 最后一行   ZeroDivisionError: division by zero —— 出了什么错")
print("   ② 倒数第二行  File \"...\", line N, in average —— 哪一行代码出的错")
print("   ③ 回到那一行   len(nums) 是 0,除以 0 当然不行")
print("\n读懂这三步,再回去改:要么让函数拦住空列表,要么在调用前先判断。")
print("AI 生成的代码跑不通时,这一套读法就是最快的那条线索。")

def average_safe(nums):
    """加上一道闸:空列表直接返回 None,而不是崩掉。"""
    if not nums:
        return None
    return sum(nums) / len(nums)

print(f"\n改完之后:average_safe([]) = {average_safe([])}(不崩了)")
print(f"          average_safe([1, 2, 3]) = {average_safe([1, 2, 3]):.4f}")

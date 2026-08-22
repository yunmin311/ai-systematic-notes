# step2_rule.py —— 规则法:规律由人来定,写死在代码里
# 运行方法:python step2_rule.py

PRICE_PER_KG = 4              # ← 这就是“规则”:每公斤 4 元。谁定的?人拍脑袋定的。

def price(weight):
    """按写死的规则算运费"""
    return PRICE_PER_KG * weight

print("规则法预测 5kg 运费:", price(5), "元")

# 思考:快递公司悄悄调价了怎么办?
# 答:数据(账单)会变,但这行代码不会自己变——只能人工回来改。
# 这正是下一步“学习法”要解决的问题。

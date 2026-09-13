from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = load_breast_cancer()
Xtr, Xte, ytr, yte = train_test_split(data.data, data.target,
                                      test_size=0.3, random_state=0, stratify=data.target)
print(f"数据: {len(Xtr)} 条训练 / {len(Xte)} 条测试,每个样本有 {data.data.shape[1]} 个特征\n")

print("树深   叶子数    训练准确率   测试准确率   差值")
for d in [1, 2, 3, 4, 5, 6, 8, 10, None]:
    m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xtr, ytr)
    tr, te = m.score(Xtr, ytr), m.score(Xte, yte)
    label = "不限" if d is None else str(d)
    print(f"{label:>4}  {m.get_n_leaves():>7}    {tr:>9.3f}   {te:>9.3f}   {tr - te:>+7.3f}")

print("\n看两列怎么分叉:深度 1 时两边都低,那是欠拟合;测试准确率在深度 5 见顶(0.912);")
print("再往深它不再涨,而训练准确率一路爬到 1.000——后面涨的全是记忆,不是泛化。")
print("最右那个「差值」列才是过拟合的刻度:从 +0.043 一路扩大到 +0.094,翻了一倍多。")

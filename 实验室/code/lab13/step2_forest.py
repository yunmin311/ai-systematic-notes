from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

data = load_breast_cancer()
Xtr, Xte, ytr, yte = train_test_split(data.data, data.target,
                                      test_size=0.3, random_state=0, stratify=data.target)

tree = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
forest = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)
boost = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)

print("模型                     训练准确率   测试准确率   差值")
for name, m in [("单棵树(不限制深度)", tree),
                ("随机森林(100 棵投票)", forest),
                ("梯度提升(100 棵接力纠错)", boost)]:
    tr, te = m.score(Xtr, ytr), m.score(Xte, yte)
    print(f"{name:<22}  {tr:>9.3f}   {te:>9.3f}   {tr - te:>+7.3f}")

print("\n三行对比说明两件事:")
print("① 单棵树训练 1.000 但测试最低——它把训练集背下来了。")
print("② 森林和提升都把「训练与测试的差距」压小了,测试反而更高。")
print("   这就是「组合很多棵」的意义:单棵爱钻牛角尖,平均之后噪声相互抵消。")

print("\n森林还顺手给出了特征重要性,前 5 名:")
imp = sorted(zip(data.feature_names, forest.feature_importances_),
             key=lambda t: -t[1])[:5]
for name, v in imp:
    print(f"   {name:<26} {v:.3f}")

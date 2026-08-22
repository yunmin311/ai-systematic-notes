from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=800, n_features=20, n_informative=5,
                           n_redundant=5, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

configs = [
    ("完全不限制",       dict()),
    ("限制深度=4",       dict(max_depth=4)),
    ("叶子最少 20 个",   dict(min_samples_leaf=20)),
    ("两个一起上",       dict(max_depth=4, min_samples_leaf=20)),
]
print("配置              训练    测试    5 折交叉验证(均值±标准差)")
for name, kw in configs:
    m = DecisionTreeClassifier(random_state=0, **kw)
    cv = cross_val_score(m, Xtr, ytr, cv=5)
    m.fit(Xtr, ytr)
    print(f"{name:<16}{m.score(Xtr,ytr):.3f}   {m.score(Xte,yte):.3f}   {cv.mean():.3f} ± {cv.std():.3f}")

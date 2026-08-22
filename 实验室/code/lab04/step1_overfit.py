from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=800, n_features=20, n_informative=5,
                           n_redundant=5, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

print("深度   训练分数   测试分数   差距")
for d in [1, 2, 3, 5, 8, 12, 20, None]:
    m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xtr, ytr)
    a, b = m.score(Xtr, ytr), m.score(Xte, yte)
    name = "无限" if d is None else str(d)
    print(f"{name:>4}   {a:.3f}      {b:.3f}      {a-b:.3f}")

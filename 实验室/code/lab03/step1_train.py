from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.9, 0.1], random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

model = LogisticRegression(max_iter=1000).fit(Xtr, ytr)

print("训练集样本数:", len(ytr), " 测试集样本数:", len(yte))
print("测试集里正样本占比:", round(yte.mean(), 3))
print("准确率:", round(model.score(Xte, yte), 4))

# 一个什么都不学的对照:全部猜「否」
print("全猜否的准确率:", round(1 - yte.mean(), 4))

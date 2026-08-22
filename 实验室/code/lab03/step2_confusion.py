from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.9, 0.1], random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
model = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
pred = model.predict(Xte)

tn, fp, fn, tp = confusion_matrix(yte, pred).ravel()
print("真阴 TN =", tn, "  假阳 FP =", fp)
print("假阴 FN =", fn, "  真阳 TP =", tp)
print()
print("精确率 = TP/(TP+FP) =", round(precision_score(yte, pred), 3), " 报为阳性的里有多少真是")
print("召回率 = TP/(TP+FN) =", round(recall_score(yte, pred), 3), " 真阳性里被抓到多少")
print("漏掉的正样本个数 FN =", fn)

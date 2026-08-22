from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.9, 0.1], random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
model = LogisticRegression(max_iter=1000).fit(Xtr, ytr)

prob = model.predict_proba(Xte)[:, 1]     # 属于正类的概率

print("阈值   报为阳性数   精确率   召回率")
for t in [0.7, 0.5, 0.3, 0.2, 0.1]:
    pred = (prob >= t).astype(int)
    p = precision_score(yte, pred, zero_division=0)
    r = recall_score(yte, pred, zero_division=0)
    print(f"{t:.1f}      {pred.sum():5d}      {p:.3f}    {r:.3f}")

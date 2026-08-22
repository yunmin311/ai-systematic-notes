import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(0)
X = rng.normal(size=(120, 3000))
y = rng.integers(0, 2, size=120)

# 错误写法(对照用):划分前就挑好了特征
X_sel = SelectKBest(f_classif, k=20).fit_transform(X, y)
bad = cross_val_score(LogisticRegression(max_iter=2000), X_sel, y, cv=5)

# ★ 正确:挑特征进流水线,每一折只看该折的训练部分
pipe = make_pipeline(SelectKBest(f_classif, k=20),
                     LogisticRegression(max_iter=2000))
good = cross_val_score(pipe, X, y, cv=5)

print("错误写法均值:", round(bad.mean(), 3))
print("正确写法均值:", round(good.mean(), 3), " ← 回到抛硬币水平,诚实")
print("虚高了:      ", round(bad.mean() - good.mean(), 3))
print()
print("正确写法每折:", np.round(good, 3))

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(0)
X = rng.normal(size=(120, 3000))          # 3000 个纯噪声特征
y = rng.integers(0, 2, size=120)          # 标签也是随机的
print("数据里没有任何规律:特征和标签互相独立")
print("所以诚实的分数应该在 0.5 上下(等于抛硬币)\n")

# ★ 错误:用全部 120 个样本挑出「最相关」的 20 个特征
X_sel = SelectKBest(f_classif, k=20).fit_transform(X, y)
bad = cross_val_score(LogisticRegression(max_iter=2000), X_sel, y, cv=5)

print("先挑特征再交叉验证(错误写法)")
print("  每折:", np.round(bad, 3))
print("  均值:", round(bad.mean(), 3), " ← 从纯噪声里「学」出来的")

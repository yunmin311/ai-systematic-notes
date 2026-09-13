import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

data = load_breast_cancer()
X = StandardScaler().fit_transform(data.data)      # 降维前必须先标准化,否则量纲大的特征会独占主成分
print(f"原始数据: {X.shape[0]} 条样本,{X.shape[1]} 个特征\n")

pca = PCA().fit(X)
cum = np.cumsum(pca.explained_variance_ratio_)
print("保留前 N 个主成分时:")
print("  N     解释了多少方差")
for n in [1, 2, 3, 5, 10, 15, 20, 30]:
    print(f"{n:>3}      {cum[n-1] * 100:>8.2f}%")

for target in [0.90, 0.95, 0.99]:
    n = int(np.searchsorted(cum, target) + 1)
    print(f"\n要保住 {target*100:.0f}% 的信息,需要 {n} 个主成分(从 30 压到 {n},{30/n:.1f} 倍)。")

X2 = PCA(n_components=2).fit_transform(X)
print(f"\n压到 2 维之后,前两个主成分各自解释了 "
      f"{pca.explained_variance_ratio_[0]*100:.1f}% 和 {pca.explained_variance_ratio_[1]*100:.1f}%。")
print("丢掉的是「不重要的方向」——但注意:不重要的方向里也可能藏着关键信息。")
print("降维是拿可解释性换可视化,不是免费的午餐。")

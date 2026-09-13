import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

# 造三堆很分明的数据。真实答案我们事先就知道:就是三堆。
X, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.9, random_state=42)
print(f"造了 {X.shape[0]} 条样本,{X.shape[1]} 个特征,真实簇数 = 3\n")

print("K    簇内平均半径    簇大小")
for k in [2, 3, 4, 5, 8]:
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    sizes = [int(n) for n in np.bincount(km.labels_, minlength=k)]
    radius = np.mean([np.linalg.norm(X[km.labels_ == i] - km.cluster_centers_[i], axis=1).mean()
                      for i in range(k)])
    print(f"{k:<4} {radius:>12.3f}    {sizes}")

print("\n① K=3 那一行的簇大小是 [100, 100, 100] —— 正好还原了造数据时的真实结构。")
print("② 但注意簇内平均半径:簇数越多它越小。K=8 时半径 0.749,比 K=3 的 1.099 好看得多。")
print("   这个指标自己没法告诉该停在哪 —— 只要愿意多切几刀,它总能更好看。")
print("   这就是无监督学习和监督学习最大的区别:没有标签,就没有一个客观的「对了」。")

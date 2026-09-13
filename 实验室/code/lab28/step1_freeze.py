import numpy as np

# 用 numpy 搭一个两层小网络。第一层(隐层)就是「通用特征」所在的位置。
# 任务故意选成线性不可分的:标签 = 两个坐标乘积的符号。
# 这样「有没有好特征」才真的决定成败 —— 换个线性可分的数据集,怎么训都差不多。

def make_data(n, pairs, seed):
    """每条的标签 = 随机挑一对坐标,看它们乘积是正是负。
       线性不可分,靠一个权重矩阵直接分不开,必须先造出「乘积」这种特征。"""
    r = np.random.default_rng(seed)
    X = r.normal(0, 1.0, size=(n, DIM))
    k = r.integers(0, len(pairs), size=n)
    i = np.array([pairs[t][0] for t in k])
    j = np.array([pairs[t][1] for t in k])
    y = ((X[np.arange(n), i] * X[np.arange(n), j]) > 0).astype(int)
    return X, y

def init(classes, seed=0):
    r = np.random.default_rng(seed)
    return {"W1": r.normal(0, 0.3, (DIM, HIDDEN)), "b1": np.zeros(HIDDEN),
            "W2": r.normal(0, 0.3, (HIDDEN, classes)), "b2": np.zeros(classes)}

def forward(p, X):
    h = np.maximum(0, X @ p["W1"] + p["b1"])      # ReLU —— 隐层,也就是「特征层」
    return h, h @ p["W2"] + p["b2"]

def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

def train(p, X, y, epochs, lr, freeze_feature):
    """freeze_feature=True 就冻住特征层,只训输出头"""
    n, classes = len(y), p["W2"].shape[1]
    oh = np.zeros((n, classes)); oh[np.arange(n), y] = 1
    for _ in range(epochs):
        h, logits = forward(p, X)
        dlogits = (softmax(logits) - oh) / n
        if not freeze_feature:
            dh = (dlogits @ p["W2"].T) * (h > 0)   # ReLU 的导数
            p["W1"] -= lr * (X.T @ dh)
            p["b1"] -= lr * dh.sum(0)
        p["W2"] -= lr * (h.T @ dlogits)
        p["b2"] -= lr * dlogits.sum(0)
    return p

def accuracy(p, X, y):
    return (forward(p, X)[1].argmax(1) == y).mean()

DIM, HIDDEN, HEAD_SEED = 20, 64, 99

# ---- 上游 A:预训练任务和下游「同一件事」——四对坐标,其中就有下游要用那对 ----
UP_STRONG = [(2, 3), (4, 5)]
# ---- 上游 B:预训练任务和下游只是「有点关系」——四对混在一起 ----
UP_WEAK = [(0, 1), (2, 3), (4, 5), (6, 7)]

def downstream(n, seed):
    return make_data(n, [(2, 3)], seed)

def pretrain(pairs, n=4000, epochs=1500):
    X, y = make_data(n, pairs, seed=1)
    m = train(init(2), X, y, epochs, 0.5, freeze_feature=False)
    return m, accuracy(m, X, y)

def compare(pre, label):
    print(f"\n{label}")
    print(f"{'下游标签数':<12}{'A 从头训':>11}{'B 冻结特征':>13}{'C 微调全部':>13}")
    out = []
    for n in [6, 20, 100, 400]:
        Xtr, ytr = downstream(n, seed=7)
        Xte, yte = downstream(800, seed=8)
        h = init(2, seed=HEAD_SEED)
        base = dict(W1=h['W1'].copy(), b1=h['b1'].copy(), W2=h['W2'].copy(), b2=h['b2'].copy())
        a = train({k: v.copy() for k, v in base.items()}, Xtr, ytr, 400, 0.5, False)
        b = train(dict(W1=pre['W1'].copy(), b1=pre['b1'].copy(), W2=base['W2'].copy(), b2=base['b2'].copy()),
                  Xtr, ytr, 400, 0.5, True)
        c = train(dict(W1=pre['W1'].copy(), b1=pre['b1'].copy(), W2=base['W2'].copy(), b2=base['b2'].copy()),
                  Xtr, ytr, 400, 0.05, False)
        ra, rb, rc = accuracy(a, Xte, yte), accuracy(b, Xte, yte), accuracy(c, Xte, yte)
        out.append((n, ra, rb, rc))
        print(f'{n:>8} 条  {ra:>10.1%}{rb:>13.1%}{rc:>13.1%}')
    return out

print('同一件下游任务(只用第 2、3 两个坐标,标签很少),三种做法:')
print('   A 从头训    随机初始化,两层都在下游的小数据上学 —— 等于不用预训练模型')
print('   B 冻结特征  抄来上游的特征层并冻住,只训新换的输出头')
print('   C 微调全部  抄来上游的特征层但解冻,用小学习率一起调')

pre_strong, acc_s = pretrain(UP_STRONG)
pre_weak,   acc_w = pretrain(UP_WEAK)
strong = compare(pre_strong, f'【上游 A:两对坐标 {UP_STRONG},上游准确率 {acc_s:.0%}】—— 和下游高度相关')
weak   = compare(pre_weak,   f'【上游 B:四对坐标 {UP_WEAK},上游准确率 {acc_w:.0%}】—— 和下游只是有点关系')

print('\n两张表对着看,才是这一节真正的结论:')
print(f"   上游 A(高度相关):数据少时冻结领先 {strong[0][2]-strong[0][1]:.1%},")
print(f"      数据多时依然领先 {strong[-1][2]-strong[-1][1]:.1%} —— 迁移一直划算。")
print(f"   上游 B(只是有点关系):数据少时优势只剩 {weak[0][2]-weak[0][1]:.1%},")
print(f"      到 {weak[-1][0]} 条时从头训反超 {weak[-1][1]-weak[-1][2]:+.1%} —— 迁移变成了负担。")
print()
print('所以 D11 那句「数据够时微调更好」要补一个前提:两个任务得多相关。')
print('   相关 + 数据少 → 冻结特征,快、稳、省算力;')
print('   不相关   → 预训练那层帮不上忙,反而要额外纠正它的偏差;')
print('   数据够多 → 自己的数据能学出特征,从头训是最干净的。')
print()
print('这也解释了一个常见困惑:为什么拿一个通用大模型微调,有时效果好得惊人,')
print('   有时几乎没变化 —— 差别往往不在调参,而在「任务离它原来学的有多远」。')

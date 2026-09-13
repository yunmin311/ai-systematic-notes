import numpy as np

def cos(a, b):
    return (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euc(a, b):
    return np.linalg.norm(a - b)

# 三篇文档的词频向量,维度是 [猫, 狗, 鱼]
A = np.array([10, 10, 0], dtype=float)   # 长文,只讲猫狗
B = np.array([ 1,  1, 0], dtype=float)   # 短文,也只讲猫狗(同一主题,只是短)
C = np.array([ 8,  8, 9], dtype=float)   # 和 A 差不多长的文,猫狗为主但也讲了不少鱼

print("三篇文档的词频向量(维度: 猫 / 狗 / 鱼):")
for name, v, note in [("A", A, "长文·只讲猫狗"), ("B", B, "短文·只讲猫狗"), ("C", C, "长文·猫狗+鱼")]:
    print(f"   {name} = {v.astype(int)}    {note}")

print("\nA 和谁更接近?两种度量给出相反的答案:")
print("   组合     余弦相似度    欧氏距离")
for n1, v1, n2, v2 in [("A", A, "B", B), ("A", A, "C", C)]:
    print(f"   {n1}–{n2}     {cos(v1, v2):>8.3f}     {euc(v1, v2):>8.3f}")

print(f"\n余弦:      A–B = {cos(A,B):.3f} > A–C = {cos(A,C):.3f}   → B 更近,判对了")
print(f"欧氏距离:  A–B = {euc(A,B):.2f} > A–C = {euc(A,C):.2f}   → 说 C 更近,判错了")
print("\n欧氏距离为什么会判错?因为它把「向量有多长」也算进去了。")
print("B 是短文,词频整体偏小,于是它离 A 的直线距离被拉得很远——")
print("可 B 和 A 的方向完全一致,讲的是一模一样的事。")
print("\n文本里「长度」来自篇幅、重复次数、文档粗细,和「在讲什么」无关。")
print("所以判断意思像不像要用余弦(只看方向,不看长度),这也是 RAG 向量检索的默认度量。")

import numpy as np

def conv2d(image, kernel):
    H, W = image.shape
    kh, kw = kernel.shape
    out = np.zeros((H - kh + 1, W - kw + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = (image[i:i+kh, j:j+kw] * kernel).sum()
    return out

def maxpool(x, size=2):
    """最大池化:每 size×size 一块,只留最大值"""
    H, W = x.shape
    out = np.zeros((H // size, W // size))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = x[i*size:(i+1)*size, j*size:(j+1)*size].max()
    return out

K = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)

img = np.zeros((8, 8)); img[:, 3:] = 9          # 竖直边在第 3 列
f = conv2d(img, K)
print(f"卷积后的特征图 {f.shape}(亮起的地方就是找到了竖边):")
for row in f:
    print("   " + " ".join(f"{int(v):>3}" for v in row))

p = maxpool(f)
print(f"\n最大池化 2×2 之后 {p.shape} —— 面积缩到四分之一:")
for row in p:
    print("   " + " ".join(f"{int(v):>3}" for v in row))
print(f"峰值 {f.max():.0f} 原样保留 —— 池化扔掉位置细节,但不丢「有没有」。")

# ---- 卷积真正厉害的地方:平移等变性 ----
img2 = np.zeros((8, 8)); img2[:, 4:] = 9        # 同一条边,整体右移 1 像素
f2 = conv2d(img2, K)
print("\n把整条边右移 1 个像素,看特征图怎么变:")
print(f"   最大值:        {f.max():.0f} → {f2.max():.0f}   ← 完全不变")
print(f"   第一行原位置:  " + " ".join(f"{int(v):>3}" for v in f[0]))
print(f"   第一行新位置:  " + " ".join(f"{int(v):>3}" for v in f2[0]))
print( "   亮点整体跟着挪了一格 —— 这就是「平移等变」:")
print( "   同一个核滑遍全图,模式出现在哪儿它都能认出来,不需要为每个位置各备一套权重。")

# ---- 池化能吸收多少位移,如实量一下 ----
d_conv = (f != f2).mean() * 100
d_pool = (p != maxpool(f2)).mean() * 100
print(f"\n量化「对位移有多敏感」(逐元素不同的比例):")
print(f"   卷积特征图: {d_conv:.0f}% 的位置变了")
print(f"   池化之后:   {d_pool:.0f}% 的位置变了")
print( "   注意两行一样:池化在这个例子里一点也没降下来。")
print( "   原因是位移方向和池化的块边界正好错开,亮点从第 1 块挪到了第 2 块。")
print( "   所以「池化提供平移不变性」是有条件的 —— 只有当位移落在同一个块内才吸收得住。")
print( "   真正让 CNN 对平移稳健的,是卷积的参数共享 + 大量数据 + 数据增强,不是池化一项。")

# ---- 感受野:每堆一层,一个神经元能看到多大范围 ----
print("\n每堆一层 3×3 卷积,单个神经元能看到的原图范围(感受野):")
for L in range(1, 9):
    print(f"   堆 {L} 层  →  感受野 {1 + 2 * L} × {1 + 2 * L}")
print("\n第 8 层的一个神经元,看到的是原图 17×17 的范围。")
print("浅层看边缘和颜色块,中层看纹理和部件,深层看整体——")
print("「从局部到整体」不是人设计的,是层层堆叠自然长出来的。")

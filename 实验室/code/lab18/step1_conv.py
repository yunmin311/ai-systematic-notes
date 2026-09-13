import numpy as np

# 一张 8×8 的小图:左半黑、右半亮,中间是一条竖直的边
img = np.array([
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
    [0, 0, 0, 9, 9, 9, 9, 9],
], dtype=float)

print("原图(左半 0 = 黑,右半 9 = 亮),中间是一条竖直边:")
for row in img:
    print("   " + "".join("#" if v > 4 else "." for v in row))

def conv2d(image, kernel):
    """让核滑过整张图:每个位置把窗口和核逐个相乘再相加"""
    H, W = image.shape
    kh, kw = kernel.shape
    out = np.zeros((H - kh + 1, W - kw + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = (image[i:i+kh, j:j+kw] * kernel).sum()
    return out

# 两个核,只差一个转置:一个专找竖边,一个专找横边
K_vertical = np.array([[-1, 0, 1],
                       [-1, 0, 1],
                       [-1, 0, 1]], dtype=float)
K_horizontal = K_vertical.T

print("\n① 竖边检测核(左列 -1、右列 +1):")
print("   " + "\n   ".join(str(r) for r in K_vertical))
f_v = conv2d(img, K_vertical)
print("   滑过之后得到的特征图:")
for row in f_v:
    print("   " + " ".join(f"{int(v):>4}" for v in row))

print("\n② 横边检测核(把上面那个转置):")
f_h = conv2d(img, K_horizontal)
print("   滑过之后得到的特征图:")
for row in f_h:
    print("   " + " ".join(f"{int(v):>4}" for v in row))

print(f"\n竖边核的最大响应 = {f_v.max():.0f},横边核的最大响应 = {f_h.max():.0f}")
print("这张图里只有竖直的边,所以竖边核被强烈激活、横边核几乎没反应——")
print("这就是卷积的核心:同一个核滑遍全图,在「它认识的那种局部模式」出现的地方亮起来。")

print(f"\n参数账:两个核一共 {K_vertical.size + K_horizontal.size} 个权重。")
print("如果改用全连接层处理 8×8 = 64 个像素,每个输出神经元就要 64 个权重。")
print("而卷积核滑到每个位置用的都是同一套 9 个权重 —— 这就是「参数共享」。")

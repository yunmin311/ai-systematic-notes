import numpy as np

# 一个神经元做三步:加权求和 → 加偏置 → 用激活函数压一下
x = np.array([0.8, 0.3])          # 两个输入
W = np.array([0.5, -0.2])         # 每个输入的权重
b = 0.1                           # 偏置

z = (x * W).sum() + b             # ① 加权求和,再加偏置
print(f"① 加权求和:  {x[0]}×{W[0]} + {x[1]}×{W[1]} + {b} = {z:.4f}")

def relu(t):  return max(0.0, t)
def sigmoid(t): return 1 / (1 + np.exp(-t))

print(f"② ReLU 压一下:    {relu(z):.4f}   ← 负数直接归零,正数原样过")
print(f"② Sigmoid 压一下: {sigmoid(z):.4f}   ← 压到 0~1 之间,可以当概率读")

print("\n为什么非要有第 ② 步?把激活去掉,两层网络会塌成一层:")
np.random.seed(0)
A = np.random.randn(3, 3)
print(f"   两层都是纯线性时, W2 @ (W1 @ x) 等于 (W2 @ W1) @ x")
print(f"   两个矩阵相乘的结果形状是 {(A @ A).shape} —— 还是一个矩阵。")
print("   堆再多层也只等价于一层,所以激活函数不是可选装饰,是「能堆多层」的前提。")

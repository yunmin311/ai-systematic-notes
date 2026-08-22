import torch

torch.manual_seed(0)
x = torch.rand(200) * 2 - 1
y = 3 * x + 2 + torch.randn(200) * 0.1

w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
opt = torch.optim.SGD([w, b], lr=0.1)
lossfn = torch.nn.MSELoss()

for step in range(1, 201):
    pred = w * x + b             # ① 前向
    loss = lossfn(pred, y)       # ② 算损失
    opt.zero_grad()              # ③ 梯度清零(漏了会累加,见第 3 步)
    loss.backward()              # ④ 反向传播:框架自动求导
    opt.step()                   # ⑤ 更新参数
    if step % 50 == 0:
        print(f"step {step:3d}  loss={loss.item():.5f}  w={w.item():.4f}  b={b.item():.4f}")

print("\nPyTorch 版最终: w =", round(w.item(), 4), " b =", round(b.item(), 4))

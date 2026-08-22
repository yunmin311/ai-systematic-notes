import torch

torch.manual_seed(0)
x = torch.rand(200) * 2 - 1
y = 3 * x + 2 + torch.randn(200) * 0.1

w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
opt = torch.optim.SGD([w, b], lr=0.1)
lossfn = torch.nn.MSELoss()

for step in range(1, 21):
    pred = w * x + b
    loss = lossfn(pred, y)
    # opt.zero_grad()          # ★ 故意注释掉(正常应该在这里)
    loss.backward()
    if step <= 5:
        print(f"step {step}  loss={loss.item():.4f}  w.grad={w.grad.item():.4f}")
    opt.step()

print("\n20 步之后: w =", round(w.item(), 4), " b =", round(b.item(), 4), " (期望 3 和 2)")

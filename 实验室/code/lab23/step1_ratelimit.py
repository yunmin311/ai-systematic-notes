# 用「逻辑时钟」而不是真实时间,这样每次跑结果完全一样。
# 真实系统用 time.monotonic(),逻辑一样。

class FixedWindow:
    """固定窗口:每 10 秒一个窗口,每窗最多 5 次。简单,但有个经典缺陷。"""
    def __init__(self, limit, window=10):
        self.limit, self.window = limit, window
        self.count, self.win_start = 0, 0
    def allow(self, t):
        if t - self.win_start >= self.window:      # 进入新窗口,计数清零
            self.win_start, self.count = t, 0
        if self.count < self.limit:
            self.count += 1
            return True
        return False

class TokenBucket:
    """令牌桶:桶里最多 5 个令牌,每 2 秒补 1 个。允许短暂的突发。"""
    def __init__(self, capacity=5, refill_every=2):
        self.capacity, self.refill_every = capacity, refill_every
        self.tokens, self.last = capacity, 0
    def allow(self, t):
        added = (t - self.last) // self.refill_every       # 这段时间该补几个
        if added:
            self.tokens = min(self.capacity, self.tokens + added)
            self.last += added * self.refill_every
        if self.tokens > 0:
            self.tokens -= 1
            return True
        return False

patterns = {
    "A 突发":   [0] * 8 + [1, 2, 3, 4, 5, 6],
    "B 跨窗口": [9] * 5 + [11] * 5,
}

for pname, traffic in patterns.items():
    print(f"流量模式 {pname}:共 {len(traffic)} 次请求,时间点 {traffic}")
    for name, lim in [("固定窗口", FixedWindow(5)), ("令牌桶", TokenBucket())]:
        ok = [lim.allow(t) for t in traffic]
        blocked = [i + 1 for i, v in enumerate(ok) if not v]
        tail = f"被挡:{blocked}" if blocked else "全部放行"
        print(f"   {name}   通过 {sum(ok):>2}/{len(traffic)}   {tail}")
    print()

print("两个模式各暴露一件事:")
print("   模式 A(突发):固定窗口挡掉 9 次,令牌桶只挡 6 次。")
print("     同一段流量,固定窗口明显更严 —— 它只数「这个窗口里发了几次」,")
print("     不管请求是均匀来的还是挤在一瞬间来的。")
print("   模式 B(跨窗口):固定窗口把 10 次全部放行了,令牌桶挡掉 4 次。")
print("     固定窗口在第 10 秒把计数清零了 —— 于是 t=9 的 5 次和 t=11 的 5 次")
print("     落在两个窗口里,各自合法,合起来却是在 3 秒内打了 10 次。")
print("     这是它的经典缺陷:限制的是「每个窗口内的次数」,不是「任意 10 秒内的次数」。")
print("     令牌桶没被绕过去,因为它按时间补令牌,压根不看窗口边界在哪。")
print()
print("这就是 A07 说的「稳」:限流不是把用户挡在外面,是让服务在被打的时候还能喘气。")
print("而选哪种算法,取决于业务能不能容忍突发、以及需不需要防住这种边界绕过。")

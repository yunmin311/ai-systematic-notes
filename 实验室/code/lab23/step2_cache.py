# 模拟一天的请求。固定随机种子,保证每次跑结果一样。
import random
random.seed(0)

TOTAL = 1000
HOT = ["怎么调亮度", "保修几年", "灯自己灭了", "能定时吗", "怎么连接手机"]

# 真实客服流量是「少量热门 + 长长一条长尾」:
# 大约四成落在那 5 个热门问题上,其余六成各问各的,基本不重复。
day = []
for i in range(TOTAL):
    if random.random() < 0.4:
        day.append(random.choice(HOT))          # 热门的,高度重复
    else:
        day.append(f"长尾问题_{i}")              # 长尾的,每个只出现一次

SYSTEM, DOCS, QUESTION, ANSWER = 320, 1800, 40, 400
PRICE_IN, PRICE_OUT = 1.5 / 1e6, 6.0 / 1e6
PREFIX_DISCOUNT = 0.1        # 命中前缀缓存的那部分输入,按 10% 计价

def cost(inp, out):
    return inp * PRICE_IN + out * PRICE_OUT

base_in = SYSTEM + DOCS + QUESTION
no_cache = TOTAL * cost(base_in, ANSWER)

# ---- 方案 1:整条缓存(问题 + 上下文完全相同才算命中) ----
seen, hits1, cost1 = set(), 0, 0.0
for q in day:
    if q in seen:
        hits1 += 1                    # 命中,直接返回,这次一分钱不花
    else:
        seen.add(q)
        cost1 += cost(base_in, ANSWER)

# ---- 方案 2:前缀缓存(系统提示 + 资料 固定,这部分输入按折价算) ----
fixed = SYSTEM + DOCS
cost2 = TOTAL * cost(fixed * PREFIX_DISCOUNT + QUESTION, ANSWER)

print(f"一天 {TOTAL} 次请求:约四成落在 5 个热门问题上,其余是长尾(各问一次)。\n")
print(f"{'方案':<22}{'一天成本':>11}{'省下':>9}   说明")
print(f"{'0 不缓存':<20}{no_cache:>11.4f}{'—':>9}   每次都全价")
print(f"{'1 整条缓存':<19}{cost1:>11.4f}{(1-cost1/no_cache):>8.1%}   命中 {hits1} 次,命中就直接返回不调模型")
print(f"{'2 前缀缓存':<19}{cost2:>11.4f}{(1-cost2/no_cache):>8.1%}   每次都调模型,但固定前缀按一折算")

top5 = sum(1 for q in day if q in HOT)
print(f"\n流量构成:热门问题 {top5} 次({top5/TOTAL:.1%}),长尾 {TOTAL-top5} 次({(TOTAL-top5)/TOTAL:.1%})")

print("\n这张表里最反直觉的一格:整条缓存的命中率被长尾拖住了。")
print(f"   热门问题来了 {top5} 次,但每种第一次都得真调,所以真正省下的只有 {hits1} 次")
print(f"   ({(1-cost1/no_cache):.1%});长尾那 {TOTAL-top5} 次一次也省不到。")
print("   而前缀缓存不管问题重复不重复 —— 只要系统提示和资料一样就算命中,")
print(f"   所以它一次不落地省下 {(1-cost2/no_cache):.1%},反而比整条缓存省得多。")

print("\n两者的长处完全不同,所以真实系统两个一起上:")
print("   整条缓存:命中就完全不出钱、延迟还低,但要求问题一字不差;")
print("   前缀缓存:命中门槛低、覆盖面广,但每次仍要调模型,只是那一段打折。")
print("   一个捡「几乎一样的请求」,一个覆盖「所有请求的固定部分」,互补。")

print("\n这也是 A07 说的「可持续」:不是砍功能,是把每次都得付的那笔固定开销压下来。")

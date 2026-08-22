/* 口吻自检 · 禁「对读者说话」与「AI 汇报进度」
   用法:  node _工具\口吻自检.mjs
   由来:  2026-08-21。index.html 曾挂着一块「现在该做什么 / 从第 1 章顺着往下读 /
          8 章已全部开放」——那是 AI 在对人说话、在汇报自己的进度,不是讲义。
          全站当时还有 746 处「你」。规则记住了没用,只有这个脚本靠得住。

   讲义的口吻是:陈述事实、解释机制。不是:
     · 用「你」称呼读者(「你会发现」「替你」「教你」「给你」)
     · 发号施令(「现在该做什么」「顺着往下读」「记得先…」)
     · 汇报自己干了什么(「已全部开放」「本轮完成」「均已写完」)

   例外(白名单):示例提示词与模型输出的原文、产品名、领域术语——见 KEEP。
*/
import { readFileSync, readdirSync, statSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const SKIP_DIR = ['_备份', '_工具', '_样本预览', 'node_modules', 'assets']

// 白名单:这些里的「你」是被引用的原文,不是在对读者说话
const KEEP = [
  '迷你',            // mini
  '猜你喜欢',        // 推荐系统的功能名
  '你是一位',        // 示例提示词原文
  '你要去北京',      // 示例模型输出原文
  '"你好"',          // 示例测试输入
  '你有一个',        // 示例工具说明原文
  '模型这一轮',      // agent loop 的一轮,不是「本轮工作汇报」
  '本轮对话',        // 领域说法
  '它们互相不知道对方存在,也不知道整体结构是什么',  // 讲义里引用的示例句
  '你确定吗',        // 反面示例:讲义在讲「别这么问」
  '你确不确定',      // 同上
]

const PAT = [
  ['对读者说话', /你/g],
  ['发号施令', /现在该做什么|接下来该|下一步该|请你|建议你|不妨|别忘了|(?<!靠|指望|人|都)记得(?:先|把|去)|顺着往下读|再进下一章|别贪多|跟着我|我们一起/g],
  ['汇报进度', /已全部开放|均已完成开放|全部完成|可以并行推进|已经写完|目前已/g],
]

const files = []
;(function walk(d) {
  for (const n of readdirSync(d)) {
    if (SKIP_DIR.includes(n)) continue
    const p = join(d, n)
    if (statSync(p).isDirectory()) walk(p)
    else if (n.endsWith('.html')) files.push(p)
  }
})(ROOT)
// assets 里的 .js 也要查——文案写在脚本里一样会显示给人看(2026-08-21 补)
;(function () {
  const a = join(ROOT, 'assets')
  try {
    for (const n of readdirSync(a)) if (n.endsWith('.js') || n.endsWith('.py')) files.push(join(a, n))
  } catch { /* 没有 assets 就算了 */ }
})()

let total = 0
const rows = []
for (const f of files) {
  let s = readFileSync(f, 'utf8')
  // 代码块里的字符串不算
  s = s.replace(/<pre[\s\S]*?<\/pre>|<code[\s\S]*?<\/code>|<style[\s\S]*?<\/style>/g, '')
  s = s.replace(/<[^>]+>/g, '')          // 去标签,免得「这一轮</b>的」骗过白名单
  for (const k of KEEP) s = s.split(k).join('')
  const hits = []
  for (const [name, re] of PAT) {
    const m = s.match(re)
    if (m) hits.push(`${name} ${m.length} 处(${[...new Set(m)].slice(0, 5).join('/')})`)
  }
  if (hits.length) {
    const n = hits.reduce((a, h) => a + +h.match(/ (\d+) 处/)[1], 0)
    total += n
    rows.push([f.substring(ROOT.length + 1), hits.join(' | ')])
  }
}

console.log(`\n口吻自检 · ${files.length} 个页面\n${'='.repeat(58)}`)
if (!rows.length) console.log('干净:没有对读者说话、没有发号施令、没有进度汇报。')
rows.forEach(([f, h]) => console.log(`  ${f}\n      ${h}`))
console.log(`\n合计 ${total} 处` + (total ? '  ← 逐条改成中性陈述;确属引用原文的,加进本脚本的 KEEP' : ''))
process.exit(total ? 1 : 0)

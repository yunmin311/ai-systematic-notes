/* 口吻自检 · 笔记必须是「第一人称独白」
   用法:  node _工具\口吻自检.mjs            正常检查
          node _工具\口吻自检.mjs --rebase   把当前正文字数记成新基线(删内容前要想清楚)

   由来(两次事故,都记在这里):
   一、2026-08-21 上午:index.html 挂着「现在该做什么 / 从第 1 章顺着往下读 / 8 章已全部开放」——
       那是 AI 在对人说话、在汇报自己的进度。全站另有 746 处「你」。
   二、2026-08-21 下午:上一版脚本只查「有没有『你』」,于是我把 620 个「你」直接删掉,
       「我」一个没增、正文净减 812 字、39 篇全变短——**脚本判绿了**。
       一个只会查禁用词、不会查句子还通不通的脚本,是在给坏改动发合格证。

   笔记的口吻是**第一人称独白**:「我发现」「我在 Claude Code 里见过」「我这台电脑」。
   不是对读者说话(「你会发现」),也不是无人称说明书(「会发现」)。

   所以查四项:
     ① 对读者说话   正文里出现「你」(白名单除外)
     ② 发号施令     「现在该做什么」「顺着往下读」「记得先…」
     ③ 汇报进度     「已全部开放」「本轮完成」「均已写完」
     ④ 人称密度     讲义类每千字「我」不得低于下限——低了就是被写成了无人称说明书
     ⑤ 正文字数     不得低于基线——**这一条专门防「把词删掉当改好」**
*/
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs'
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
  // 2026-09-10:U03 题库在考「页面不许对读者说话」这条规则,题干必须引用它的禁用词原文。
  // 这是「规则的检查对象」而不是「对读者说话」,属于引用,放行。
  '「你」「现在该做什么」',
]

const PAT = [
  ['对读者说话', /你/g],
  ['发号施令', /现在该做什么|接下来该|下一步该|请你|建议你|不妨|别忘了|(?<!靠|指望|人|都)记得(?:先|把|去)|顺着往下读|再进下一章|别贪多|跟着我(?:做|走|来|一起)|我们一起/g],
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
console.log('① ② ③ 禁用口吻')
if (!rows.length) console.log('   干净:没有对读者说话、没有发号施令、没有进度汇报。')
rows.forEach(([f, h]) => console.log(`   ${f}\n       ${h}`))
console.log(`   合计 ${total} 处` + (total ? '  ← 改成第一人称;确属引用原文的,加进 KEEP' : ''))

/* ────────── ④ 人称密度 · ⑤ 正文字数基线 ────────── */
const FLOOR = 1.2          // 讲义类每千字「我」的下限。当时 39 篇里最低的是 1.46,留了余量
const GRADED = ['基础课程', '深度课程', '应用工程', '项目']   // 现在就按下限卡的
// 新板块的人称还没补(2026-08-21 用户明确要求先别动手,只登记)。列出来但不判失败。
const PENDING = ['AI使用', '实验室', '排障台', '台账']
const BASE_FILE = join(ROOT, '_工具', '正文字数基线.json')

const plain = s => s.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, '')
  .replace(/<[^>]+>/g, '').replace(/\s+/g, '')
const stat = f => {
  const t = plain(readFileSync(f, 'utf8'))
  return { w: t.length, me: (t.match(/我/g) || []).length }
}
const groupOf = rel => (rel.split(/[\\/]/)[0])

const thin = [], pending = [], now = {}
for (const f of files) {
  if (!f.endsWith('.html')) continue
  const rel = f.substring(ROOT.length + 1).replace(/\\/g, '/')
  const g = groupOf(rel)
  const { w, me } = stat(f)
  now[rel] = w
  if (w < 800) continue                       // 太短的入口页不参与密度判断
  const d = me / w * 1000
  if (GRADED.includes(g) && d < FLOOR) thin.push([rel, w, me, d])
  else if (PENDING.includes(g) && d < FLOOR) pending.push([rel, w, me, d])
}

console.log(`\n④ 人称密度(讲义类每千字「我」≥ ${FLOOR})`)
if (!thin.length) console.log('   全部达标。')
thin.sort((a, b) => a[3] - b[3]).forEach(([r, w, m, d]) =>
  console.log(`   ✗ ${d.toFixed(2)}  ${m} 个 / ${w} 字   ${r}`))
if (pending.length)
  console.log(`   ⏳ 已登记待办(2026-08-21,用户暂缓):${pending.length} 个新板块页面人称密度偏低,不计入失败`)

/* ⑤ 字数基线 */
let base = null
try { base = JSON.parse(readFileSync(BASE_FILE, 'utf8')) } catch { }
const REBASE = process.argv.includes('--rebase')
const shrunk = []
if (base && !REBASE) {
  for (const [rel, w] of Object.entries(now)) {
    const b = base.files[rel]
    if (b === undefined) continue
    if (w < b) shrunk.push([rel, b, w])
  }
}
console.log(`\n⑤ 正文字数基线` + (base ? `(基线记于 ${base.date})` : '(还没有基线)'))
if (REBASE || !base) {
  const total_w = Object.values(now).reduce((a, b) => a + b, 0)
  const d = new Date(), p = n => (n < 10 ? '0' : '') + n
  const stamp = `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`
  writeFileSync(BASE_FILE, JSON.stringify({ date: stamp, total: total_w, files: now }, null, 1))
  console.log(`   已写入新基线:${Object.keys(now).length} 个页面,正文合计 ${total_w} 字`)
} else if (!shrunk.length) {
  console.log('   没有页面比基线短。')
} else {
  shrunk.sort((a, b) => (a[2] - a[1]) - (b[2] - b[1])).forEach(([r, b, w]) =>
    console.log(`   ✗ ${w - b} 字  ${b} → ${w}   ${r}`))
  console.log('   ← 正文变短了。若确属该删,跑一次 --rebase 把新字数记成基线;否则就是又在删字。')
}

const failed = total || thin.length || shrunk.length
console.log(`\n${failed ? '不合格' : '全部通过'}`)
process.exit(failed ? 1 : 0)

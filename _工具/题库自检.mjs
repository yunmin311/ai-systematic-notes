/* 题库自检 · 出题偏差检测
   用法:  node _工具\题库自检.mjs
   目的:  出新题之后跑一次,防止「不读题也能蒙对」的系统性偏差再次出现。
          这个脚本是机械机制——规则记住了不算数,跑出来绿了才算数。

   查四项:
     ① 正确答案的位置分布(A/B/C/D 是否各约 25%)
     ② 正确选项是否系统性偏长(平均字数比 / 「正确=最长」的题数占比)
     ③ 判断题「对/错」是否失衡
     ④ 明显比同题其他选项短得多的选项(疑似一眼假干扰项,人工复看)
   最后给一个总闸:蒙题策略能得多少分。等于随机基准才算过。
*/
import { readFileSync, readdirSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const DIR = join(dirname(fileURLToPath(import.meta.url)), '..', '题库')

// ---- 合格线 ----
const LIMIT = {
  posMax: 0.32,        // 单个位置占比上限(理想 0.25)
  lenRatio: 1.15,      // 正确项平均字数 / 错误项平均字数 的上限
  longestShare: 0.45,  // 「正确项比所有错项都长」的题数占比上限
  judgeSkew: 0.65,     // 判断题里占多数的那一边的占比上限
  shortRatio: 0.45,    // 某选项 < 同题最长项的 45% → 标记为疑似一眼假
}

const files = readdirSync(DIR).filter(f => /^quiz-.+\.html$/.test(f)).sort()
const G = { pos: [0, 0, 0, 0], nMC: 0, cLen: 0, wLen: 0, wN: 0, longest: 0, shortest: 0,
            jT: 0, jF: 0, guess: 0, guessMax: 0 }
const bad = []   // 点名的文件
const suspects = []

for (const f of files) {
  const src = readFileSync(join(DIR, f), 'utf8')
  // 2026-08-30 修:原来是 `;\n<\/script>`,只认 LF。库里 98 个 HTML 是 CRLF(Windows),
  // `];\r\n</script>` 匹配不上 → 32 份全报「解析失败」,样本 0 反而让总闸判绿(假绿灯)。
  // 改成 `;\s*<\/script>`,LF / CRLF 都认。
  const m = src.match(/window\.QUESTIONS = ([\s\S]*?);\s*<\/script>/)
  if (!m) { bad.push([f, '解析失败:找不到 window.QUESTIONS']); continue }
  let qs
  try { qs = Function('return ' + m[1])() } catch (e) { bad.push([f, '解析失败:' + e.message]); continue }
  const id = f.replace(/^quiz-|\.html$/g, '')

  const L = { pos: [0, 0, 0, 0], nMC: 0, cLen: 0, wLen: 0, wN: 0, longest: 0, shortest: 0, jT: 0, jF: 0 }

  qs.forEach((q, i) => {
    if (!q.options) return                       // 开放题不参与
    if (q.type === 'judge') {
      // 约定 options = ['对','错'] 之类,answer 0 = 对
      if (q.answer === 0) { L.jT++; G.jT++ } else { L.jF++; G.jF++ }
      G.guessMax++
      if (q.answer === 1) G.guess++              // 蒙题策略:一律选「错」
      return
    }
    if (q.options.length !== 4) return
    L.nMC++; G.nMC++
    L.pos[q.answer]++; G.pos[q.answer]++
    G.guessMax++
    if (q.answer === 1) G.guess++                // 蒙题策略:一律选 B

    const c = q.options[q.answer].length
    const others = q.options.filter((_, k) => k !== q.answer).map(o => o.length)
    L.cLen += c; G.cLen += c
    others.forEach(n => { L.wLen += n; L.wN++; G.wLen += n; G.wN++ })
    if (c > Math.max(...others)) { L.longest++; G.longest++ }

    if (c < Math.min(...others)) { L.shortest++; G.shortest++ }

    const max = Math.max(c, ...others)
    if (max >= 14) q.options.forEach((o, k) => {   // 纯数字/公式题的选项天然短,不算
      if (o.length / max < LIMIT.shortRatio)
        suspects.push(`${id}#${i} 选项${'ABCD'[k]}(${o.length}字 vs 本题最长${max}字) ${o.slice(0, 34)}`)
    })
  })

  // 逐文件点名
  const msgs = []
  if (L.nMC >= 12) {
    const worst = Math.max(...L.pos) / L.nMC
    if (worst > LIMIT.posMax)
      msgs.push(`位置偏斜 ${L.pos.map((n, k) => 'ABCD'[k] + ':' + n).join(' ')}(最高 ${(worst * 100).toFixed(0)}%)`)
  }
  if (L.nMC >= 8) {   // 题量太少时这两个统计没有意义
    const r = (L.cLen / L.nMC) / (L.wLen / L.wN)
    if (r > LIMIT.lenRatio)
      msgs.push(`正确项偏长 ${r.toFixed(2)}×(正确均 ${(L.cLen / L.nMC).toFixed(1)}字 / 错项均 ${(L.wLen / L.wN).toFixed(1)}字)`)
    const ls = L.longest / L.nMC
    if (ls > LIMIT.longestShare)
      msgs.push(`「正确=最长」占 ${(ls * 100).toFixed(0)}%(${L.longest}/${L.nMC})`)
  }
  const jn = L.jT + L.jF
  if (jn >= 4 && Math.max(L.jT, L.jF) / jn > LIMIT.judgeSkew)
    msgs.push(`判断题失衡 对:${L.jT} 错:${L.jF}`)
  if (msgs.length) bad.push([f, msgs.join(' | ')])
}

const pct = n => (n / G.nMC * 100).toFixed(1) + '%'
const ratio = (G.cLen / G.nMC) / (G.wLen / G.wN)
const randomBase = G.nMC * 0.25 + (G.jT + G.jF) * 0.5

console.log(`\n题库自检 · ${files.length} 份 · 四选一 ${G.nMC} 道 · 判断 ${G.jT + G.jF} 道\n${'='.repeat(58)}`)
console.log(`① 答案位置    A ${G.pos[0]} (${pct(G.pos[0])})  B ${G.pos[1]} (${pct(G.pos[1])})  C ${G.pos[2]} (${pct(G.pos[2])})  D ${G.pos[3]} (${pct(G.pos[3])})`)
console.log(`② 长度线索    正确项均 ${(G.cLen / G.nMC).toFixed(1)} 字 / 错误项均 ${(G.wLen / G.wN).toFixed(1)} 字 = ${ratio.toFixed(2)}×  (合格 ≤${LIMIT.lenRatio})`)
console.log(`              「正确=最长」${G.longest}/${G.nMC} = ${pct(G.longest)}  (合格 ≤${(LIMIT.longestShare * 100)}%)`)
console.log(`              「正确=最短」${G.shortest}/${G.nMC} = ${pct(G.shortest)}  (反向线索,同样要低)`)
console.log(`③ 判断题      对 ${G.jT} / 错 ${G.jF}`)
console.log(`④ 疑似一眼假  ${suspects.length} 条(下方列出,需人工复看)`)
console.log(`${'-'.repeat(58)}`)
console.log(`总闸 · 蒙题策略(四选一一律选 B + 判断题一律选「错」)`)
console.log(`      得 ${G.guess}/${G.guessMax} 分,随机基准 ${randomBase.toFixed(1)} 分 → ${G.guess <= randomBase * 1.15 ? '过' : '不过'}`)

if (suspects.length) {
  console.log(`\n④ 疑似一眼假干扰项(明显比同题其他选项短):`)
  suspects.slice(0, 30).forEach(s => console.log('   ' + s))
  if (suspects.length > 30) console.log(`   ...另有 ${suspects.length - 30} 条`)
}

console.log(`\n不合格文件 ${bad.length} 份:`)
if (!bad.length) console.log('   (无)')
bad.forEach(([f, msg]) => console.log(`   ${f.padEnd(18)} ${msg}`))
console.log('')
process.exit(bad.length || ratio > LIMIT.lenRatio || G.longest / G.nMC > LIMIT.longestShare ? 1 : 0)

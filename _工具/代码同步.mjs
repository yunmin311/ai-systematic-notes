/* 代码同步 · 页面里的代码块 和 code/labNN/*.py 必须一模一样
   用法:  node _工具\代码同步.mjs          只检查
          node _工具\代码同步.mjs --fix    以页面为准,把磁盘上的 .py 覆盖成页面里的版本

   为什么需要它:
      实验页里写着「代码同时放在 实验室\code\labNN\ 下,可以直接 python xxx.py」。
      这句话一旦不成立,照着「方式 B」走的人跑出来的输出就和页面上的「应该看到」对不上。
      而实验自检只验页面里的代码,查不出这种漂移。

   哪一边为准:页面。因为页面是学习者直接看到的东西,也同步过了口吻检查和输出比对。
*/
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const LAB = join(ROOT, '实验室')
const CODE = join(LAB, 'code')
const FIX = process.argv.includes('--fix')

const unesc = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
  .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
const norm = s => s.split(/\r?\n/).map(l => l.replace(/\s+$/, '')).join('\n').trim()

// 从页面里取出 { 文件名 -> 代码 }
function pageCode(html) {
  const names = [...html.matchAll(/<span class="fname"[^>]*>([^<]*)</g)].map(m => m[1].trim())
  const codes = [...html.matchAll(/<textarea[^>]*>([\s\S]*?)<\/textarea>/g)].map(m => unesc(m[1]))
  // 带「填入参考答案」按钮的是页面内练习题,答案故意不写出来,也不该要求磁盘有副本
  const exer = [...html.matchAll(/<div class="runner"[^>]*>([\s\S]*?)<pre class="runout"/g)]
    .map(m => /class="btn ghost sm fill"/.test(m[1]))
  const out = {}
  names.forEach((n, i) => { if (codes[i] !== undefined) out[n] = { code: codes[i], exercise: !!exer[i] } })
  return out
}

// 页面里的名字可能带后缀(如 step3_learn.py(最小版本)),磁盘上是干净的文件名
const baseName = n => n.replace(/[（(].*$/, '').trim()

let pairs = 0, drift = [], orphan = [], fixed = 0
const ambiguous = []

for (const dir of readdirSync(CODE)) {
  const m = dir.match(/^lab(\d+)$/)
  if (!m) continue
  const num = String(m[1]).padStart(2, '0')
  const page = readdirSync(LAB).find(f => f.startsWith(`lab-${num}-`) && f.endsWith('.html'))
  if (!page) { orphan.push(`code/${dir}/ 有代码目录,但没有 lab-${num} 页面`); continue }

  const inPage = pageCode(readFileSync(join(LAB, page), 'utf8'))
  // 建一份「去后缀」的索引。注意同一个基名可能对应多个块
  // (lab-01 就有 step3_learn.py 的「最小版本」和「补全中」两份),
  // 所以不能后写覆盖前写——要按优先级挑:完整版 > 带「最小版本」的 > 其他。
  const cands = {}
  for (const [n, v] of Object.entries(inPage)) {
    const b = baseName(n)
    if (b === n) continue                       // 名字本来就干净,走精确匹配
    if (v.exercise) continue                    // 练习题不进候选,磁盘不需要副本
    ;(cands[b] ||= []).push({ name: n, code: v.code })
  }
  const byBase = {}
  for (const [b, list] of Object.entries(cands)) {
    const best = list.find(x => /最小版本/.test(x.name)) || list[0]
    byBase[b] = best.code
    if (list.length > 1 && list.some(x => x.code !== best.code)) {
      ambiguous.push(`${page} 里 ${list.map(x => x.name).join(' / ')} 同名,已取「${best.name}」,请人工确认`)
    }
  }

  for (const f of readdirSync(join(CODE, dir))) {
    if (!f.endsWith('.py')) continue
    const diskPath = join(CODE, dir, f)
    if (!(f in inPage) && !(f in byBase)) {
      orphan.push(`${dir}/${f} 在 ${page} 里找不到对应的代码块`)
      continue
    }
    pairs++
    const src = inPage[f]?.code ?? byBase[f]
    const disk = readFileSync(diskPath, 'utf8')
    if (norm(disk) === norm(src)) continue
    drift.push(`${dir}/${f}  ≠  ${page}`)
    if (FIX) { writeFileSync(diskPath, src.endsWith('\n') ? src : src + '\n'); fixed++ }
  }
}

console.log(`\n代码同步 · 比对了 ${pairs} 组(页面代码块 ↔ code/ 下的 .py)`)
console.log('='.repeat(56))
if (drift.length) {
  console.log(`不一致 ${drift.length} 组:`)
  drift.forEach(x => console.log('  ' + x))
  if (FIX) console.log(`  已按「页面为准」覆盖 ${fixed} 个文件`)
} else {
  console.log('  全部一致')
}
if (orphan.length) {
  console.log(`\n对不上号的 ${orphan.length} 条(要人工看):`)
  orphan.forEach(x => console.log('  ' + x))
}
if (ambiguous.length) {
  console.log(`\n同名块 ${ambiguous.length} 条(已按规则挑,但要人工看一眼):`)
  ambiguous.forEach(x => console.log('  ' + x))
}

if (drift.length && !FIX) {
  console.log(`\n不合格:同一段代码在页面和磁盘上必须是同一份。`)
  console.log(`  跑 node _工具/代码同步.mjs --fix 可以按「页面为准」一键同步。`)
  process.exit(1)
}
console.log(`\n通过`)

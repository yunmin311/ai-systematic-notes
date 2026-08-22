/* 题目 ↔ 正文 对照筛查(2026-08-21)
   用法:  node _工具\题目对正文.mjs [题库编号正则]
   目的:  两个自检脚本验的全是形式(位置、长度、干扰项像不像真误解)。
          没有任何形式指标能证明题目考的知识点是对的。这个脚本做的是内容侧的第一道粗筛。

   它查两件机器能查的事:
     ① 超范围:题干/正确答案里出现的术语,在本章正文里一次都没出现
     ② 数字对不上:题干/答案里的数字,在本章正文里找不到
   命中不等于错,只是「需要人看一眼」。真正的判断只能人来做。
*/
import { readFileSync, readdirSync, statSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const QDIR = join(ROOT, '题库')

// 题库编号 → 讲义文件
const chapterFile = id => {
  const dir = /^\d\d$/.test(id) ? '基础课程' : /^D/.test(id) ? '深度课程' : /^A/.test(id) ? '应用工程' : null
  if (!dir) return null
  const d = join(ROOT, dir)
  const f = readdirSync(d).find(n => n.startsWith(id + '-') && n.endsWith('.html'))
  return f ? join(d, f) : null
}

const plain = s => s
  .replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, '')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&[a-z]+;/g, ' ')

// 抽「像术语的东西」:英文词/缩写、以及常见中文技术词
const TERM = /[A-Za-z][A-Za-z0-9_.+-]{2,}/g
const NUM = /(?<![A-Za-z0-9_.])\d+(?:\.\d+)?%?/g
// 这些到处都是,查了没意义
const STOP = new Set(['html', 'href', 'span', 'div', 'class', 'the', 'and', 'for', 'you', 'with',
  'true', 'false', 'null', 'none', 'print', 'import', 'from', 'return', 'this', 'that'])

const only = process.argv[2] ? new RegExp(process.argv[2]) : null
let nQ = 0, nFlag = 0
const rows = []

for (const f of readdirSync(QDIR).filter(n => /^quiz-.+\.html$/.test(n)).sort()) {
  const id = f.replace(/^quiz-|\.html$/g, '')
  if (only && !only.test(id)) continue
  const cf = chapterFile(id)
  if (!cf) { rows.push([id, '—', '找不到对应讲义(项目/实验类题库跳过)']); continue }
  const text = plain(readFileSync(cf, 'utf8')).toLowerCase()
  const src = readFileSync(join(QDIR, f), 'utf8')
  const m = src.match(/window\.QUESTIONS = ([\s\S]*?);\n<\/script>/)
  if (!m) continue
  const qs = Function('return ' + m[1])()

  qs.forEach((q, i) => {
    nQ++
    const parts = [q.q || '']
    if (q.options && typeof q.answer === 'number') parts.push(q.options[q.answer] || '')
    const blob = parts.join(' ')
    const terms = [...new Set((blob.match(TERM) || [])
      .map(t => t.toLowerCase()).filter(t => !STOP.has(t) && t.length > 2))]
    const missT = terms.filter(t => !text.includes(t))
    const nums = [...new Set((blob.match(NUM) || []))].filter(x => x.length > 1)
    const missN = nums.filter(x => !text.includes(x.toLowerCase()))
    if (missT.length || missN.length) {
      nFlag++
      rows.push([`${id}#${i}`, q.type,
        (missT.length ? '术语不在正文:' + missT.join('/') : '') +
        (missT.length && missN.length ? ' | ' : '') +
        (missN.length ? '数字不在正文:' + missN.join('/') : '')])
    }
  })
}

console.log(`\n题目对正文 · 粗筛 ${nQ} 道,标出 ${nFlag} 道待人看\n${'='.repeat(58)}`)
rows.forEach(r => console.log(`  ${String(r[0]).padEnd(9)} ${String(r[1]).padEnd(8)} ${r[2]}`))
console.log(`\n提醒:命中 ≠ 出错。这一步只缩小范围,判断必须人来做。`)

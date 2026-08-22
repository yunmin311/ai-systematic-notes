/* 全站体检:①缺纸材背景 ②内部死链 ③锚点失效 ④过时字样
   用法: node _工具\全站体检.mjs
   出新页面或改完链接之后跑一次。②③必须是 0。 */
import { readFileSync, readdirSync, statSync, existsSync } from 'fs'
import { join, dirname, resolve } from 'path'

import { fileURLToPath } from 'url'
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const files = []
;(function walk(d) {
  for (const n of readdirSync(d)) {
    if (n === '_备份' || n === '_工具' || n === '_样本预览' || n === 'node_modules') continue
    const p = join(d, n)
    if (statSync(p).isDirectory()) walk(p)
    else if (n.endsWith('.html') && !n.includes('.bak')) files.push(p)
  }
})(ROOT)

const noBg = [], broken = [], badAnchor = [], stale = []
const STALE = ['规划中', '制作中', '待建', '(即将', '敬请期待']

for (const f of files) {
  const raw = readFileSync(f, 'utf8')
  // 脚本里的字符串拼接不是真链接,先剔掉(2026-08-21)
  const s = raw.replace(/<script(?![^>]*\ssrc=)[^>]*>[\s\S]*?<\/script>/g, '')
  const rel = f.substring(ROOT.length + 1).replace(/\\/g, '/')

  // ① 背景:要么自足页内联了 paper-linen,要么引了 course.css(css 里有)
  const hasPaper = s.includes('paper-linen')
  const usesCourseCss = s.includes('assets/course.css')
  const usesQuizEngine = s.includes('quiz-engine.js')   // 题库页的底纹由引擎注入
  if (!hasPaper && !usesCourseCss && !usesQuizEngine) noBg.push(rel)

  // ② 内部链接
  const ids = new Set([...s.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]))
  for (const m of s.matchAll(/href="([^"#][^"]*?)(#[^"]*)?"/g)) {
    const href = m[1], anchor = m[2]
    if (/^(https?:|mailto:|data:)/.test(href)) continue
    const target = resolve(dirname(f), decodeURIComponent(href))
    if (!existsSync(target)) broken.push(`${rel}  →  ${href}`)
    else if (anchor && target === f) {
      if (!ids.has(anchor.slice(1))) badAnchor.push(`${rel}  →  ${anchor}`)
    }
  }
  // 同页锚点(href="#xxx")
  for (const m of s.matchAll(/href="#([^"]+)"/g)) {
    if (!ids.has(m[1])) badAnchor.push(`${rel}  →  #${m[1]}`)
  }

  // ④ 过时字样(只看正文可见区域的粗略匹配)
  for (const w of STALE) {
    const c = (s.split(w).length - 1)
    if (c) stale.push(`${rel}  「${w}」×${c}`)
  }
}

const p = (title, arr) => {
  console.log(`\n===== ${title}(${arr.length})=====`)
  arr.slice(0, 60).forEach(x => console.log('  ' + x))
  if (arr.length > 60) console.log(`  … 还有 ${arr.length - 60} 条`)
}
console.log(`扫描 ${files.length} 个页面`)
p('① 没有纸材背景', noBg)
p('② 内部死链', [...new Set(broken)])
p('③ 锚点失效', [...new Set(badAnchor)])
p('④ 过时字样(需人工判断)', stale)

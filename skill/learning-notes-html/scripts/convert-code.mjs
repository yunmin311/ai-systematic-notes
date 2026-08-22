import { readFileSync, writeFileSync, copyFileSync } from 'fs'
import { codeToHtml } from 'shiki'

const FILE = '<课程库根目录>/基础课程/02-Python基础.html'

// 变体 A:纯墨黑灰,关键词加粗,零彩色
const theme = {
  name: 'mono', type: 'light',
  colors: { 'editor.background': '#ffffff', 'editor.foreground': '#14181f' },
  settings: [
    { scope: ['comment', 'punctuation.definition.comment'], settings: { foreground: '#8b95a8', fontStyle: 'italic' } },
    { scope: ['string', 'string.quoted', 'punctuation.definition.string', 'string.template', 'constant.character'], settings: { foreground: '#557089' } },
    { scope: ['keyword', 'keyword.control', 'storage.type', 'storage.modifier', 'keyword.operator.logical', 'keyword.operator.new', 'variable.language'], settings: { foreground: '#14181f', fontStyle: 'bold' } },
    { scope: ['constant.numeric', 'constant.language'], settings: { foreground: '#14181f' } },
    { scope: ['entity.name.function', 'support.function', 'meta.function-call.generic'], settings: { foreground: '#14181f' } },
  ],
}

function decode(s) {
  return s.replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/&amp;/g, '&')
}

const html = readFileSync(FILE, 'utf8')
copyFileSync(FILE, FILE.replace('.html', '.pre-shiki.bak.html'))

const preRe = /<pre\b[^>]*>([\s\S]*?)<\/pre>/g
const parts = []
let m
while ((m = preRe.exec(html))) parts.push({ start: m.index, end: preRe.lastIndex, inner: m[1] })

let cursor = 0
const pieces = []
for (const p of parts) {
  pieces.push(html.slice(cursor, p.start))
  const raw = decode(p.inner)
  let rendered = await codeToHtml(raw, { lang: 'python', theme })
  // 让 shiki 的 pre 背景透明,交给外层 .code-block / details 的白底
  rendered = rendered.replace(/background-color:#ffffff/gi, 'background-color:transparent')
  pieces.push(rendered)
  cursor = p.end
}
pieces.push(html.slice(cursor))

writeFileSync(FILE, pieces.join(''))
console.log('converted', parts.length, 'code blocks via Shiki (variant A mono)')

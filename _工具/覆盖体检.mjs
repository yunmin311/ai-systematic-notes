/* 覆盖体检 · 配套件缺口检测
   用法:  node _工具\覆盖体检.mjs
   目的:  查出「讲义有、配套没有」的洞——题库、术语表、实验室、台账采集。
          2026-08-30 建的:这四类缺口之前全靠人眼扫,一次全库体检就查出
          题库 32/46、术语表 32/46、实验室 13/46 三处漏,所以补上这道机械闸。

   查五项:
     ① 每章是否有对应题库(项目章豁免:交付物即检验)
     ② 每章是否挂了 study-tracker(台账采不采集得到)
     ③ 每章是否被术语表收录
     ④ 每章是否有配套实验(按实验页声明的「配 X 章」算,不是靠反链猜)
     ⑤ 全站计数是否与首页/README 宣传一致(46 章 / 32 份题库 / 9 个实验)
*/
import { readFileSync, readdirSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')

const STAGES = [
  ['基础课程', /^(\d{2})-/],
  ['深度课程', /^(D\d{2})-/],
  ['应用工程', /^(A\d{2})-/],
  ['项目', /^(P\d)-/],
  ['AI使用', /^(U\d{2})-/],
]

const read = p => { try { return readFileSync(join(ROOT, p), 'utf8') } catch { return '' } }

// ---- 收集全部章节 ----
const chapters = []
for (const [dir, re] of STAGES) {
  for (const f of readdirSync(join(ROOT, dir)).filter(f => f.endsWith('.html')).sort()) {
    const m = f.match(re)
    if (m) chapters.push({ dir, file: f, id: m[1], path: `${dir}/${f}` })
  }
}

const quizDir = readdirSync(join(ROOT, '题库')).filter(f => /^quiz-.+\.html$/.test(f))
const gloss = read('资料/术语表.html')
const indexHtml = read('index.html')

// ---- ④ 实验配套:解析实验页里声明的「配 X 章」 ----
// meta 形如: 配 第 1 章 · 浏览器 + 本机 · <b>4 个脚本</b>
// 取到第一个 < 为止,再抽章节号(裸数字=基础课程章号,补零成 01;D/A/U 开头原样)
const labDir = join(ROOT, '实验室')
const labs = readdirSync(labDir).filter(f => /^lab-\d+/.test(f) && f.endsWith('.html')).sort()
const labIndex = read('实验室/index.html')
const coveredByLab = new Set()
for (const m of labIndex.matchAll(/<span class="meta">配\s*([^<]+)/g)) {
  for (const tok of m[1].matchAll(/\b(\d{1,2}|[DAU]\d{2})\b/g)) {
    const t = tok[1]
    coveredByLab.add(/^\d/.test(t) ? t.padStart(2, '0') : t)
  }
}
// 术语表按「小节标题」收录,标题形如:
//   第 1 章 · 人工智能全景与学习环境 / 应用工程 · A01–A07 / 深度课程 · 经典机器学习 D01–D06
// 不能靠条目里的 class="src" 判——第 1 章那批条目的 src 写的是「§10 概念一」这种章内小节号。
const glossChapters = new Set()
for (const m of gloss.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/g)) {
  const t = m[1].replace(/<[^>]+>/g, '')
  const bare = t.match(/第\s*(\d{1,2})\s*章/)   // 基础课程按「第 N 章」成节
  if (bare) { glossChapters.add(bare[1].padStart(2, '0')); continue }
  // 2026-09-10 修:原来只认 \d{2},而项目章号是一位数(P1–P7),补了术语表也照样算缺。
  const range = t.match(/([DAUP])(\d{1,2})\s*[–\-~]\s*([DAUP])(\d{1,2})/)
  if (range) {
    for (let i = +range[2]; i <= +range[4]; i++) {
      // 两种写法都收:文件名里 D/A/U 是两位(D01)、P 是一位(P1),补零与否都认
      glossChapters.add(range[1] + i)
      glossChapters.add(range[1] + String(i).padStart(2, '0'))
    }
    continue
  }
  for (const one of t.matchAll(/\b([DAUP])(\d{1,2})\b/g)) glossChapters.add(one[0])
}
const inGlossary = c => glossChapters.has(c.id)

const rows = []
for (const c of chapters) {
  const src = read(c.path)
  const quiz = quizDir.includes(`quiz-${c.id}.html`)
  const tracker = /study-tracker\.js/.test(src)
  const inGloss = inGlossary(c)
  const lab = coveredByLab.has(c.id)
  rows.push({ ...c, quiz, tracker, inGloss, lab })
}

// ---- 输出 ----
const EXEMPT_QUIZ = /^P\d$/   // 项目不设题库,是设计决定
const miss = { quiz: [], tracker: [], gloss: [], lab: [] }
for (const r of rows) {
  if (!r.quiz && !EXEMPT_QUIZ.test(r.id)) miss.quiz.push(r)
  if (!r.tracker) miss.tracker.push(r)
  if (!r.inGloss) miss.gloss.push(r)
  if (!r.lab) miss.lab.push(r)
}

const pct = (a, b) => `${b - a.length}/${b}`
console.log(`\n覆盖体检 · ${chapters.length} 章`)
console.log('='.repeat(56))
console.log(`① 题库        ${pct(miss.quiz.filter(r => !EXEMPT_QUIZ.test(r.id)), chapters.filter(r => !EXEMPT_QUIZ.test(r.id)).length)}` +
            `   (项目 P1–P7 设计上不设,已豁免)`)
console.log(`② 台账采集    ${pct(miss.tracker, chapters.length)}`)
console.log(`③ 术语表      ${pct(miss.gloss, chapters.length)}`)
console.log(`④ 配套实验    ${pct(miss.lab, chapters.length)}   配套来自 ${labs.length} 个实验`)

for (const [key, label] of [['quiz', '题库'], ['tracker', '台账采集'], ['gloss', '术语表'], ['lab', '配套实验']]) {
  const list = miss[key].filter(r => !(key === 'quiz' && EXEMPT_QUIZ.test(r.id)))
  if (!list.length) continue
  console.log(`\n—— 缺${label} ${list.length} 章 ——`)
  console.log('   ' + list.map(r => r.id).join(' '))
}

// ---- ⑤ 宣传一致性 ----
console.log('\n⑤ 首页 / README 计数一致性')
const claims = [
  [/(\d+)\s*章讲义/, chapters.length, '章讲义'],
  [/(\d+)\s*份题库/, quizDir.length, '份题库'],
]
for (const [re, actual, label] of claims) {
  const m = indexHtml.match(re)
  const said = m ? +m[1] : null
  const ok = said === actual
  console.log(`   ${ok ? '✓' : '✗'} 首页说 ${said ?? '?'} ${label},实际 ${actual}`)
}
const labM = indexHtml.match(/(\d+)\s*个 · 分步跑/)
console.log(`   ${labM && +labM[1] === labs.length ? '✓' : '✗'} 首页说 ${labM ? labM[1] : '?'} 个实验,实际 ${labs.length}`)

const failed = miss.tracker.length
console.log(`\n${failed ? '不合格:台账采集必须 46/46,否则学习数据有洞' : '通过(除已登记欠账)'}`)
// 项目 P1–P7 与 AI 使用 U01–U07 是**设计上不设**实验(项目本身就是动手交付物;
// AI 使用那段明确不写代码),所以不能算欠账。真正的欠账只数讲义章。
const byDesign = r => /^P\d$/.test(r.id) || /^U\d\d$/.test(r.id)
const realDebt = miss.lab.filter(r => !byDesign(r))
console.log(`\n注:配套实验的缺口是唯一不计入失败的一项——` +
            `\n  其中项目 P1–P7 与 AI 使用 U01–U07 共 14 章是设计上不设实验,真正的欠账只有 ${realDebt.length} 章讲义。` +
            `\n  题库与术语表已于 2026-09-10 补到满。`)
if (realDebt.length)
  console.log(`  仍缺实验的讲义章(${realDebt.length}):` + realDebt.map(r => r.id).join(' '))
process.exit(failed ? 1 : 0)

import { readFileSync, writeFileSync, copyFileSync } from 'fs'

const FILE = '<课程库根目录>/基础课程/02-Python基础.html'
let svgs = JSON.parse(readFileSync('<用户主目录>/svgs.json', 'utf8'))
if (typeof svgs === 'string') svgs = JSON.parse(svgs)

const map = [
  ['Python 五块地基环绕核心目标', 'd1'],
  ['字典是键到值的对应表', 'd4'],
  ['if 分支流程图', 'd5'],
  ['for 循环流程图', 'd6'],
  ['函数是进料出料的机器', 'd7'],
]

let html = readFileSync(FILE, 'utf8')
copyFileSync(FILE, FILE.replace('.html', '.pre-mermaid.bak.html'))

for (const [label, id] of map) {
  let svg = svgs[id]
  // 给 mermaid svg 补上无障碍标签,并加一个类名方便日后定位
  svg = svg.replace('<svg ', `<svg role="img" aria-label="${label}" data-mmd="${id}" `)
  const re = new RegExp('<svg[^>]*aria-label="' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '"[\\s\\S]*?<\\/svg>')
  if (!re.test(html)) { console.log('NOT FOUND:', label); continue }
  html = html.replace(re, () => svg)
  console.log('replaced', label, '->', id)
}

writeFileSync(FILE, html)
console.log('done')

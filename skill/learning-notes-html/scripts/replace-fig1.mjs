import { readFileSync, writeFileSync, copyFileSync } from 'fs'

const FILE = '<课程库根目录>/基础课程/02-Python基础.html'

const hub = `<svg viewBox="0 0 760 412" role="img" aria-label="Python 五块地基环绕核心目标" data-mmd="d1-hub">
<defs><marker id="m-hub" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8b95a8"/></marker></defs>
<line x1="380" y1="78" x2="380" y2="178" class="d-soft" marker-end="url(#m-hub)"/>
<line x1="600" y1="168" x2="476" y2="198" class="d-soft" marker-end="url(#m-hub)"/>
<line x1="510" y1="330" x2="452" y2="244" class="d-soft" marker-end="url(#m-hub)"/>
<line x1="250" y1="330" x2="308" y2="244" class="d-soft" marker-end="url(#m-hub)"/>
<line x1="160" y1="168" x2="284" y2="198" class="d-soft" marker-end="url(#m-hub)"/>
<rect x="288" y="182" width="184" height="66" rx="33" class="d-acc nf-acc" stroke-width="1.6"/>
<text x="380" y="210" text-anchor="middle" class="nl-acc">读懂并改写</text>
<text x="380" y="230" text-anchor="middle" class="nl-acc">数据代码</text>
<rect x="298" y="32" width="164" height="46" rx="8" class="d-ink nf"/>
<text x="380" y="60" text-anchor="middle" class="nl">① 变量与类型</text>
<rect x="588" y="122" width="164" height="46" rx="8" class="d-ink nf"/>
<text x="670" y="150" text-anchor="middle" class="nl">② 容器 list/dict</text>
<rect x="452" y="330" width="164" height="46" rx="8" class="d-ink nf"/>
<text x="534" y="358" text-anchor="middle" class="nl">③ 控制流 if/for</text>
<rect x="144" y="330" width="164" height="46" rx="8" class="d-ink nf"/>
<text x="226" y="358" text-anchor="middle" class="nl">④ 函数 def</text>
<rect x="8" y="122" width="150" height="46" rx="8" class="d-ink nf"/>
<text x="83" y="150" text-anchor="middle" class="nl">⑤ 读报错</text>
</svg>`

let html = readFileSync(FILE, 'utf8')
copyFileSync(FILE, FILE.replace('.html', '.pre-fig1.bak.html'))

const re = /<svg[^>]*data-mmd="d1"[\s\S]*?<\/svg>/
if (!re.test(html)) { console.log('d1 not found'); process.exit(1) }
html = html.replace(re, () => hub)
writeFileSync(FILE, html)
console.log('图1 replaced with radial hub')

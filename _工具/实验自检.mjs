/* 实验自检 · 「应该看到」必须是真跑出来的
   用法:  node _工具\实验自检.mjs [python路径]
   目的:  维护约定里写着「把每一步的『应该看到』真跑一遍抓回来,不要凭空写」——
          这条规矩只写在文档里等于没有。本脚本把每个实验页里的代码抽出来真跑一遍,
          和页面上写的「应该看到」逐字比对,对不上就点名。

   做法:  ① 从 lab-XX.html 里抽出每个 .runner 的代码(textarea)和它下面的 .expect
          ② 把代码写成临时 .py,用真 Python 跑
          ③ 输出与 expect 比对(去首尾空白、容忍行尾空格)

   注意:  含时间戳、随机数、网络请求的代码没法逐字比对,脚本会把它们标成
          「跳过了」并列出,供人工确认——跳过不等于通过。
*/
import { readFileSync, writeFileSync, readdirSync, mkdtempSync, rmSync } from 'fs'
import { execFileSync } from 'child_process'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'
import { tmpdir } from 'os'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const LAB = join(ROOT, '实验室')

// python:命令行可指定,其次环境变量,其次常见路径
const PY = process.argv[2] || process.env.LAB_PYTHON
  || 'C:/Users/lqy/.workbuddy/binaries/python/envs/default/Scripts/python.exe'

const unesc = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
                    .replace(/&quot;/g, '"').replace(/&#39;/g, "'")

// 拿到所有 runner 块:文件名 / 代码 / 期望输出
function parse(html) {
  const blocks = []
  // 注意两处:
  // ① 不能拿 </div> 当终点——.runner-bar 自己的 </div> 会提前截断;终点用 <pre class="runout"。
  // ② <div class="runner"> 后面可能被工具注入别的属性(见过 data-page-node-id),
  //    所以不能写死成 `<div class="runner">`,必须容忍多余属性,否则整个文件会被静默跳过。
  const re = /<div class="runner"[^>]*>([\s\S]*?)<pre class="runout"/g
  let m
  while ((m = re.exec(html))) {
    const chunk = m[1]
    const fn = (chunk.match(/class="fname"[^>]*>([^<]*)</) || [])[1] || '(未命名)'
    const code = (chunk.match(/<textarea[^>]*>([\s\S]*?)<\/textarea>/) || [])[1]
    if (!code) continue
    // 期望输出紧跟在这个 runner 之后,有两种历史写法:
    //   新(lab-02 起):<div class="expect"><b>应该看到</b>…</div>
    //   旧(lab-01)  :<pre class="out">…</pre>
    // 两种都认,否则 lab-01 会被误报成「没有应该看到」。
    const after = html.slice(re.lastIndex)
    // 每个标签后面都可能被工具塞进属性(data-page-node-id),所以一律用 [^>]* 兜住
    const em = after.match(/<div class="expect"[^>]*>\s*<b[^>]*>应该看到<\/b>([\s\S]*?)<\/div>/)
      || after.match(/<pre class="out"[^>]*>([\s\S]*?)<\/pre>/)
    blocks.push({ fn, code: unesc(code), expect: em ? unesc(em[1]).trim() : null,
                  isExercise: /class="btn ghost sm fill"/.test(chunk) })
  }
  return blocks
}

const files = readdirSync(LAB).filter(f => /^lab-\d+/.test(f) && f.endsWith('.html')).sort()
const tmp = mkdtempSync(join(tmpdir(), 'labcheck-'))
let nRun = 0, nOk = 0, nSkip = 0, nNoMod = 0, nNoExpect = 0
const bad = []
const noExpect = []

console.log(`\n实验自检 · ${files.length} 个实验`)
console.log('='.repeat(56))

for (const f of files) {
  const html = readFileSync(join(LAB, f), 'utf8')
  const blocks = parse(html)
  // 静默跳过是危险的:lab-12 就因为 div 上多了一个注入属性而整份没被检查,总数还看不出少了谁。
  if (!blocks.length) {
    if (/class="runner"/.test(html)) {
      console.log(`  ${f.padEnd(34)} ✗ 有 runner 但一段都没解析出来 —— 检查标签写法`)
      bad.push([f, '(整页)', '解析出 0 段', '页面里有 class="runner" 却不匹配正则'])
    }
    continue
  }
  const res = []
  for (const b of blocks) {
    // 练习题:带「填入参考答案」按钮的,答案是故意藏起来的,不算缺失
    if (b.isExercise) {
      nSkip++; res.push(`${b.fn} 练习题 → 跳过`); continue
    }
    // 没有「应该看到」= 学习者在页面里看不到对照,违反实验页的基本格式,要单列出来
    if (!b.expect) { nNoExpect++; noExpect.push(`${f}  ${b.fn}`); res.push(`${b.fn} ✗ 无「应该看到」`); continue }
    // 时间戳 / 随机 / 网络:没法逐字比对,标记跳过由人看
    // 版本/平台/时间/网络:输出随机器而变,没法逐字比对。
    // 随机要单独判断:写了 seed 的就是确定性的,必须照常比对,不能放水跳过。
    const timeDep = /(%H:%M|time\(\)|datetime\.now|sys\.version|platform\.)/.test(b.code)
    const netDep = /(requests\.|openai|urllib)/.test(b.code)
    const randNoSeed = /(random\.|np\.random)/.test(b.code) && !/seed\(/.test(b.code)
    if (timeDep || netDep || randNoSeed) {
      nSkip++; res.push(`${b.fn} 含时间/随机/网络 → 跳过`); continue
    }
    const py = join(tmp, b.fn.replace(/[^\w.]/g, '_'))
    writeFileSync(py, b.code)
    let out
    try {
      out = execFileSync(PY, [py], { encoding: 'utf8', timeout: 120000,
        env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONUTF8: '1' } })
    } catch (e) {
      const err = (e.stderr || e.stdout || e.message || '')
      // 缺第三方包 ≠ 写错了:本机没装而已(lab-06 要 torch,Pyodide 里也没有)。
      // 这类单独列出来,不算不合格,但要让人看见「这段代码没能被验证过」。
      const mm = err.match(/No module named '([^']+)'/)
      if (mm) { nNoMod++; res.push(`${b.fn} 缺包 ${mm[1]} → 未验证`) }
      else {
        nRun++; bad.push([f, b.fn, '运行报错', err.split('\n').slice(-3).join(' | ')])
        res.push(`${b.fn} ✗ 运行报错`)
      }
      continue
    }
    nRun++
    const norm = s => s.split('\n').map(l => l.replace(/\s+$/, '')).join('\n').trim()
    if (norm(out) === norm(b.expect)) { nOk++; res.push(`${b.fn} ✓`) }
    else {
      bad.push([f, b.fn, '输出与「应该看到」不一致', ''])
      res.push(`${b.fn} ✗ 输出不一致`)
    }
  }
  console.log(`  ${f.padEnd(34)} ${res.join('   ')}`)
}

rmSync(tmp, { recursive: true, force: true })

console.log(`\n跑了 ${nRun} 段,一致 ${nOk},跳过 ${nSkip}(需人工确认),缺包未验证 ${nNoMod}`)
if (noExpect.length) {
  console.log(`\n缺「应该看到」${nNoExpect} 段 —— 实验页每段代码都要给出对照输出:`)
  noExpect.forEach(x => console.log('  ' + x))
}
if (bad.length) {
  console.log(`\n不一致 ${bad.length} 段:`)
  for (const [f, fn, why, extra] of bad) {
    console.log(`  ${f}  ${fn}\n     ${why}${extra ? '  ' + extra : ''}`)
  }
}
if (bad.length || noExpect.length) {
  console.log(`\n不合格:「应该看到」必须等于真跑出来的输出,不许凭空写;每段代码都得有。`)
  process.exit(1)
}
console.log(`\n通过(跳过的那几段要人工看一眼——跳过不等于通过)`)

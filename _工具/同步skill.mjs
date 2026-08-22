/* 把写这套笔记用的 skill 同步进本仓(2026-08-22)
   用法: node _工具\同步skill.mjs

   为什么需要这个脚本:
   skill 的正本在 Claude Code 的用户级技能目录 `~/.claude/skills/`——它必须待在那里才会被加载,
   所以不能直接搬进仓库。但它是这套笔记的「怎么写出来的」那一半,不进仓就等于没备份、也没法开源。

   于是:**正本仍在 ~/.claude/skills,仓库里放一份单向同步的副本**。
   只许从正本 → 仓库,不许反向;改 skill 请改正本,然后跑一次本脚本。

   同步时会顺手做两件事:
     ① 把脚本里写死的本机绝对路径换成占位符(否则开源出去就带着我的用户名)
     ② 在副本目录里放一个 README,写清正本在哪、别直接改副本
*/
import { readFileSync, writeFileSync, readdirSync, statSync, mkdirSync, rmSync, existsSync } from 'fs'
import { fileURLToPath } from 'url'
import { dirname, join, relative } from 'path'
import { homedir } from 'os'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const SRC = join(homedir(), '.claude', 'skills')
const DST = join(ROOT, 'skill')
const WANTED = ['learning-notes-html', 'course-authoring']

// 本机痕迹 → 占位符
const SCRUB = [
  [/[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9_.-]+[\\/]Desktop[\\/]人工智能-系统学习/g, '<课程库根目录>'],
  [/[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9_.-]+/g, '<用户主目录>'],
  [/桌面\\人工智能-系统学习/g, '<课程库根目录>'],
]
const TEXT = ['.md', '.mjs', '.js', '.json', '.html', '.txt', '.css']

let files = 0, scrubbed = 0
for (const name of WANTED) {
  const from = join(SRC, name)
  if (!existsSync(from)) { console.log(`★ 正本里没有 ${name},跳过`); continue }
  const to = join(DST, name)
  if (existsSync(to)) rmSync(to, { recursive: true, force: true })
  ;(function copy(a, b) {
    mkdirSync(b, { recursive: true })
    for (const n of readdirSync(a)) {
      const pa = join(a, n), pb = join(b, n)
      if (statSync(pa).isDirectory()) { copy(pa, pb); continue }
      if (TEXT.some(e => n.endsWith(e))) {
        let s = readFileSync(pa, 'utf8')
        const before = s
        for (const [re, rep] of SCRUB) s = s.replace(re, rep)
        if (s !== before) scrubbed++
        writeFileSync(pb, s)
      } else {
        writeFileSync(pb, readFileSync(pa))
      }
      files++
    }
  })(from, to)
  console.log(`✔ ${name}`)
}

writeFileSync(join(DST, 'README.md'), `# skill —— 这套笔记是怎么写出来的

这两个 skill 是写这套课程库时实际用的写作与出题标准。放在这里有两个目的:
**一是备份**(否则它只存在一台机器的用户目录里),**二是开源**——想用同一套方法写自己的笔记,可以直接拿去改。

| 目录 | 管什么 |
|---|---|
| \`learning-notes-html/\` | 单文件离线 HTML 笔记怎么写:外链策展法、设计系统(字号/颜色/组件/纸材)、代码走 Shiki、图走 Mermaid 或自制、以及交付前的自检 |
| \`course-authoring/\` | 讲义与题目的内容标准:零连续比喻、术语首现要给白话、九种题型、干扰项必须是真实误解 |

## 怎么用

这是 [Claude Code](https://docs.claude.com/en/docs/claude-code) 的 skill 格式。
把目录拷到 \`~/.claude/skills/\` 下即可被自动发现;换别的工具就当成一份写作规范来读。

## 注意:这里是副本

**正本在 \`~/.claude/skills/\` ——那里才是被加载的那一份。**
本目录由 \`_工具/同步skill.mjs\` 从正本单向同步而来,同步时会把脚本里写死的本机路径换成占位符。
要改 skill 请改正本,然后重跑一次同步;**直接改这里的副本会在下次同步时被覆盖**。
`)
console.log(`\n同步完成:${files} 个文件 → skill/(其中 ${scrubbed} 个文件里的本机路径已换成占位符)`)

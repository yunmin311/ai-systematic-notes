---
name: learning-notes-html
description: >
  写「为自己裁剪的学习笔记」并出成自足单文件、离线可看的 HTML——用外链策展法组织内容(领读+索引+外链+收口),
  用单一强调色的极简设计系统排版(6 级字号、一条左边线、说明块共用骨架、图带外框),代码走 Shiki、图走 Mermaid/自制。
  只要用户要写或改「学习笔记 / 课程章节笔记 / 讲义 / knowledge base 页面」——尤其是 AI 系统学习课程的后续章节(如 03 NumPy、04 Pandas 等)、
  把参考资料消化成带图的教学页面、或提到「笔记基准线 / 按 02-Python 那套做 / 外链策展」——就用这个 skill,别自己临时发明排版或手搓代码高亮和 SVG。
  黄金范本:<课程库根目录>\基础课程\02-Python基础.html。
---

# 学习笔记写作(基准线 + 外链策展 + 生产流水线)

把三样合成一套可复用的做法:**怎么写**(外链策展法)、**长什么样**(设计系统)、**怎么产出**(Shiki/Mermaid 流水线)。
目标产物:一篇自足单文件、离线双击即看的教学 HTML。黄金范本是 `02-Python基础.html`——拿不准长相时对照它。

这套是十几轮实战打磨出来的,每条规矩背后都有踩过的坑。别绕开、别即兴重造;要偏离先说清为什么。

## reference,按需读

- `references/writing-method.md` —— **写什么**。每篇固定六段、外链策展三件套、书体声音。**动笔前先读。**
- `references/design-system.md` —— **长什么样**。6 级字号、一条左边线、框只有 3 类、图的分工。**排版/改样式前读。**
- `references/production-pipeline.md` —— **怎么产出**。Shiki 高亮 + Mermaid/自制图 + 两个血泪坑。**出代码块和图前读。**
- `references/index-page.md` —— **整册总入口(MOC/落地页)的结构**。开新库、或每做完一章回填总索引时读。
- `references/theming.md` —— **定制窗口**:配色/UI/动效怎么随需要换而不动结构。要改皮或加 motion 时读。

`assets/template.html` = 能跑的成品骨架(全部 CSS + 页面结构 + 通用 JS),新章节从它起。
`scripts/` = Shiki/Mermaid 预渲染脚本(`convert-code.mjs` / `render-diagrams.html` / `inject-diagrams.mjs` / `replace-fig1.mjs`)。

## 写一篇新章节的流程

**1. 先内容,后排版。** 按 `writing-method.md` 把这一篇的六段写出来:定位(卸包袱、明确不学什么)→ 心智地图(亲手画,外链替代不了)→ 外链策展(2–5 条精挑,每条带三件套,**真核实链接**)→ 收口(自己的话 + 常见误区表)→ 练习题 → 实例(能跑 + 改改看)。声音用书体,不用「你」。
> **出题环节走 `course-authoring`**——它是出题标准的正本(题型、干扰项=真实误解、答案打散、解析拆穿干扰项)。本 skill **不另写一套出题标准**,只负责把答案放折叠区(`<details>`)。两个 skill 触发词有重叠(如「讲义」):**笔记结构/设计/产出**归本 skill,**纯出题**让 course-authoring 主导。

**2. 从模板起。** 复制 `assets/template.html`,填面包屑、章首 recap、骨架清单;正文按小节铺开。每个概念节的固定节奏:
```
<p class="handoff">过渡句(朴素灰、不加粗)</p>
<h2 id="xxx"><span class="no">N</span><span>小节标题</span></h2>
<p class="one-liner">术语<span class="en">en</span>:一句话定义。</p>
<p>散文讲解,加粗领句省着用……</p>
<figure>…一张图…</figure>
<div class="code-block">…<pre>普通文本代码</pre></div>
<div class="callout go"><span class="label">去精读</span><p>外链三件套……</p></div>
```
概念节之间用 `.handoff` 过渡句串成一条线(承上启下,别让小节变孤岛)。右侧 `.toc-sidebar` 每个 `a` 的 `data-toc-target` 要等于对应 h2 的 `id`。

**3. 代码交给 Shiki。** 先在 HTML 里把代码按普通 `<pre>` 写好(缩进正确、注释对齐),再跑 `scripts/convert-code.mjs` 一次性高亮成纯墨黑灰。别手写高亮 span。

**4. 图按本质选载体**(见 pipeline):流程/关系→Mermaid 预渲染;辐射/概念→自制 SVG(复用工具类);报错→`.trace` 面板;索引格子→`.idxgrid` 表。**Mermaid 必须 `htmlLabels:false`、渲染字体用本机的**,否则截字。

**5. 自检**(浏览器里过一遍,别静态猜):
- 正文字号 = 7 种、字体 = 2 种、无 Arial。
- 正文/定义/说明块/过渡句左边缘对齐到一条线。
- 每张图有外框、不截字、不撞线、无黑块;整页彩色只有群青蓝一种(+代码的墨灰)。
- 无外部资源加载(script src / link css / CDN / img 计数为 0),离线双击可看。
- 六段齐、外链三件套齐、链接真的可达、心智地图在场、答案能折叠。

**6. 交付给本人给绝对路径**(用户常打不开在线链接,只认本地文件)。更新总索引(MOC),标好和前后篇的顺序。

## 会踩的坑(前人已替你踩过)

- **别用颜色分级**——想加颜色前先试线/字号/小标签。整页只留一个强调色。
- **别在正文写 `style="font-size"`**、别用 `em` 给行内代码——会滚出一堆怪字号。
- **别让左边缘参差**——说明块用悬挂竖线把文字拉回 x=0,去底色、去 `↓→` 符号、列表去小圆点。
- **别手搓代码高亮和 SVG**——一致性差、格式爆炸;交给 Shiki 和 Mermaid。
- **别把辐射图硬塞给 Mermaid**(会挤成扇形)、**别用深色黑块**。
- **加粗要省**,过渡句不加粗、不用中文斜体(合成假斜发丑)。

# 生产流水线 · 代码走 Shiki,图走 Mermaid/自制

**铁律:代码和图都不许手搓。** 手写 `<span>` 高亮、手画 SVG 是「不一致、格式过多」的病根。
上成熟工具,**构建期预渲染成离线静态文件,零运行时**——成品仍是自足单文件、双击即看。

脚本都在本 skill 的 `scripts/`。一次性装依赖(需本机 Node 18+):
```
cd <skill>/scripts && npm install shiki mermaid
```
渲染时开个本地静态服务器看效果(`file://` 常被浏览器拦):`python -m http.server 8799`,浏览器开 `http://127.0.0.1:<port>/…`。**每轮都截图亲眼看,别静态猜。**

---

## 一、代码 = Shiki(纯墨黑灰,变体 A)

VS Code 同款引擎。用自定义**零彩色主题**:注释 `#8b95a8` 斜体、字符串 `#557089`、关键词加粗墨色、其余墨色。强调蓝只留给正文链接/警示,代码里不上蓝/绿。

`scripts/convert-code.mjs` 做的事:读一篇 HTML 里所有 `<pre>`,取原始代码(剥标签、解实体),用 Shiki 主题渲染成**自带内联样式**的 HTML,写回。壳 `.code-block`(文件名 + 语言 + 复制按钮)和复制 JS 都照用。

用法:改脚本顶部 `FILE` 指向目标 HTML,然后 `node convert-code.mjs`。它会先备份成 `*.pre-shiki.bak.html`。
先在 HTML 里把代码按普通 `<pre>…</pre>` 写好(纯文本、正确缩进、注释对齐),再跑脚本一次性全部高亮。

## 二、图 = Mermaid + 自制 + 表/面板 混合

按图的本质选载体:

**流程/关系图(判断、循环、输入→处理→输出)→ Mermaid 预渲染静态 SVG。**
1. 在 `skills/learning-notes-html/scripts/render-diagrams.html` 里写图定义(每张一个 `<pre class="mermaid" id="dN">`)。装到本机后即 `~/.claude/skills/learning-notes-html/scripts/`。
2. 起服务器,浏览器打开该页,渲染后取每个 `#dN svg` 的 `outerHTML`,拼成 JSON 存盘。
3. `node inject-diagrams.mjs` 按 `aria-label` 把 HTML 里对应的旧 SVG 换成新的。

**辐射/环绕图(中心目标 + N 块环绕)、概念示意图(贴标签盒子这类隐喻)→ 自制 SVG。**
Mermaid 只会画层级树,硬做辐射会挤成扇形。自制时复用模板里的 `.d-ink/.d-soft/.nf/.nf-acc/.nl/.nl-acc/.el` 工具类,视觉和 Mermaid 一致。`scripts/replace-fig1.mjs` 是一个辐射式「五块环绕核心」的范例(直接改坐标和文字即可复用)。

**报错 traceback → `.trace` 文本面板**(不画图);**列表索引格子 → `.idxgrid` 表格**(不画图)。

### 两个必踩的坑(务必照做)

1. **Mermaid 必须 `htmlLabels:false`**。默认 `htmlLabels:true` 用 `foreignObject` 装 HTML 文字,内联进页面后会**继承页面 CSS(字号/行距/字距)**,把文字撑宽、超出节点被截断。改用原生 SVG `<text>` 后免疫页面 CSS,`<br/>` 多行照常。`render-diagrams.html` 里已设好。
2. **渲染时字体用本机装了的**(如 `Microsoft YaHei`),和页面实际回退字体一致;否则渲染器按别的字体量节点宽度、显示时又换字体 → 框比字窄 → 截字。
3. 单色皮肤:节点白底墨线、连线灰、边标签白底光晕、强调只点**一个**群青蓝节点;**不要深色黑块**——重点用浅底 `#f4f6fb` + 蓝框。

## 三、自检(渲染完在浏览器里过一遍)

- 正文字号 = 7 种(11/13/15/16/18/22/30);字体 = 2 种(Noto Sans SC + JetBrains Mono),无 Arial。
- 正文/定义/说明块/过渡句左边缘在同一条线(测 `getBoundingClientRect().left` 应一致)。
- 每张图有外框、文字不截、不撞线、没有黑块。
- 无外部资源加载:`<script src>`、`<link rel=stylesheet>`、CDN、`<img>` 计数应为 0(内联 SVG 除外)。离线双击可看。
- 交付给用户永远给**本地文件的绝对路径**(用户可能打不开在线链接)。

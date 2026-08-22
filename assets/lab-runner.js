/* 实验室 · 页面内 Python 运行器(Pyodide,真实 Python,首次需联网)
   2026-08-21 抽成共享文件,并补上「按 import 自动装包」——
   lab-01 那版没有装包,遇到 numpy/pandas/sklearn 会报 ModuleNotFoundError。

   页面里只要有 .runner 结构就会被接管:
     <div class="runner">
       <div class="runner-bar"><span class="fname">x.py</span>
         <button class="btn sm run">▶ 运行</button>
         <button class="btn ghost sm reset">重置</button></div>
       <textarea class="code" rows="10">…</textarea>
       <pre class="runout">…</pre>
     </div>
   torch 不在 Pyodide 里,需要 PyTorch 的实验只提供本地 .py 方式。
*/
(function () {
  'use strict';
  var VER = 'v0.26.2';
  var BASE = 'https://cdn.jsdelivr.net/pyodide/' + VER + '/full/';
  var ready = null;

  function boot() {
    if (ready) return ready;
    ready = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = BASE + 'pyodide.js';
      s.onload = function () {
        window.loadPyodide({ indexURL: BASE }).then(resolve, reject);
      };
      s.onerror = function () {
        reject(new Error('无法加载 Pyodide(需要联网)。改用本地终端方式运行同名 .py 文件。'));
      };
      document.head.appendChild(s);
    });
    return ready;
  }

  document.querySelectorAll('.runner').forEach(function (runner) {
    var ta = runner.querySelector('textarea.code');
    var out = runner.querySelector('.runout');
    var runBtn = runner.querySelector('.run');
    var resetBtn = runner.querySelector('.reset');
    if (!ta || !out || !runBtn) return;
    var initial = ta.value;

    if (resetBtn) resetBtn.addEventListener('click', function () {
      ta.value = initial;
      out.classList.remove('err');
      out.textContent = '已重置';
    });

    runBtn.addEventListener('click', function () {
      out.classList.remove('err');
      out.textContent = '⏳ 正在加载浏览器内 Python(首次约 10–20 秒)…';
      boot().then(function (py) {
        out.textContent = '📦 正在按 import 装包…';
        return py.loadPackagesFromImports(ta.value).catch(function () { /* 没有要装的就算了 */ })
          .then(function () { return py; });
      }).then(function (py) {
        out.textContent = '▶ 运行中…';
        var lines = [];
        py.setStdout({ batched: function (s) { lines.push(s); } });
        py.setStderr({ batched: function (s) { lines.push(s); } });
        try {
          var ns = py.globals.get('dict')();
          py.runPython(ta.value, { globals: ns });
          ns.destroy();
          out.textContent = lines.length ? lines.join('\n')
            : '(程序运行完毕,没有任何输出——是不是忘了 print?)';
        } catch (e) {
          out.classList.add('err');
          out.textContent = (lines.length ? lines.join('\n') + '\n\n' : '') + String(e.message || e);
        }
      }).catch(function (e) {
        out.classList.add('err');
        out.textContent = String(e.message || e);
      });
    });
  });
})();

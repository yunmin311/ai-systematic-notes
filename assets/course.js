/* 公共交互:阅读进度条 / 代码复制按钮 / 自查清单记忆 / 返回顶部
   所有课程页在 </body> 前引入:<script src="../assets/course.js"></script> */
(function () {
  'use strict';

  /* ---------- 顶部阅读进度条 ---------- */
  var bar = document.createElement('div');
  bar.id = 'readbar';
  document.body.appendChild(bar);
  function updateBar() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  }
  window.addEventListener('scroll', updateBar, { passive: true });
  updateBar();

  /* ---------- 代码块复制按钮(预期输出块除外) ---------- */
  document.querySelectorAll('pre:not(.out)').forEach(function (pre) {
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.type = 'button';
    btn.textContent = '复制';
    btn.addEventListener('click', function () {
      var text = pre.innerText.replace(/^复制\n?/, '');
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = '已复制 ✓';
        setTimeout(function () { btn.textContent = '复制'; }, 1600);
      }, function () {
        btn.textContent = '复制失败';
      });
    });
    pre.appendChild(btn);
  });

  /* ---------- 自查清单:勾选状态存 localStorage ---------- */
  var pageKey = 'aicourse:' + location.pathname.split(/[\\/]/).pop();
  document.querySelectorAll('.checklist').forEach(function (list, li0) {
    list.querySelectorAll('li').forEach(function (li, i) {
      var box = li.querySelector('input[type="checkbox"]');
      if (!box) return;
      var key = pageKey + ':chk' + li0 + '-' + i;
      if (localStorage.getItem(key) === '1') { box.checked = true; li.classList.add('done'); }
      li.addEventListener('click', function (e) {
        if (e.target !== box) { box.checked = !box.checked; }
        li.classList.toggle('done', box.checked);
        localStorage.setItem(key, box.checked ? '1' : '0');
      });
    });
  });

  /* ---------- 返回顶部 ---------- */
  var top = document.createElement('button');
  top.id = 'totop';
  top.type = 'button';
  top.title = '回到顶部';
  top.textContent = '↑';
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  document.body.appendChild(top);
  window.addEventListener('scroll', function () {
    top.classList.toggle('show', document.documentElement.scrollTop > 900);
  }, { passive: true });
})();

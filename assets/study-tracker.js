/* 学习台账 · 采集端(2026-08-21)
   每个讲义/实验页在末尾引一行:
     <script src="../assets/study-tracker.js" data-ch="D14" data-kind="chapter" data-title="注意力机制逐步手算"></script>
   它做的事只有一件:把「这一章被打开过几次」记进 localStorage。
   第 2 次及以后打开 = 一次回查。回查次数是掌握度最诚实的指标。

   不改正文、不改样式、不发网络请求。存储不可用时(某些浏览器禁用 file:// 的 localStorage)
   静默跳过,不影响页面。
*/
(function () {
  'use strict';
  var KEY = 'aicourse.v1';

  function load() {
    try {
      var raw = window.localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return null; }          // 存储不可用
  }
  function save(db) {
    try { window.localStorage.setItem(KEY, JSON.stringify(db)); return true; }
    catch (e) { return false; }
  }
  function today() {
    var d = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; };
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  }

  var me = document.currentScript;
  if (!me) return;
  var id = me.getAttribute('data-ch');
  if (!id) return;
  var kind = me.getAttribute('data-kind') || 'chapter';
  var title = me.getAttribute('data-title') || document.title;

  var db = load();
  if (!db) return;                        // 存储不可用,安静退出
  if (!db.chapters) db.chapters = {};

  var rec = db.chapters[id] || { visits: 0, first: today(), last: today(), kind: kind, title: title };
  rec.visits += 1;
  rec.last = today();
  rec.kind = kind;
  rec.title = title;
  db.chapters[id] = rec;
  db.updated = today();
  save(db);

  // 供台账页与页面自身取用
  window.__studyRecord = rec;
})();

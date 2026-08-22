/* 共享题库引擎(冷靛蓝图主题)
   每个 quiz-XX.html 只需定义:
     window.QUIZ_TITLE  — 标题
     window.QUIZ_SUB    — 副标题
     window.QUESTIONS   — 题目数组
   题目字段:
     type    judge|choice|code|predict|debug|shape → 选项题(options + answer + explain)
             short|scene|param                    → 自评题(model,看参考答案后自评)
     section 可选,小节分隔标题
     q       题干; code 可选,附代码块
   然后引入本文件即可,页面其余部分自动生成。 */
(function () {
  'use strict';

  var CSS = '\
  :root{--bg:#eef1f6;--card:#f6f8fc;--ink:#14181f;--muted:#55617a;--line:#d8dee9;\
    --acc:#2743c7;--acc-dark:#1d33a0;--acc-soft:#e8ecfb;--teal:#0c6e63;--teal-soft:#e3f0ee;\
    --warn:#9a3412;--warn-soft:#fdeee4;--danger:#b42318;--code:#111826;}\
  *{box-sizing:border-box}\
  body{margin:0;color:var(--ink);line-height:1.7;font-size:16px;\
    background-color:#e6eaf1;background-image:url("../assets/paper-linen-v3.jpg");\
    background-repeat:repeat;background-size:230px 230px;\
    font-family:"Noto Sans SC","Microsoft YaHei",-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}\
  .scorebar{background:rgba(230,234,241,.94)!important}\
  .wrap{max-width:780px;margin:0 auto;padding:36px 20px 100px}\
  .back{color:var(--acc-dark);text-decoration:none;font-size:13px}\
  .back:hover{text-decoration:underline}\
  h1{font-size:25px;margin:14px 0 4px}\
  .sub{color:var(--muted);font-size:15px;margin:0 0 8px}\
  .scorebar{position:sticky;top:0;background:rgba(238,241,246,.94);backdrop-filter:blur(6px);\
    padding:12px 0;margin:14px 0 6px;border-bottom:1px solid var(--line);font-size:15px;z-index:5}\
  .scorebar b{color:var(--acc-dark)}\
  .section{margin:32px 0 4px;font-size:16px;color:var(--teal);font-weight:700;\
    padding-bottom:6px;border-bottom:2px solid var(--line)}\
  .q{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:18px 20px;margin:16px 0;\
    box-shadow:none}\
  .qhead{display:flex;justify-content:space-between;align-items:center;gap:8px}\
  .q .num{font-size:12px;color:var(--muted);font-weight:600;letter-spacing:.5px}\
  .badge{font-size:11px;font-weight:600;padding:1px 0;border-radius:0;font-family:"JetBrains Mono","Cascadia Code",Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;color:var(--muted);background:none!important}\
  .b-judge,.b-choice,.b-code,.b-predict,.b-debug,.b-shape,.b-short,.b-scene,.b-param{color:var(--muted)}\
  \
  \
  \
  \
  .q .qt{font-size:16px;font-weight:600;margin:8px 0 12px;white-space:pre-line}\
  pre{background:#f4f6fb;color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:13px 15px;overflow-x:auto;\
    margin:0 0 12px;font-size:13px;line-height:1.6;font-family:"JetBrains Mono","Cascadia Code",Consolas,monospace;white-space:pre}\
  .opt{display:block;width:100%;text-align:left;background:var(--bg);border:1px solid var(--line);\
    border-radius:4px;padding:11px 14px;margin:8px 0;font-size:15px;cursor:pointer;\
    font-family:inherit;color:inherit;transition:.12s;line-height:1.55}\
  .opt:hover:not(:disabled){border-color:var(--acc);background:#fff}\
  .opt:disabled{cursor:default}\
  .opt.right{border-color:var(--teal);background:var(--teal-soft)}\
  .opt.wrong{border-color:var(--danger);background:#fbebe9}\
  .opt .mk{float:right;font-weight:700;margin-left:8px}\
  .opt.right .mk{color:var(--teal)}.opt.wrong .mk{color:var(--danger)}\
  .reveal{background:var(--acc);color:#fff;border:none;border-radius:4px;padding:9px 18px;\
    font-size:15px;cursor:pointer;font-family:inherit}\
  .reveal:hover{background:var(--acc-dark)}\
  .explain{display:none;background:var(--acc-soft);border-left:3px solid var(--acc);\
    border-radius:0;padding:10px 14px;margin-top:12px;font-size:15px;white-space:pre-line}\
  .explain.show{display:block}\
  .selfrow{display:none;gap:10px;margin-top:12px}\
  .selfrow.show{display:flex}\
  .self{flex:1;border:1px solid var(--line);border-radius:4px;padding:9px;font-size:15px;\
    cursor:pointer;font-family:inherit;background:var(--bg)}\
  .self.y{border-color:var(--teal);color:var(--teal)}.self.n{border-color:var(--danger);color:var(--danger)}\
  .self:disabled{opacity:.55;cursor:default}\
  .done{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:22px;\
    margin-top:24px;text-align:center;display:none}\
  .done.show{display:block}\
  .done b{font-size:22.5px;color:var(--acc-dark)}\
  .retry{margin-top:12px;background:var(--acc);color:#fff;border:none;border-radius:4px;\
    padding:10px 22px;font-size:15px;cursor:pointer;font-family:inherit}';

  var style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  var QUESTIONS = window.QUESTIONS || [];
  var wrap = document.createElement('div'); wrap.className = 'wrap'; document.body.appendChild(wrap);
  var back = document.createElement('a'); back.className = 'back'; back.href = 'quiz.html';
  back.textContent = '← 题库入口'; wrap.appendChild(back);
  var h1 = document.createElement('h1'); h1.textContent = window.QUIZ_TITLE || '自测题库'; wrap.appendChild(h1);
  var sub = document.createElement('p'); sub.className = 'sub'; sub.textContent = window.QUIZ_SUB || ''; wrap.appendChild(sub);
  var bar = document.createElement('div'); bar.className = 'scorebar';
  bar.innerHTML = '已答 <b id="answered">0</b> / <span id="total"></span> · 答对/自评掌握 <b id="correct">0</b>';
  wrap.appendChild(bar);
  var quiz = document.createElement('div'); wrap.appendChild(quiz);
  var done = document.createElement('div'); done.className = 'done';
  done.innerHTML = '<b id="finalmsg"></b><p id="finalsub" style="color:var(--muted);font-size:13px"></p>' +
    '<button class="retry" type="button">再考一遍 ↻</button>';
  wrap.appendChild(done);
  var back2 = document.createElement('a'); back2.className = 'back'; back2.href = 'quiz.html';
  back2.textContent = '← 题库入口'; wrap.appendChild(back2);
  done.querySelector('.retry').onclick = function () { location.reload(); };

  var answered = 0, correct = 0;
  var total = QUESTIONS.length;
  document.getElementById('total').textContent = total;

  var badgeMap = {
    judge:   ['概念判断', 'b-judge'],
    choice:  ['选择', 'b-choice'],
    code:    ['代码阅读', 'b-code'],
    predict: ['输出预测', 'b-predict'],
    debug:   ['找错', 'b-debug'],
    shape:   ['形状推导', 'b-shape'],
    short:   ['简答', 'b-short'],
    scene:   ['场景分析', 'b-scene'],
    param:   ['参数实验', 'b-param']
  };
  var SELF_TYPES = { short: 1, scene: 1, param: 1 };

  var wrongIdx = [];
  function bump(ok, qi) {
    answered++;
    if (ok) correct++;
    else if (typeof qi === 'number') wrongIdx.push(qi);
    document.getElementById('answered').textContent = answered;
    document.getElementById('correct').textContent = correct;
    if (answered === total) showDone();
  }

  QUESTIONS.forEach(function (item, qi) {
    if (item.section) {
      var h = document.createElement('div'); h.className = 'section';
      h.textContent = item.section; quiz.appendChild(h);
    }
    var card = document.createElement('div'); card.className = 'q';
    var head = document.createElement('div'); head.className = 'qhead';
    var num = document.createElement('span'); num.className = 'num';
    num.textContent = '第 ' + (qi + 1) + ' 题';
    var bm = badgeMap[item.type] || badgeMap.choice;
    var bd = document.createElement('span'); bd.className = 'badge ' + bm[1]; bd.textContent = bm[0];
    head.appendChild(num); head.appendChild(bd); card.appendChild(head);
    var qt = document.createElement('div'); qt.className = 'qt'; qt.textContent = item.q; card.appendChild(qt);
    if (item.code) { var pre = document.createElement('pre'); pre.textContent = item.code; card.appendChild(pre); }

    if (SELF_TYPES[item.type]) {
      /* 自评题:看参考答案 → 自评 会/不会 */
      var btn = document.createElement('button'); btn.className = 'reveal'; btn.type = 'button';
      btn.textContent = '看参考答案';
      var exp = document.createElement('div'); exp.className = 'explain';
      var lab = document.createElement('b'); lab.textContent = '参考答案:'; exp.appendChild(lab);
      exp.appendChild(document.createTextNode('\n' + item.model));
      var self = document.createElement('div'); self.className = 'selfrow';
      var yes = document.createElement('button'); yes.className = 'self y'; yes.type = 'button';
      yes.textContent = '我答出来了 ✓';
      var no = document.createElement('button'); no.className = 'self n'; no.type = 'button';
      no.textContent = '还不熟 ✗';
      var counted = false;
      function report(ok) {
        if (counted) return; counted = true;
        yes.disabled = no.disabled = true;
        bump(ok, qi);
      }
      yes.onclick = function () { report(true); };
      no.onclick = function () { report(false); };
      btn.onclick = function () {
        exp.classList.add('show'); self.classList.add('show'); btn.style.display = 'none';
      };
      self.appendChild(yes); self.appendChild(no);
      card.appendChild(btn); card.appendChild(exp); card.appendChild(self);
    } else {
      /* 选项题 */
      var exp2 = document.createElement('div'); exp2.className = 'explain';
      var lab2 = document.createElement('b'); lab2.textContent = '解析:'; exp2.appendChild(lab2);
      exp2.appendChild(document.createTextNode('\n' + item.explain));
      item.options.forEach(function (opt, oi) {
        var b = document.createElement('button'); b.className = 'opt'; b.type = 'button'; b.textContent = opt;
        b.onclick = function () {
          Array.prototype.forEach.call(card.querySelectorAll('.opt'), function (x) { x.disabled = true; });
          var ok = (oi === item.answer);
          if (ok) {
            b.classList.add('right');
            var m = document.createElement('span'); m.className = 'mk'; m.textContent = '✓ 对'; b.appendChild(m);
          } else {
            b.classList.add('wrong');
            var m1 = document.createElement('span'); m1.className = 'mk'; m1.textContent = '✗'; b.appendChild(m1);
            var right = card.querySelectorAll('.opt')[item.answer];
            right.classList.add('right');
            var m2 = document.createElement('span'); m2.className = 'mk'; m2.textContent = '✓ 正确答案'; right.appendChild(m2);
          }
          exp2.classList.add('show');
          bump(ok, qi);
        };
        card.appendChild(b);
      });
      card.appendChild(exp2);
    }
    quiz.appendChild(card);
  });

  function showDone() {
    var pct = Math.round(correct / total * 100);
    var msg = pct === 100 ? '满分。这一章算是吃透了 🎉'
      : pct >= 70 ? '大部分掌握了;错题解析值得回头看一遍 👍'
      : '低于七成:错题对应的小节需要回讲义重读 📖';
    document.getElementById('finalmsg').textContent = correct + ' / ' + total + '(' + pct + '%)';
    document.getElementById('finalsub').textContent = msg;
    done.classList.add('show');
    done.scrollIntoView({ behavior: 'smooth' });
    saveResult(pct);
  }

  /* —— 学习台账:把成绩与错题号记下来 —— */
  function saveResult(pct) {
    var KEY = 'aicourse.v1';
    var id = (location.pathname.match(/quiz-([A-Za-z0-9]+)\.html/) || [, null])[1];
    if (!id) return;
    var db;
    try { db = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return; }
    if (!db.quizzes) db.quizzes = {};
    var d = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; };
    var day = d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
    var rec = db.quizzes[id] || { attempts: 0, best: 0, total: total, first: day };
    rec.attempts += 1;
    rec.total = total;
    rec.last = day;
    rec.lastScore = correct;
    rec.lastPct = pct;
    if (correct > rec.best) rec.best = correct;
    rec.wrong = wrongIdx.slice();           // 最近一次的错题号
    db.quizzes[id] = rec;
    db.updated = day;
    try { localStorage.setItem(KEY, JSON.stringify(db)); } catch (e) {}
  }
})();

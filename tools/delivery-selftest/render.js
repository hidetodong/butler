'use strict';

// 交付自测桥 · 渲染层（纯函数，无 IO）
// render(manifest) -> 单文件自包含 HTML 字符串（GitHub 风格分步流程页）
// 结构保真 docs/research/MILE-0002-R2-manual-test-bridge-sample.html

// 四态：机器码（ASCII，供 R4 稳健路由）+ 中文展示 + 图标
const VERDICTS = [
  { code: 'pass',  label: '通过',     ic: '✓' },
  { code: 'fail',  label: '未通过',   ic: '✕' },
  { code: 'defer', label: '延后处理', ic: '⏳' },
  { code: 'skip',  label: '跳过',     ic: '⊘' },
];

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// 安全内联 JSON 进 <script>：转义 </ 与 U+2028/2029
function safeJson(obj) {
  return JSON.stringify(obj)
    .replace(/</g, '\\u003c')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}

// 规整 manifest.items 为客户端消费形状
function normalizeItems(manifest) {
  const items = Array.isArray(manifest.items) ? manifest.items : [];
  return items.map((it, i) => ({
    id: String(it.id != null ? it.id : 'item-' + (i + 1)),
    title: String(it.title != null ? it.title : ''),
    steps: Array.isArray(it.steps) ? it.steps.map(String) : [],
    expect: String(it.expected != null ? it.expected : (it.expect != null ? it.expect : '')),
  }));
}

function render(manifest) {
  manifest = manifest || {};
  const items = normalizeItems(manifest);
  const project = escapeHtml(manifest.project || '—');
  const iteration = escapeHtml(manifest.iteration || '');
  const phase = escapeHtml(manifest.phase || 'P5 验证 · 人测道残余');
  const total = items.length;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>交付自测 · butler delivery-selftest</title>
<style>
  :root{
    --fg:#1f2328; --muted:#59636e; --canvas:#ffffff; --subtle:#f6f8fa;
    --border:#d1d9e0; --border-muted:#d8dee4;
    --accent:#0969da; --accent-soft:#ddf4ff;
    --green:#1a7f37; --green-soft:#dafbe1; --green-bd:#2da44e;
    --red:#cf222e; --red-soft:#ffebe9; --red-bd:#f19d99;
    --yellow:#9a6700; --yellow-soft:#fff8c5; --yellow-bd:#eed888;
    --gray:#59636e; --gray-soft:#eef1f5;
    --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box;}
  body{margin:0; padding:2rem 1rem 5rem; background:var(--subtle); color:var(--fg);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    font-size:14px; line-height:1.6;}
  .wrap{max-width:840px; margin:0 auto;}
  header.repo-head{background:var(--canvas); border:1px solid var(--border); border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem;}
  header.repo-head h1{margin:0 0 .5rem; font-size:1.35rem; display:flex; align-items:center; gap:.5rem;}
  header.repo-head h1 .oct{color:var(--muted);}
  .meta{display:flex; flex-wrap:wrap; gap:.4rem; margin-top:.3rem;}
  .chip{display:inline-flex; align-items:center; gap:.3rem; padding:.1rem .55rem; border-radius:999px; font-size:.78rem;
    font-family:var(--mono); background:var(--gray-soft); color:var(--muted); border:1px solid var(--border-muted);}
  .chip.acc{background:var(--accent-soft); color:var(--accent); border-color:transparent;}
  .statusbar{position:sticky; top:0; z-index:5; background:var(--canvas); border:1px solid var(--border); border-radius:10px;
    padding:.6rem .9rem; margin-bottom:1rem; display:flex; align-items:center; gap:.5rem; flex-wrap:wrap; box-shadow:0 1px 3px rgba(31,35,40,.08);}
  .statusbar .track{flex:1; min-width:140px; height:8px; border-radius:999px; background:var(--gray-soft); overflow:hidden; display:flex;}
  .statusbar .track > i{display:block; height:100%;}
  .count{display:inline-flex; align-items:center; gap:.3rem; font-size:.8rem; font-family:var(--mono);}
  .dot{width:.6rem; height:.6rem; border-radius:50%; display:inline-block;}
  .dot.g{background:var(--green-bd);} .dot.r{background:var(--red);} .dot.y{background:var(--yellow-bd);} .dot.k{background:var(--gray);} .dot.p{background:var(--border);}
  .item{background:var(--canvas); border:1px solid var(--border); border-radius:12px; margin-bottom:1rem; overflow:hidden;}
  .item.decided{border-left-width:4px;}
  .item[data-state="pass"]{border-left-color:var(--green-bd);}
  .item[data-state="fail"]{border-left-color:var(--red);}
  .item[data-state="skip"]{border-left-color:var(--gray);}
  .item[data-state="defer"]{border-left-color:var(--yellow-bd);}
  .item-head{display:flex; align-items:flex-start; gap:.6rem; padding:.9rem 1.1rem; border-bottom:1px solid var(--border);}
  .item-head .idx{font-family:var(--mono); font-size:.75rem; color:var(--muted); background:var(--gray-soft); padding:.1rem .45rem; border-radius:6px; white-space:nowrap; margin-top:.15rem;}
  .item-head h2{margin:0; font-size:1rem; flex:1;}
  .verdict-tag{font-size:.72rem; font-family:var(--mono); padding:.12rem .5rem; border-radius:999px; white-space:nowrap;}
  .verdict-tag.none{background:var(--gray-soft); color:var(--muted);}
  .verdict-tag.pass{background:var(--green-soft); color:var(--green);}
  .verdict-tag.fail{background:var(--red-soft); color:var(--red);}
  .verdict-tag.skip{background:var(--gray-soft); color:var(--gray);}
  .verdict-tag.defer{background:var(--yellow-soft); color:var(--yellow);}
  .item-body{padding:.4rem 1.1rem 1rem;}
  .label{font-size:.75rem; font-weight:650; color:var(--muted); text-transform:uppercase; letter-spacing:.03em; margin:.9rem 0 .35rem;}
  ol.steps{margin:.2rem 0; padding:0; list-style:none; counter-reset:s;}
  ol.steps li{counter-increment:s; position:relative; padding:.35rem 0 .35rem 2rem; border-bottom:1px dashed var(--border-muted);}
  ol.steps li:last-child{border-bottom:none;}
  ol.steps li::before{content:counter(s); position:absolute; left:0; top:.35rem; width:1.35rem; height:1.35rem; border-radius:50%;
    background:var(--accent-soft); color:var(--accent); font-family:var(--mono); font-size:.72rem; font-weight:700; display:flex; align-items:center; justify-content:center;}
  .expect{background:var(--subtle); border:1px solid var(--border); border-left:3px solid var(--accent); border-radius:6px; padding:.5rem .75rem; font-size:.9rem;}
  textarea.note{width:100%; min-height:2.4rem; resize:vertical; border:1px solid var(--border); border-radius:6px; padding:.5rem .65rem; font:inherit; font-size:.9rem; background:var(--canvas); color:var(--fg);}
  textarea.note:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-soft);}
  .verdicts{display:flex; gap:.5rem; flex-wrap:wrap; margin-top:1rem;}
  .verdicts button{flex:1; min-width:88px; cursor:pointer; font:inherit; font-size:.85rem; font-weight:600; padding:.5rem .4rem; border-radius:8px;
    border:1px solid var(--border); background:var(--canvas); color:var(--fg); display:inline-flex; align-items:center; justify-content:center; gap:.35rem; transition:all .12s;}
  .verdicts button:hover{background:var(--subtle);}
  .verdicts button[data-v="pass"].on{background:var(--green-soft); border-color:var(--green-bd); color:var(--green);}
  .verdicts button[data-v="fail"].on{background:var(--red-soft); border-color:var(--red-bd); color:var(--red);}
  .verdicts button[data-v="skip"].on{background:var(--gray-soft); border-color:var(--gray); color:var(--gray);}
  .verdicts button[data-v="defer"].on{background:var(--yellow-soft); border-color:var(--yellow-bd); color:var(--yellow);}
  .submitbar{position:fixed; left:0; right:0; bottom:0; background:var(--canvas); border-top:1px solid var(--border); padding:.7rem 1rem;
    display:flex; align-items:center; gap:.8rem; justify-content:center; box-shadow:0 -1px 6px rgba(31,35,40,.06);}
  .submitbar .info{font-size:.82rem; color:var(--muted);}
  .btn-primary{cursor:pointer; font:inherit; font-size:.9rem; font-weight:650; color:#fff; background:var(--green-bd); border:1px solid rgba(31,35,40,.15); border-radius:8px; padding:.5rem 1.1rem;}
  .btn-primary:disabled{background:#94d3a2; cursor:not-allowed;}
  .done-panel{display:none; background:var(--canvas); border:1px solid var(--green-bd); border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem;}
  .done-panel.show{display:block;}
  .done-panel h2{margin:0 0 .4rem; color:var(--green); font-size:1.1rem;}
  pre.json{background:#0d1117; color:#e6edf3; border-radius:8px; padding:1rem; overflow:auto; font-family:var(--mono); font-size:.8rem; line-height:1.5;}
  .foot{text-align:center; color:var(--muted); font-size:.78rem; margin-top:1.5rem;}
</style>
</head>
<body>
<div class="wrap">
  <header class="repo-head">
    <h1><span class="oct">🔧</span> 交付自测 <span style="color:var(--muted);font-weight:400;font-size:1rem;">· delivery-selftest</span></h1>
    <div class="meta">
      <span class="chip acc">${project}</span>
      <span class="chip">${iteration}</span>
      <span class="chip">${phase}</span>
      <span class="chip" id="total-chip">${total} 项待测</span>
    </div>
  </header>

  <div class="done-panel" id="donePanel">
    <h2>✓ 已提交，可关闭页面</h2>
    <p style="margin:.2rem 0 .8rem; color:var(--muted);">结果已写回 <code>results.json</code>，桥进程将自退，butler 按四态路由续跑。</p>
    <pre class="json" id="jsonOut"></pre>
  </div>

  <div class="statusbar">
    <span class="count"><span class="dot g"></span><b id="c-pass">0</b> 通过</span>
    <span class="count"><span class="dot r"></span><b id="c-fail">0</b> 未通过</span>
    <span class="count"><span class="dot y"></span><b id="c-defer">0</b> 延后</span>
    <span class="count"><span class="dot k"></span><b id="c-skip">0</b> 跳过</span>
    <span class="count"><span class="dot p"></span><b id="c-todo">${total}</b> 待定</span>
    <span class="track" id="track"></span>
  </div>

  <div id="list"></div>
</div>

<div class="submitbar">
  <span class="info" id="subInfo">还有 <b>${total}</b> 项待定</span>
  <button class="btn-primary" id="submitBtn" disabled>提交结果并退出</button>
</div>

<script>
"use strict";
var ITEMS = ${safeJson(items)};
var VERDICTS = ${safeJson(VERDICTS)};
var META = ${safeJson({ project: manifest.project || null, iteration: manifest.iteration || null, phase: manifest.phase || 'P5' })};
var state = {}; // id -> {state, note}

var list = document.getElementById('list');
ITEMS.forEach(function(it){
  state[it.id] = { state: null, note: "" };
  var el = document.createElement('section');
  el.className = 'item';
  el.dataset.id = it.id;

  var head = document.createElement('div'); head.className = 'item-head';
  var idx = document.createElement('span'); idx.className = 'idx'; idx.textContent = it.id;
  var h2 = document.createElement('h2'); h2.textContent = it.title;
  var tag = document.createElement('span'); tag.className = 'verdict-tag none'; tag.textContent = '待定';
  head.appendChild(idx); head.appendChild(h2); head.appendChild(tag);

  var body = document.createElement('div'); body.className = 'item-body';
  var lbSteps = document.createElement('div'); lbSteps.className = 'label'; lbSteps.textContent = '测试步骤';
  var ol = document.createElement('ol'); ol.className = 'steps';
  it.steps.forEach(function(s){ var li = document.createElement('li'); li.textContent = s; ol.appendChild(li); });
  var lbExp = document.createElement('div'); lbExp.className = 'label'; lbExp.textContent = '预期结果';
  var exp = document.createElement('div'); exp.className = 'expect'; exp.textContent = it.expect;
  var lbNote = document.createElement('div'); lbNote.className = 'label'; lbNote.textContent = '备注 / 反馈（未通过时请填线索）';
  var note = document.createElement('textarea'); note.className = 'note'; note.placeholder = '可选……未通过时写下现象/复现，供 butler 纠错';
  note.addEventListener('input', function(e){ state[it.id].note = e.target.value; });

  var vs = document.createElement('div'); vs.className = 'verdicts';
  VERDICTS.forEach(function(x){
    var b = document.createElement('button'); b.dataset.v = x.code;
    var ic = document.createElement('span'); ic.className = 'ic'; ic.textContent = x.ic;
    b.appendChild(ic); b.appendChild(document.createTextNode(x.label));
    b.addEventListener('click', function(){
      state[it.id].state = x.code;
      Array.prototype.forEach.call(vs.querySelectorAll('button'), function(bb){ bb.classList.toggle('on', bb === b); });
      el.dataset.state = x.code; el.classList.add('decided');
      tag.className = 'verdict-tag ' + x.code; tag.textContent = x.label;
      refresh();
    });
    vs.appendChild(b);
  });

  body.appendChild(lbSteps); body.appendChild(ol); body.appendChild(lbExp); body.appendChild(exp);
  body.appendChild(lbNote); body.appendChild(note); body.appendChild(vs);
  el.appendChild(head); el.appendChild(body);
  list.appendChild(el);
});

function count(k){ return Object.keys(state).filter(function(id){ return state[id].state === k; }).length; }
function refresh(){
  var n = ITEMS.length;
  var pass = count('pass'), fail = count('fail'), defer = count('defer'), skip = count('skip');
  var todo = n - pass - fail - defer - skip;
  document.getElementById('c-pass').textContent = pass;
  document.getElementById('c-fail').textContent = fail;
  document.getElementById('c-defer').textContent = defer;
  document.getElementById('c-skip').textContent = skip;
  document.getElementById('c-todo').textContent = todo;
  function seg(w, c){ return w ? '<i style="width:' + (w / n * 100) + '%;background:' + c + '"></i>' : ''; }
  document.getElementById('track').innerHTML =
    seg(pass, 'var(--green-bd)') + seg(fail, 'var(--red)') + seg(defer, 'var(--yellow-bd)') + seg(skip, 'var(--gray)');
  document.getElementById('subInfo').innerHTML = todo > 0 ? '还有 <b>' + todo + '</b> 项待定' : '全部已判定，可提交';
  document.getElementById('submitBtn').disabled = todo > 0;
}

document.getElementById('submitBtn').addEventListener('click', function(){
  var btn = this; btn.disabled = true;
  var payload = {
    project: META.project, iteration: META.iteration, phase: META.phase,
    results: ITEMS.map(function(it){ return { id: it.id, state: state[it.id].state, note: state[it.id].note || null }; })
  };
  fetch('/submit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    .then(function(r){ return r.json(); })
    .then(function(res){
      document.getElementById('jsonOut').textContent = JSON.stringify(payload, null, 2);
      document.getElementById('donePanel').classList.add('show');
      document.querySelector('.submitbar').style.display = 'none';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    })
    .catch(function(err){ btn.disabled = false; alert('提交失败：' + err); });
});

refresh();
</script>
<div class="wrap"><p class="foot">交付自测 · GitHub 风格 · butler delivery-selftest（MILE-0002）</p></div>
</body>
</html>`;
}

module.exports = { render, VERDICTS, escapeHtml, normalizeItems, safeJson };

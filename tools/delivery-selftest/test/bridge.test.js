'use strict';

// 交付自测桥 · 端到端自测（Node 内建，零三方依赖）
// 覆盖：render 纯函数 / GET 首页 / GET health / POST 提交写 results / summary 计数 /
//       非法 state 归 null / 真进程提交后自退 exit(0)。
// 运行：node test/bridge.test.js  （全过 exit 0，任一失败 exit 1）

const assert = require('assert');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const { render } = require('../render');
const { createBridge, summarize, STATES } = require('../bridge');

const MANIFEST = {
  project: 'demo',
  iteration: 'ITER-TEST',
  phase: 'P5',
  items: [
    { id: 'A1', title: '标题一 <脚本注入>', steps: ['步骤一', '步骤二'], expected: '预期一' },
    { id: 'A2', title: '标题二', steps: ['只有一步'], expected: '预期二' },
  ],
};

let passed = 0;
function ok(name) { passed++; process.stdout.write('  ✓ ' + name + '\n'); }

function request(opts, body) {
  return new Promise((resolve, reject) => {
    const req = http.request(opts, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    });
    req.on('error', reject);
    if (body != null) req.write(body);
    req.end();
  });
}

function listen(server) {
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

async function testRenderPure() {
  const html = render(MANIFEST);
  assert.ok(html.startsWith('<!DOCTYPE html>'), 'render 应产出完整 HTML');
  // 结构保真（AC2）：静态脚手架 + CSS 选择器（分步卡/四态/备注的运行时 DOM 由 Playwright AC8 覆盖）
  ['statusbar', 'ol.steps', '.verdicts button', 'textarea.note', 'id="submitBtn"', 'id="donePanel"', 'id="list"'].forEach((m) =>
    assert.ok(html.indexOf(m) >= 0, 'HTML 应含结构标记 ' + m));
  // 客户端构建逻辑在场（运行时会生成 steps/verdicts/note 节点）
  ["className = 'steps'", "className = 'verdicts'", "createElement('textarea')"].forEach((m) =>
    assert.ok(html.indexOf(m) >= 0, 'HTML 应含客户端构建逻辑 ' + m));
  // 四态码嵌入
  STATES.forEach((s) => assert.ok(html.indexOf('"' + s + '"') >= 0, 'HTML 应含四态码 ' + s));
  // 数据内联且 < 被转义（AC 安全渲染 / DD6）
  assert.ok(html.indexOf('标题一') >= 0, 'HTML 应含 item 标题（内联数据）');
  assert.ok(html.indexOf('\\u003cscript') >= 0 || html.indexOf('\\u003c脚本') >= 0, '内联 JSON 的 < 应转义为 \\u003c');
  assert.ok(html.indexOf('<脚本注入>') < 0, '原始 < 不应裸出现在内联数据中');
  ok('render 纯函数：完整 HTML + 结构保真 + 四态码 + 安全内联');
}

function testSummarize() {
  const s = summarize([
    { state: 'pass' }, { state: 'pass' }, { state: 'fail' }, { state: 'skip' }, { state: 'defer' }, { state: null },
  ]);
  assert.deepStrictEqual(s, { pass: 2, fail: 1, skip: 1, defer: 1 }, 'summary 四态计数应正确、忽略 null');
  ok('summarize：四态计数正确、忽略非法');
}

async function testServeAndSubmit() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dst-'));
  const outPath = path.join(tmp, 'results.json');
  const { server } = createBridge(MANIFEST, { out: outPath, exitOnSubmit: false });
  const port = await listen(server);
  const base = { host: '127.0.0.1', port };

  // GET / (AC1)
  const home = await request({ ...base, method: 'GET', path: '/' });
  assert.strictEqual(home.status, 200, 'GET / 应 200');
  assert.ok(home.body.indexOf('标题一') >= 0, 'GET / 应含 item 标题');
  ok('GET /：200 + 渲染含条目');

  // GET /health
  const health = await request({ ...base, method: 'GET', path: '/health' });
  assert.strictEqual(health.status, 200, 'GET /health 应 200');
  ok('GET /health：200 就绪探针');

  // 404
  const nf = await request({ ...base, method: 'GET', path: '/nope' });
  assert.strictEqual(nf.status, 404, '未知路径应 404');
  ok('未知路径：404');

  // POST /submit (AC3)
  const payload = JSON.stringify({
    project: 'demo', iteration: 'ITER-TEST',
    results: [
      { id: 'A1', state: 'pass', note: null },
      { id: 'A2', state: 'defer', note: '晚点再看' },
      { id: 'A3', state: '乱码', note: null }, // 非法 state → null
    ],
  });
  const sub = await request({ ...base, method: 'POST', path: '/submit', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) } }, payload);
  assert.strictEqual(sub.status, 200, 'POST /submit 应 200');
  const subBody = JSON.parse(sub.body);
  assert.strictEqual(subBody.ok, true, '提交响应 ok:true');

  // results.json 落盘 + 内容 (AC3)
  assert.ok(fs.existsSync(outPath), 'results.json 应落盘');
  const results = JSON.parse(fs.readFileSync(outPath, 'utf8'));
  assert.strictEqual(results.results.length, 3, '应回填 3 条');
  assert.strictEqual(results.results[0].state, 'pass');
  assert.strictEqual(results.results[1].note, '晚点再看');
  assert.strictEqual(results.results[2].state, null, '非法 state 应归 null');
  assert.deepStrictEqual(results.summary, { pass: 1, fail: 0, skip: 0, defer: 1 }, 'summary 应正确');
  assert.ok(typeof results.submittedAt === 'string' && results.submittedAt.length > 0, '应有 submittedAt');
  ok('POST /submit：写 results.json + summary + 非法 state 归 null');

  await new Promise((r) => server.close(r));
  fs.rmSync(tmp, { recursive: true, force: true });
}

// AC4：真进程提交后自退 exit(0)
function testSelfExit() {
  return new Promise((resolve, reject) => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dst-exit-'));
    const manifestPath = path.join(tmp, 'manifest.json');
    const outPath = path.join(tmp, 'results.json');
    fs.writeFileSync(manifestPath, JSON.stringify(MANIFEST));
    const child = spawn(process.execPath, [path.join(__dirname, '..', 'bridge.js'), manifestPath, '--no-open', '--port', '0', '--out', outPath]);
    let out = '';
    const timer = setTimeout(() => { child.kill(); reject(new Error('自退超时：进程未在提交后退出')); }, 8000);
    child.stdout.on('data', (d) => {
      out += d;
      const m = out.match(/serving (http:\/\/127\.0\.0\.1:(\d+)\/)/);
      if (m && !child._posted) {
        child._posted = true;
        const port = parseInt(m[2], 10);
        const payload = JSON.stringify({ results: [{ id: 'A1', state: 'pass' }, { id: 'A2', state: 'skip' }] });
        const req = http.request({ host: '127.0.0.1', port, method: 'POST', path: '/submit', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) } }, (res) => { res.resume(); });
        req.on('error', () => {}); // 进程可能已退，忽略
        req.write(payload); req.end();
      }
    });
    child.on('exit', (code) => {
      clearTimeout(timer);
      try {
        assert.strictEqual(code, 0, '提交后应 exit(0)，实际 ' + code);
        assert.ok(fs.existsSync(outPath), '真进程应写出 results.json');
        fs.rmSync(tmp, { recursive: true, force: true });
        ok('真进程：提交后自退 exit(0) + results.json 落盘');
        resolve();
      } catch (e) { reject(e); }
    });
  });
}

async function testExampleRenders() {
  const example = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'example', 'manifest.json'), 'utf8'));
  const html = render(example);
  assert.ok(html.indexOf('登录页在 iPhone SE') >= 0, 'example manifest 应能渲染');
  ok('example/manifest.json：符合契约、渲染无异常');
}

(async () => {
  process.stdout.write('delivery-selftest 自测：\n');
  await testRenderPure();
  testSummarize();
  await testServeAndSubmit();
  await testSelfExit();
  await testExampleRenders();
  process.stdout.write('\nALL PASS (' + passed + ' checks)\n');
  process.exit(0);
})().catch((e) => {
  process.stderr.write('\nFAIL: ' + (e && e.stack ? e.stack : e) + '\n');
  process.exit(1);
});

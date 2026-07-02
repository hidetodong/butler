'use strict';

// 交付自测桥 · 服务层（零三方依赖）
// 用法：node bridge.js <manifest.json> [--out results.json] [--port N] [--no-open]
//   读 manifest → 起本地 HTTP 服务 → 渲染分步流程页 → 开浏览器
//   人对每项选四态（pass/fail/skip/defer）+ 备注 → 提交 → 写 results.json → 进程自退
// 契约与四态路由语义见同目录 README.md。

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const { render, VERDICTS } = require('./render');

const STATES = VERDICTS.map((v) => v.code); // ['pass','fail','skip','defer']

function parseArgs(argv) {
  const opts = { manifest: null, out: null, port: 0, noOpen: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') opts.out = argv[++i];
    else if (a === '--port') opts.port = parseInt(argv[++i], 10) || 0;
    else if (a === '--no-open') opts.noOpen = true;
    else if (a === '-h' || a === '--help') opts.help = true;
    else if (!a.startsWith('--')) opts.manifest = a;
  }
  return opts;
}

function summarize(results) {
  const s = { pass: 0, fail: 0, defer: 0, skip: 0 }; // 顺序对齐 UI 四态
  for (const r of results) if (Object.prototype.hasOwnProperty.call(s, r.state)) s[r.state]++;
  return s;
}

function openBrowser(url) {
  const p = process.platform;
  let cmd, args;
  if (p === 'darwin') { cmd = 'open'; args = [url]; }
  else if (p === 'win32') { cmd = 'cmd'; args = ['/c', 'start', '', url]; }
  else { cmd = 'xdg-open'; args = [url]; }
  execFile(cmd, args, () => {}); // best-effort，失败不影响服务
}

// 起桥服务。返回 { server, outPath, html }。
// opts.exitOnSubmit=false 时提交后不退进程（供测试进程内驱动），改回调 onSubmitted(out)。
function createBridge(manifest, opts = {}) {
  const html = render(manifest);
  const outPath = opts.out || path.join(process.cwd(), 'results.json');
  const exitOnSubmit = opts.exitOnSubmit !== false;
  const onSubmitted = typeof opts.onSubmitted === 'function' ? opts.onSubmitted : null;

  const server = http.createServer((req, res) => {
    const url = (req.url || '').split('?')[0];
    if (req.method === 'GET' && url === '/') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
      return;
    }
    if (req.method === 'GET' && url === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('{"ok":true}');
      return;
    }
    if (req.method === 'GET' && url === '/favicon.ico') {
      res.writeHead(204); // 无图标，静默避免浏览器 console 404
      res.end();
      return;
    }
    if (req.method === 'POST' && url === '/submit') {
      let body = '';
      req.on('data', (c) => {
        body += c;
        if (body.length > 1e6) req.destroy(); // 防超大 body
      });
      req.on('end', () => {
        let payload;
        try { payload = JSON.parse(body || '{}'); }
        catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end('{"ok":false,"error":"invalid json"}');
          return;
        }
        const rawResults = Array.isArray(payload.results) ? payload.results : [];
        const results = rawResults
          .filter((r) => r && r.id != null && String(r.id).length > 0) // 缺 id 的条目丢弃，避免写出 "undefined" 脏结果
          .map((r) => ({
            id: String(r.id),
            state: STATES.indexOf(r.state) >= 0 ? r.state : null,
            note: r.note != null && String(r.note).length ? String(r.note) : null,
          }));
        const out = {
          project: manifest.project || null,
          iteration: manifest.iteration || null,
          phase: manifest.phase || 'P5',
          submittedAt: new Date().toISOString(),
          results,
          summary: summarize(results),
        };
        try {
          fs.mkdirSync(path.dirname(outPath), { recursive: true });
          fs.writeFileSync(outPath, JSON.stringify(out, null, 2) + '\n');
        } catch (e) {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: false, error: 'write failed: ' + e.message }));
          return;
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, out: outPath, summary: out.summary }));
        if (onSubmitted) onSubmitted(out);
        if (exitOnSubmit) {
          // 响应刷出后再退，避免竞态
          setTimeout(() => { server.close(() => process.exit(0)); }, 120);
        }
      });
      return;
    }
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('not found');
  });

  return { server, outPath, html };
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help || !opts.manifest) {
    process.stderr.write('usage: node bridge.js <manifest.json> [--out results.json] [--port N] [--no-open]\n');
    process.exit(opts.help ? 0 : 2);
    return;
  }
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(opts.manifest, 'utf8'));
  } catch (e) {
    process.stderr.write('[delivery-selftest] 读取/解析 manifest 失败：' + e.message + '\n');
    process.exit(1);
    return;
  }
  if (!Array.isArray(manifest.items) || manifest.items.length === 0) {
    process.stderr.write('[delivery-selftest] manifest.items 必须是非空数组\n');
    process.exit(1);
    return;
  }
  const outPath = opts.out || path.join(path.dirname(path.resolve(opts.manifest)), 'results.json');
  const { server } = createBridge(manifest, { out: outPath, exitOnSubmit: true });
  server.listen(opts.port, '127.0.0.1', () => {
    const addr = server.address();
    const url = 'http://127.0.0.1:' + addr.port + '/';
    process.stdout.write('[delivery-selftest] serving ' + url + '\n');
    process.stdout.write('[delivery-selftest] results → ' + outPath + '\n');
    process.stdout.write('[delivery-selftest] 提交后自动写回结果并退出；Ctrl-C 可中断\n');
    if (!opts.noOpen) openBrowser(url);
  });
}

if (require.main === module) main();

module.exports = { parseArgs, summarize, createBridge, openBrowser, STATES };

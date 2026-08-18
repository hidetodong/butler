import io
s = io.open('.ai/01_CHANGELOG.md', encoding='utf-8').read()
line = [l for l in s.split('\n') if l.startswith('- `.ai/project/capabilities.md`')][0]
seg = line.split('22 个小节逐条核查，全部可弃——', 1)[1].split('，真源分别为', 1)[0]
parts = [p.strip() for p in seg.split('/') if p.strip()]
extra = 4 if 'Decision Map R1–R5 五节' in seg else 0
print(len(parts) + extra)

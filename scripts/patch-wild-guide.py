from pathlib import Path
import re
import subprocess

index = Path('index.html')
fragment = Path('scripts/wild-guide-fragment.html').read_text(encoding='utf-8')
s = index.read_text(encoding='utf-8')
start = s.find('<div id="wild-guide"')
if start < 0:
    raise SystemExit('Existing isolated wild guide was not found; stopping.')
end = s.find('</script></section>', start)
if end < 0:
    raise SystemExit('Wild guide end marker was not found; stopping.')
end += len('</script>')
s = s[:start] + fragment + s[end:]
blocks = re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>', s, re.I)
for i, js in enumerate(blocks, 1):
    f = Path(f'/tmp/check-{i}.js')
    f.write_text(js, encoding='utf-8')
    subprocess.run(['node', '--check', str(f)], check=True)
index.write_text(s, encoding='utf-8')

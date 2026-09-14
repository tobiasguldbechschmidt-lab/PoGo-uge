from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the menu button and the complete Field Research page.
s, n = re.subn(r'<button class="menu" data-p="research">.*?</button>', '', s, flags=re.S)
if n != 1:
    raise SystemExit(f'Expected one Field Research menu button, got {n}')
s, n = re.subn(r'<section class="page" id="p-research">.*?</section>\n', '', s, flags=re.S)
if n != 1:
    raise SystemExit(f'Expected one Field Research page, got {n}')

# Remove the research data endpoint from the URL map.
s, n = re.subn(r',research:B\+\'research_tasks\.json\'', '', s)
if n != 1:
    raise SystemExit(f'Expected one research endpoint, got {n}')

# Remove the navigation title entry.
s, n = re.subn(r",research:\['Field Research Tasks','Rewards'\]", '', s)
if n != 1:
    raise SystemExit(f'Expected one research title entry, got {n}')

# Remove the research page loader from show().
s, n = re.subn(r"if\(p==='research'\)research\(\);", '', s)
if n != 1:
    raise SystemExit(f'Expected one research loader call, got {n}')

# Remove the complete research() function, using the next stable function as the boundary.
s, n = re.subn(r'async function research\(\)\{.*?\}\n(?=async function dynamax\(\)\{)', '', s, flags=re.S)
if n != 1:
    raise SystemExit(f'Expected one research function, got {n}')

# Final safety checks: no Field Research UI or callable remains.
for needle in ('data-p="research"', 'id="p-research"', 'Field Research Tasks', 'research()'):
    if needle in s:
        raise SystemExit(f'Field Research remnant remains: {needle}')

p.write_text(s, encoding='utf-8')
print('Field Research removed successfully')

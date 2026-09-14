from pathlib import Path
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'maxbattles.json'
UA = 'Mozilla/5.0 (compatible; GO-Uge/1.0)'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

# Jina gives GitHub Actions a stable text representation of Snack Nap's
# client-rendered Max Battle page.
text = fetch('https://r.jina.ai/https://www.snacknap.com/max-battles').decode('utf-8', errors='replace')
types_raw = json.loads(fetch('https://pogoapi.net/api/v1/pokemon_types.json'))
shiny_raw = json.loads(fetch('https://pogoapi.net/api/v1/shiny_pokemon.json'))

# Plain-text/Markdown form contains headings followed by D-Max rows.
tier = None
entries = []
row_re = re.compile(r'D-(?:Max|G-Max)\s+(.+?)\s+CP\s+(\d+)\s*-\s*(\d+)\s*$', re.I)
for raw in text.splitlines():
    line = re.sub(r'\s+', ' ', raw).strip().strip('*').strip()
    tm = re.match(r'(?:#+\s*)?Tier\s+([1-6])\b', line, re.I)
    if tm:
        tier = int(tm.group(1))
        continue
    if tier is None:
        continue
    rm = row_re.search(line)
    if not rm:
        continue
    name = rm.group(1).strip()
    # Remove a trailing Markdown link marker if the mirror includes one.
    name = re.sub(r'\s*\[.*$', '', name).strip()
    cp_min, cp_max = int(rm.group(2)), int(rm.group(3))
    entries.append((tier, name, cp_min, cp_max))

if not entries:
    raise SystemExit('Could not parse any current Max Battle Pokémon from Snack Nap')

# Map names to Pokédex IDs from the current PogoAPI name dataset.
names_raw = json.loads(fetch('https://pogoapi.net/api/v1/pokemon_names.json'))
id_by_name = {}
for key, row in names_raw.items() if isinstance(names_raw, dict) else []:
    if isinstance(row, dict) and row.get('name'):
        id_by_name[str(row['name']).strip().lower()] = int(row.get('id', key))

# Current Pokémon typing.
type_map = {}
for row in types_raw if isinstance(types_raw, list) else types_raw.values():
    try:
        type_map[int(row.get('pokemon_id'))] = row.get('type', [])
    except (TypeError, ValueError):
        pass

shiny_map = shiny_raw if isinstance(shiny_raw, dict) else {}
def shiny_for(pid):
    row = shiny_map.get(str(pid), shiny_map.get(pid, {}))
    if not isinstance(row, dict):
        return False
    return any(bool(row.get(k)) for k in ('found_wild','found_raid','found_egg','found_evolution','found_research','found_photobomb','alolan_shiny'))

seen = set()
by_tier = {f'tier_{i}': [] for i in range(1, 7)}
for tier, name, cp_min, cp_max in entries:
    pid = id_by_name.get(name.lower())
    if not pid:
        continue
    key = (tier, pid)
    if key in seen:
        continue
    seen.add(key)
    by_tier[f'tier_{tier}'].append({
        'id': pid,
        'names': {'English': name},
        'level': tier,
        'types': type_map.get(pid, []),
        'shiny': shiny_for(pid),
        'assets': {'image': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pid}.png'},
        'cpRange': [cp_min, cp_max],
        'form': 'DYNAMAX',
    })

count = sum(len(v) for v in by_tier.values())
if count == 0:
    raise SystemExit('No Max Battle entries produced')

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'currentList': by_tier}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Wrote {count} current Max Battle entries')

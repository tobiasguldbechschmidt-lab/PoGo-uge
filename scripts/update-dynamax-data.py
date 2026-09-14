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

html = fetch('https://www.snacknap.com/max-battles').decode('utf-8', errors='replace')
types_raw = json.loads(fetch('https://pogoapi.net/api/v1/pokemon_types.json'))
shiny_raw = json.loads(fetch('https://pogoapi.net/api/v1/shiny_pokemon.json'))

# Snack Nap renders each current boss as a Pokedex link with its tier heading.
link_re = re.compile(r'href=[\"\'](?:https?://www\.snacknap\.com)?/pokedex/pokemon/(\d+)[^>]*>\s*(?:D-Max|G-Max)\s*([^<]+?)\s*CP\s*(\d+)\s*-\s*(\d+)', re.I)
tier_re = re.compile(r'>\s*Tier\s*([1-6])\s*<', re.I)

matches = list(link_re.finditer(html))
if not matches:
    raise SystemExit('Could not parse any current Max Battle Pokémon from Snack Nap')

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

# Determine the tier by the nearest preceding Tier heading.
entries = []
for m in matches:
    before = html[:m.start()]
    tiers = list(tier_re.finditer(before))
    if not tiers:
        continue
    tier = int(tiers[-1].group(1))
    pid = int(m.group(1))
    name = re.sub(r'\s+', ' ', m.group(2)).strip()
    cp_min, cp_max = int(m.group(3)), int(m.group(4))
    gmax = bool(re.search(r'g-max|gigantamax', m.group(0), re.I))
    entries.append({
        'id': pid,
        'names': {'English': name},
        'level': tier,
        'types': type_map.get(pid, []),
        'shiny': shiny_for(pid),
        'assets': {'image': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pid}.png'},
        'cpRange': [cp_min, cp_max],
        'form': 'GIGANTAMAX' if gmax or tier == 6 else 'DYNAMAX',
    })

# Keep one current entry per tier/species.
seen = set()
by_tier = {f'tier_{i}': [] for i in range(1, 7)}
for x in entries:
    key = (x['level'], x['id'])
    if key in seen:
        continue
    seen.add(key)
    by_tier[f"tier_{x['level']}"].append(x)

count = sum(len(v) for v in by_tier.values())
if count == 0:
    raise SystemExit('No Max Battle entries produced')

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'currentList': by_tier}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Wrote {count} current Max Battle entries')

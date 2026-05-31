import os
import re
import json

html_path = r"C:\Users\Nabendu\.gemini\antigravity-ide\brain\740b72b6-eaf7-4c32-b98b-72f4d3dd79e7\.system_generated\steps\274\content.md"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(r'n:\wuwabot\data\weapons.json', 'r', encoding='utf-8') as f:
    weapons = json.load(f)

boxes = html.split('<div class="ww-weapon-box box">')[1:]
count = 1
for box in boxes:
    # Fix rarity parsing
    # <p>Rarity:<!-- --> <strong class="rarity-ww rar-5">5<!-- -->★</strong></p>
    rarity_match = re.search(r'Rarity:.*?<strong[^>]*>(.*?)</strong>', box)
    if rarity_match:
        # 5<!-- -->★ -> 5★ -> 5-Star
        rarity_clean = rarity_match.group(1).replace('<!-- -->', '').replace('★', '-Star').strip()
        if str(count) in weapons:
            weapons[str(count)]["rarity"] = rarity_clean
    
    # Fix type parsing
    type_match = re.search(r'Type:\s*<strong>(.*?)</strong>', box)
    if type_match:
        type_clean = type_match.group(1).replace('<!-- -->', '').strip()
        if str(count) in weapons:
            weapons[str(count)]["type"] = type_clean

    count += 1

with open(r'n:\wuwabot\data\weapons.json', 'w', encoding='utf-8') as f:
    json.dump(weapons, f, indent=2)

print("Fixed rarity and type in weapons.json")

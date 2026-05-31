import re
import json
import urllib.request
import os

content_file = r'C:\Users\Nabendu\.gemini\antigravity-ide\brain\c620df9b-6f44-4488-9adb-7a8738ecf594\.system_generated\steps\101\content.md'
with open(content_file, 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('List of Ascension Materials</h3>')
if start_idx == -1:
    print("Could not find start of table.")
    exit(1)

table_start = text.find('<table', start_idx)
table_end = text.find('</table>', table_start)
table_html = text[table_start:table_end]

# Extract items: <img ... data-src="URL" ...> ... </a>
# We can find all matches of data-src='([^']+)' and the item name.
# Looking at the snippet:
# <a ...><img ... alt='Wuthering Waves - Item Name' data-src='...' ... /> Item Name</a>
pattern = re.compile(r"<a[^>]*>.*?data-src=['\"]([^'\"]+)['\"][^>]*>\s*(?:</?img[^>]*>\s*)*(.*?)\s*</a>", re.IGNORECASE | re.DOTALL)
matches = pattern.findall(table_html)

items_data = {}
items_json_path = r'n:\wuwabot\data\items.json'
img_dir = r'n:\wuwabot\img\items'

if not os.path.exists(img_dir):
    os.makedirs(img_dir, exist_ok=True)

if os.path.exists(items_json_path):
    with open(items_json_path, 'r', encoding='utf-8') as f:
        items_data = json.load(f)

print(f"Found {len(matches)} items in the table.")

for img_url, name in matches:
    name = name.strip()
    if not name: continue
    
    # Clean up name if it has HTML tags
    name = re.sub(r'<[^>]+>', '', name).strip()
    
    # Generate item key
    item_key = name.lower().replace("'", "").replace("-", "_").replace(" ", "_")
    
    # Add prefix/suffix handling if there are duplicates or weird characters? Should be fine.
    
    # Download image
    img_filename = f"{item_key}.png"
    img_path = os.path.join(img_dir, img_filename)
    
    # In items.json the path uses forward slashes
    icon_path = f"img/items/{img_filename}"
    
    print(f"Downloading {name} from {img_url}...")
    try:
        # Provide a User-Agent to avoid 403
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
        
    items_data[item_key] = {
        "name": name,
        "icon": icon_path
    }

with open(items_json_path, 'w', encoding='utf-8') as f:
    json.dump(items_data, f, indent=4)

print("Items updated successfully.")

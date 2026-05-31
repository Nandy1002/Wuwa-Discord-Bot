import re
import urllib.request
import os

content_file = r'C:\Users\Nabendu\.gemini\antigravity-ide\brain\c620df9b-6f44-4488-9adb-7a8738ecf594\.system_generated\steps\269\content.md'
with open(content_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Finding image url near 'Shell Credit'
match = re.search(r"<a[^>]*href=[^>]*>.*?<img[^>]*data-src=['\"]([^'\"]+)['\"][^>]*alt=['\"][^'\"]*Shell Credit[^'\"]*['\"][^>]*>.*?</a>", text, re.IGNORECASE)
if not match:
    match = re.search(r"<img[^>]*data-src=['\"]([^'\"]+)['\"][^>]*>.*?Shell Credit", text, re.IGNORECASE)

if match:
    img_url = match.group(1)
    print('Found URL:', img_url)
    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(r'n:\wuwabot\img\items\shell_credit.png', 'wb') as out_file:
        out_file.write(response.read())
    print('Shell Credit downloaded successfully.')
else:
    print('Shell Credit not found in the page.')

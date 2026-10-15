"""Rebuilds ../index.html from the data files: python kaynak/derle.py"""
import hashlib
import os
import re
import subprocess
import sys

base = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(base, "..")
for script in ["build.py", "build_extra.py", "build_exam.py"]:
    subprocess.check_call([sys.executable, "-I", os.path.join(base, script)])
subprocess.check_call([sys.executable, "-I", os.path.join(base, "assemble.py"), base, os.path.join(root, "index.html")])

# tie the service worker cache name to the built files, so installed copies pick up every new build
digest = hashlib.sha256()
for name in ["index.html", "manifest.webmanifest", "icon.svg"]:
    with open(os.path.join(root, name), "rb") as f:
        digest.update(f.read())
sw_path = os.path.join(root, "sw.js")
with open(sw_path, encoding="utf-8") as f:
    sw = f.read()
sw_new = re.sub(r'const CACHE = "[^"]*";', f'const CACHE = "kelime-kampi-{digest.hexdigest()[:10]}";', sw, count=1)
if sw_new == sw and "kelime-kampi-" + digest.hexdigest()[:10] not in sw:
    sys.exit("sw.js: CACHE satırı bulunamadı")
with open(sw_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(sw_new)
print("index.html güncellendi; sw.js önbellek sürümü:", digest.hexdigest()[:10])

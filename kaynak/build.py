import json, sys, os
base = os.path.dirname(os.path.abspath(__file__))
levels = ["a1", "a2", "b1", "b2", "c1", "oxford", "yds"]  # oxford.txt: extra Oxford 3000 words, level in 4th column
words = {}  # key -> dict
order = []
for lv in levels:
    with open(os.path.join(base, "data", lv + ".txt"), encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) < 3:
                print("BAD", lv, ln, line); continue
            w, pos, tr = parts[0].strip(), parts[1].strip(), parts[2].strip()
            if lv == "oxford":
                wlv = parts[3].strip() if len(parts) > 3 else "B1"
                syn = parts[4].strip() if len(parts) > 4 else ""
            elif lv == "yds":
                wlv = "YDS"
                syn = parts[3].strip() if len(parts) > 3 else ""
            else:
                wlv = lv.upper()
                extra = parts[3].strip() if len(parts) > 3 else ""
                syn = "" if extra in {"A1", "A2", "B1", "B2", "C1", "YDS"} else extra
            key = w.lower()
            if key in words:
                e = words[key]
                if lv == "yds":
                    e["y"] = 1
                    if syn and not e["s"]:
                        e["s"] = syn
                else:
                    # merge additional meaning
                    known = [m.strip() for m in e["t"].replace(";", ",").split(",")]
                    new = [m.strip() for m in tr.replace(";", ",").split(",") if m.strip() not in known]
                    if new:
                        e["t"] = e["t"] + "; " + ", ".join(new)
                    if pos not in e["p"].split("/"):
                        e["p"] += "/" + pos
                    if syn and not e["s"]:
                        e["s"] = syn
                continue
            words[key] = {"w": w, "p": pos, "t": tr, "l": wlv, "y": 1 if lv == "yds" else 0, "s": syn, "ipa": ""}
            order.append(key)
ipa_path = os.path.join(base, "data", "ipa.txt")
if os.path.exists(ipa_path):
    for line in open(ipa_path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        w, ipa = [x.strip() for x in line.split("|", 1)]
        if w.lower() in words:
            words[w.lower()]["ipa"] = ipa
syn_path = os.path.join(base, "data", "synonyms.txt")
if os.path.exists(syn_path):
    for line in open(syn_path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        w, syn = [x.strip() for x in line.split("|", 1)]
        e = words.get(w.lower())
        if e and syn and not e["s"]:
            e["s"] = syn
out = [[words[k]["w"], words[k]["p"], words[k]["t"], words[k]["l"], words[k]["y"], words[k]["s"], words[k].get("ipa", "")] for k in order]
from collections import Counter
c = Counter(x[3] for x in out)
print("total", len(out), dict(c), "yds-flag", sum(x[4] for x in out))
with open(os.path.join(base, "words.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

import json, os, sys
from collections import Counter
base = os.path.dirname(os.path.abspath(__file__))
errs = []
groups = []
ROMAN = ["I", "II", "III", "IV", "V"]
data_dir = os.path.join(base, "data")
exam_files = sorted(fn for fn in os.listdir(data_dir) if fn.startswith("exam_") and fn.endswith(".txt"))
for fn in exam_files:
    g = None
    for ln, line in enumerate(open(os.path.join(data_dir, fn), encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        if line.startswith("## "):
            parts = [x.strip() for x in line[3:].split("|")]
            g = {"id": parts[0], "type": parts[1], "lv": parts[2], "topic": parts[3] if len(parts) > 3 else "", "p": [], "qs": []}
            groups.append(g)
            continue
        tag, rest = line[:3], line[3:].strip()
        if tag == "P: ": g["p"].append(rest)
        elif tag == "Q: ": g["qs"].append({"s": rest, "a": None, "x": [], "w": ""})
        elif tag == "A: ": g["qs"][-1]["a"] = rest
        elif tag == "X: ": g["qs"][-1]["x"].append(rest)
        elif tag == "W: ": g["qs"][-1]["w"] = rest
        else: errs.append(f"{fn}:{ln} unknown line")
for g in groups:
    g["p"] = "\n".join(g["p"])
    for n, q in enumerate(g["qs"]):
        where = f"{g['id']} q{n+1}"
        if not q["a"]: errs.append(where + " no answer")
        if len(q["x"]) != 4: errs.append(where + f" distractors={len(q['x'])}")
        if q["a"] in q["x"]: errs.append(where + " answer among distractors")
        if not q["w"]: errs.append(where + " no explanation")
        if g["type"] == "irrelevant" and sorted([q["a"]] + q["x"], key=ROMAN.index) != ROMAN: errs.append(where + " roman options")
    if g["type"] == "reading" and len(g["qs"]) != 4: errs.append(g["id"] + " reading needs 4 questions")
    if g["type"] == "cloze":
        if len(g["qs"]) != 5: errs.append(g["id"] + " cloze needs 5 blanks")
        for k in range(1, 6):
            if f"({k})___" not in g["p"]: errs.append(g["id"] + f" missing blank ({k})")
    if g["type"] in ("parcomp", "dialogue") and "___" not in g["p"]: errs.append(g["id"] + " passage has no blank")
ids = Counter(g["id"] for g in groups)
for k, v in ids.items():
    if v > 1: errs.append("duplicate id " + k)
print("groups", len(groups), dict(Counter(g["type"] for g in groups)), "questions", sum(len(g["qs"]) for g in groups))
# answer position balance for irrelevant
print("irrelevant answers", Counter(g["qs"][0]["a"] for g in groups if g["type"] == "irrelevant"))

depth = {"fam": [], "conf": [], "coll": []}
sec = None
for ln, line in enumerate(open(os.path.join(base, "data", "depth.txt"), encoding="utf-8"), 1):
    line = line.strip()
    if not line: continue
    if line.startswith("@"): sec = line[1:]; continue
    p = [x.strip() for x in line.split("|")]
    if sec == "fam":
        forms = [f.split(" (")[0].strip() for f in p[0].split(",")]
        if len(p) != 4 or p[2] not in forms or p[1].count("___") != 1: errs.append(f"depth:{ln} fam"); continue
        depth["fam"].append({"forms": p[0], "s": p[1], "a": p[2], "d": [f for f in forms if f != p[2]], "tr": p[3]})
    elif sec == "conf":
        grp = [x.strip() for x in p[0].split("/")]
        if len(p) != 5 or p[3] not in grp or p[2].count("___") != 1: errs.append(f"depth:{ln} conf"); continue
        depth["conf"].append({"grp": p[0], "why": p[1], "s": p[2], "a": p[3], "d": [x for x in grp if x != p[3]], "tr": p[4]})
    elif sec == "coll":
        ds = [x.strip() for x in p[2].split(";")] if len(p) > 2 else []
        if len(p) != 5 or len(ds) != 3 or p[1] in ds or p[0].count("___") != 1: errs.append(f"depth:{ln} coll"); continue
        depth["coll"].append({"s": p[0], "a": p[1], "d": ds, "tr": p[3], "why": p[4]})
print("depth", {k: len(v) for k, v in depth.items()})
for e in errs: print("ERR", e)
json.dump(groups, open(os.path.join(base, "exam.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump(depth, open(os.path.join(base, "depth.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
sys.exit(1 if errs else 0)

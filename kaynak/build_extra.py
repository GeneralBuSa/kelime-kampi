import json, os, sys

def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
base = os.path.dirname(os.path.abspath(__file__))
words = {w[0].lower(): w for w in _load(os.path.join(base, "words.json"))}
errs = []

topics = []
for fn in ["grammar1.txt", "grammar2.txt"]:
    cur = None
    for ln, line in enumerate(open(os.path.join(base, "data", fn), encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        tag, rest = line[:2], line[2:].strip()
        if tag == "# ":
            tid, lv, en, tr = [x.strip() for x in rest.split("|")]
            cur = {"id": tid, "lv": lv, "en": en, "tr": tr, "p": [], "f": [], "e": [], "q": []}
            topics.append(cur)
        elif tag == "> ":
            cur["p"].append(rest)
        elif tag == "= ":
            cur["f"].append(rest)
        elif tag == "e ":
            en, tr = [x.strip() for x in rest.split("||")]
            cur["e"].append([en, tr])
        elif tag == "? ":
            parts = [x.strip() for x in rest.split("|")]
            if len(parts) != 4:
                errs.append(f"{fn}:{ln} parts={len(parts)}"); continue
            s, a, d, why = parts
            ds = [x.strip() for x in d.split(";")]
            if s.count("___") != 1: errs.append(f"{fn}:{ln} blanks={s.count('___')}")
            if len(ds) != 3: errs.append(f"{fn}:{ln} distractors={len(ds)}")
            if a.lower() in [x.lower() for x in ds]: errs.append(f"{fn}:{ln} answer among distractors")
            cur["q"].append([s, a, ds, why])
        else:
            errs.append(f"{fn}:{ln} unknown line")

by_id = {t["id"]: t for t in topics}
drill = os.path.join(base, "data", "grammar_drill.txt")
if os.path.exists(drill):
    cur_id = None
    for ln, line in enumerate(open(drill, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("//"):
            continue
        if line.startswith("# "):
            cur_id = line[2:].strip().split("|")[0]
            if cur_id not in by_id:
                errs.append(f"grammar_drill.txt:{ln} unknown topic {cur_id}")
            continue
        if not line.startswith("? "):
            errs.append(f"grammar_drill.txt:{ln} unknown line")
            continue
        parts = [x.strip() for x in line[2:].split("|")]
        if len(parts) != 4:
            errs.append(f"grammar_drill.txt:{ln} parts={len(parts)}")
            continue
        s, a, d, why = parts
        ds = [x.strip() for x in d.split(";")]
        if s.count("___") != 1 or len(ds) != 3 or a.lower() in [x.lower() for x in ds]:
            errs.append(f"grammar_drill.txt:{ln} bad question")
            continue
        if cur_id in by_id:
            by_id[cur_id]["q"].append([s, a, ds, why])

sents = []
sent_files = ["sentences.txt", "sentences_more.txt"]
for sfn in sent_files:
  spath = os.path.join(base, "data", sfn)
  if not os.path.exists(spath):
    continue
  for ln, line in enumerate(open(spath, encoding="utf-8"), 1):
    line = line.strip()
    if not line: continue
    parts = [x.strip() for x in line.split("|")]
    if len(parts) != 5: errs.append(f"{sfn}:{ln} parts={len(parts)}"); continue
    lemma, ans, s, d, tr = parts
    ds = [x.strip() for x in d.split(";")]
    if lemma.lower() not in words: errs.append(f"{sfn}:{ln} lemma not in word list: {lemma}")
    if s.count("___") != 1: errs.append(f"{sfn}:{ln} blanks")
    if len(ds) != 3: errs.append(f"{sfn}:{ln} distractors={len(ds)}")
    if ans.lower() in [x.lower() for x in ds]: errs.append(f"{sfn}:{ln} answer among distractors")
    sents.append([lemma, ans, s, ds, tr])

from collections import Counter
print("topics", len(topics), dict(Counter(t["lv"] for t in topics)), "questions", sum(len(t["q"]) for t in topics))
print("sentences", len(sents), dict(Counter(words[s[0].lower()][3] for s in sents if s[0].lower() in words)))
for e in errs: print("ERR", e)
json.dump(topics, open(os.path.join(base, "grammar.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump(sents, open(os.path.join(base, "sents.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
sys.exit(1 if errs else 0)

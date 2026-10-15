"""Heuristic review of generated content.
Run: python kaynak/review_content.py
"""
import json, os, sys
base = os.path.dirname(os.path.abspath(__file__))
warns, hard = [], []

exam = json.load(open(os.path.join(base, "exam.json"), encoding="utf-8"))
for g in exam:
    for n, q in enumerate(g["qs"]):
        where = f"{g['id']} q{n+1}"
        opts = [q["a"]] + q["x"]
        low = [o.strip().lower() for o in opts]
        if len(set(low)) < len(low):
            hard.append(where + " duplicate option")
        if q["w"] and len(q["w"]) < 20:
            warns.append(where + " short explanation")
        if g["type"] != "irrelevant" and q["a"] in q["x"]:
            hard.append(where + " answer in distractors")

sents = json.load(open(os.path.join(base, "sents.json"), encoding="utf-8"))
seen = {}
for i, row in enumerate(sents):
    lemma, ans, s, ds, tr = row
    if ans.lower() in [x.lower() for x in ds]:
        hard.append(f"sent {i} {lemma} answer in distractors")
    if s.count("___") != 1:
        hard.append(f"sent {i} {lemma} blanks")
    seen[lemma] = seen.get(lemma, 0) + 1

gram = json.load(open(os.path.join(base, "grammar.json"), encoding="utf-8"))
gq = 0
for t in gram:
    for n, q in enumerate(t["q"]):
        gq += 1
        s, a, ds, why = q
        if a.lower() in [x.lower() for x in ds]:
            hard.append(f"gram {t['id']} q{n+1} answer in distractors")
        if s.count("___") != 1:
            hard.append(f"gram {t['id']} q{n+1} blanks")

depth = json.load(open(os.path.join(base, "depth.json"), encoding="utf-8"))
for i, r in enumerate(depth.get("fam", [])):
    if r["a"] in r["d"]:
        hard.append(f"depth fam {i} answer in distractors")
for i, r in enumerate(depth.get("conf", [])):
    if r["a"] in r["d"]:
        hard.append(f"depth conf {i} answer in distractors")
for i, r in enumerate(depth.get("coll", [])):
    if r["a"].lower() in [x.lower() for x in r["d"]]:
        hard.append(f"depth coll {i} answer in distractors")

print("exam groups", len(exam), "questions", sum(len(g["qs"]) for g in exam))
print("sentences", len(sents), "unique lemmas", len(seen))
print("grammar questions", gq)
print("depth", {k: len(v) for k, v in depth.items()})
print("hard", len(hard), "warnings", len(warns))
for w in hard[:30]:
    print("HARD", w)
for w in warns[:20]:
    print("WARN", w)
sys.exit(1 if hard else 0)

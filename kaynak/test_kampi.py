"""Unit tests for scoring, Leitner intervals, and cloud packing sizes."""
import json, os, unittest

def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

INTERVALS = [0, 1, 2, 4, 7, 15, 30, 60]
MASTER = 4

def grade_box(box, ok, weight=1):
    if ok:
        box = min(7, box + weight)
    else:
        box = max(0, min(box - 2, 1))
    return box

def mock_score(ok, n):
    return round(ok * (100 / n) * 100) / 100

class KampiTests(unittest.TestCase):
    def test_full_mock_score(self):
        self.assertEqual(mock_score(80, 80), 100)
        self.assertEqual(mock_score(48, 80), 60)
        self.assertEqual(mock_score(1, 80), 1.25)

    def test_short_mock_score(self):
        self.assertEqual(mock_score(40, 40), 100)
        self.assertEqual(mock_score(20, 40), 50)
        self.assertEqual(mock_score(20, 20), 100)
        self.assertEqual(mock_score(10, 20), 50)

    def test_leitner_correct_advances(self):
        b = 0
        for _ in range(4):
            b = grade_box(b, True)
        self.assertGreaterEqual(b, MASTER)

    def test_leitner_wrong_drops(self):
        self.assertEqual(grade_box(5, False), 1)
        self.assertEqual(grade_box(0, False), 0)

    def test_interval_table(self):
        self.assertEqual(len(INTERVALS), 8)
        self.assertEqual(INTERVALS[4], 7)

    def test_exam_bank_targets(self):
        base = os.path.dirname(os.path.abspath(__file__))
        exam = _load(os.path.join(base, "exam.json"))
        from collections import Counter
        c = Counter(g["type"] for g in exam)
        self.assertGreaterEqual(c["reading"], 25)
        self.assertGreaterEqual(c["cloze"], 15)
        for t in ("dialogue", "restate", "parcomp", "irrelevant", "en_tr", "tr_en"):
            self.assertGreaterEqual(c[t], 20, t)
        self.assertGreaterEqual(c["sentcomp"], 20)
        # every passage offers one of the less common YDS stems (title, attitude, NOT, purpose)
        for g in exam:
            if g["type"] == "reading":
                self.assertTrue(any(q.get("k") in ("baslik", "tutum", "degil", "amac") for q in g["qs"]), g["id"])
            if g["type"] in ("cloze", "sentcomp"):
                for q in g["qs"]:
                    self.assertTrue(q.get("t"), g["id"] + " has no trap type")
        # no two passages share the same opening sentence (duplicate texts)
        openings = [g["p"].split(".")[0] for g in exam if g["type"] == "reading"]
        self.assertEqual(len(openings), len(set(openings)))

    def test_sentence_cover(self):
        base = os.path.dirname(os.path.abspath(__file__))
        sents = _load(os.path.join(base, "sents.json"))
        self.assertGreaterEqual(len(sents), 350)

    def test_grammar_and_depth_cover(self):
        base = os.path.dirname(os.path.abspath(__file__))
        gram = _load(os.path.join(base, "grammar.json"))
        depth = _load(os.path.join(base, "depth.json"))
        gq = sum(len(t["q"]) for t in gram)
        self.assertGreaterEqual(gq, 300)
        self.assertGreaterEqual(len(depth["fam"]), 40)
        self.assertGreaterEqual(len(depth["conf"]), 30)
        self.assertGreaterEqual(len(depth["coll"]), 40)

    def test_ipa_and_syn_cover(self):
        base = os.path.dirname(os.path.abspath(__file__))
        words = _load(os.path.join(base, "words.json"))
        ipa = sum(1 for w in words if len(w) > 6 and w[6])
        syn = sum(1 for w in words if w[5])
        self.assertGreaterEqual(ipa, 200)
        self.assertGreaterEqual(syn, 400)

if __name__ == "__main__":
    unittest.main()

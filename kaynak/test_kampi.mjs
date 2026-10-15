/** Tests the app's real functions: they are read by name from the built index.html, not copied here.
 *  Run after a build: node kaynak/test_kampi.mjs */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const html = readFileSync(fileURLToPath(new URL("../index.html", import.meta.url)), "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const app = scripts[scripts.length - 1][1].split(String.fromCharCode(13)).join("");

// one-line top-level constants and top-level functions (which close with "}" at the start of a line)
function constDecl(name) {
  const m = app.match(new RegExp(`^const ${name} = .*;[^\\n]*$`, "m"));
  if (!m) throw new Error("const not found in app: " + name);
  return m[0];
}
function fnDecl(name) {
  const start = app.indexOf(`\nfunction ${name}(`);
  if (start < 0) throw new Error("function not found in app: " + name);
  const oneLine = app.indexOf("\n", start + 1);
  const line = app.slice(start + 1, oneLine);
  if (line.trimEnd().endsWith("}")) return line;
  const end = app.indexOf("\n}\n", start);
  return app.slice(start + 1, end + 2);
}
const code = [
  ...["INTERVALS", "MASTER", "today", "esc", "shuffle", "blank", "IRREG", "RICH_STEMS"].map(constDecl),
  ...["mockScore", "grade", "merge", "packCloud", "unpackCloud", "richText", "lookupWord", "pickReadingItems"].map(fnDecl)
].join("\n");
const ctx = vm.createContext({ S: { prog: {} }, BYKEY: new Map(), Blob });
vm.runInContext(code + "\nthis.api = { INTERVALS, MASTER, today, esc, blank, mockScore, grade, merge, packCloud, unpackCloud, richText, lookupWord, pickReadingItems };", ctx);
const A = ctx.api;

let failed = 0, passed = 0;
function eq(name, a, b) {
  const ok = Object.is(a, b) || JSON.stringify(a) === JSON.stringify(b);
  if (ok) passed++; else { failed++; console.error("FAIL", name, "\n  got:     ", a, "\n  expected:", b); }
}

// scoring: every question is worth 100 / n points (1.25 in the full 80-question mock)
eq("full mock 80/80", A.mockScore(80, 80), 100);
eq("full mock 1/80", A.mockScore(1, 80), 1.25);
eq("short mock 20/40", A.mockScore(20, 40), 50);
eq("mini mock 10/20", A.mockScore(10, 20), 50);

// spaced repetition
ctx.S.prog = {};
const cat = { w: "Cat" };
for (let i = 0; i < 4; i++) A.grade(cat, true);
eq("four correct answers reach MASTER", ctx.S.prog.cat[0] >= A.MASTER, true);
eq("next review after box 4 is 7 days later", ctx.S.prog.cat[1] - A.today(), A.INTERVALS[4]);
A.grade(cat, false);
eq("a wrong answer drops the box to 1 or below", ctx.S.prog.cat[0] <= 1, true);
eq("wrong answers are counted", ctx.S.prog.cat[3], 1);
eq("a wrong word is due today", ctx.S.prog.cat[1], A.today());

eq("escape HTML", A.esc(`a&b<"'>`), "a&amp;b&lt;&quot;&#39;&gt;");

// merging two copies of the progress (browser + account / backup)
const m = A.merge(
  { ts: 1, xp: 10, prog: { cat: [1, 0, 2, 0] }, badges: { a: 1 }, mocks: [{ ts: 5, score: 40 }] },
  { ts: 2, xp: 8, prog: { cat: [2, 0, 5, 1], dog: [0, 0, 1, 0] }, badges: { b: 2 }, mocks: [{ ts: 5, score: 40 }, { ts: 9, score: 60 }] }
);
eq("merge keeps the higher XP", m.xp, 10);
eq("merge keeps the record with more answers", m.prog.cat[2] + m.prog.cat[3], 6);
eq("merge keeps words found on only one side", m.prog.dog[2], 1);
eq("merge unites badges", Object.keys(m.badges).sort(), ["a", "b"]);
eq("merge unites mocks without duplicates", m.mocks.map(x => x.ts), [5, 9]);

// account storage is split into parts and must come back unchanged; the API key never leaves the browser
const state = Object.assign(A.blank(), { ts: 3, xp: 7, prog: { a: [1, 0, 1, 0] }, gq: { g: [1] }, badges: { x: 1 }, hist: [{ ts: 1 }], mocks: [{ ts: 2 }], aiKey: "sk-secret" });
const packed = A.packCloud(state);
eq("packed core has no word records", packed.core.prog, undefined);
eq("packed core has no API key", packed.core.aiKey, undefined);
const back = A.unpackCloud(JSON.parse(JSON.stringify(packed)));
eq("unpack restores word records", back.prog, state.prog);
eq("unpack restores grammar records", back.gq, state.gq);
eq("unpack restores badges and mocks", [back.badges, back.mocks], [state.badges, state.mocks]);

// reading passages: gaps survive, words become tappable, text stays escaped
const rt = A.richText("A (1)___ b's & <c> ___.", true, "1");
eq("cloze gap kept and marked current", rt.includes('<span class="pgap cur">(1)</span>'), true);
eq("plain gap kept", rt.includes('<span class="gap"'), true);
eq("words tappable", rt.includes('<span class="tw">A</span>') && rt.includes('<span class="tw">b&#39;s</span>'), true);
eq("special characters escaped", rt.includes("&amp;") && rt.includes("&lt;") && !rt.includes("<c>"), true);
eq("no taps in the mock exam", A.richText("Hello world", false, null), "Hello world");

// tapping a word finds its dictionary entry from inflected forms
ctx.BYKEY.clear();
for (const w of ["decline", "study", "child", "make", "stop", "be", "happy", "rapid", "go"]) ctx.BYKEY.set(w, { w });
const look = raw => (A.lookupWord(raw) || {}).w || null;
eq("declined -> decline", look("declined"), "decline");
eq("studies -> study", look("studies"), "study");
eq("children -> child", look("Children"), "child");
eq("making -> make", look("making"), "make");
eq("stopped -> stop", look("stopped"), "stop");
eq("were -> be", look("were"), "be");
eq("happily -> happy", look("happily"), "happy");
eq("rapidly -> rapid", look("rapidly"), "rapid");
eq("went -> go", look("went"), "go");
eq("unknown word -> null", look("zzzz"), null);

// mock exam: four questions per passage, in passage order, with one of the rarer stem types when present
const g = { items: ["ayrinti", "anafikir", "kelime", "cikarim", "baslik"].map((k, n) => ({ n, k })) };
for (let i = 0; i < 20; i++) {
  const picked = A.pickReadingItems(g, 4);
  eq("four questions per passage", picked.length, 4);
  eq("questions keep passage order", picked.map(x => x.n), [...picked.map(x => x.n)].sort((a, b) => a - b));
  eq("rare stem included", picked.some(x => x.k === "baslik"), true);
}
eq("short passage returns all its questions", A.pickReadingItems({ items: [{ n: 0 }, { n: 1 }] }, 4).length, 2);

if (failed) { console.error(`${failed} failed, ${passed} passed`); process.exit(1); }
console.log("ok", passed);

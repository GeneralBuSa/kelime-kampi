/** Node tests for scoring, Leitner, merge, and cloud packing. Run: node kaynak/test_kampi.mjs */
const INTERVALS = [0, 1, 2, 4, 7, 15, 30, 60];
const MASTER = 4;

function gradeBox(box, ok, weight = 1) {
  if (ok) box = Math.min(7, box + weight);
  else box = Math.max(0, Math.min(box - 2, 1));
  return box;
}

function mockScore(ok, n) {
  return Math.round(ok * (100 / n) * 100) / 100;
}

function mergeMap(ma = {}, mb = {}) {
  const o = Object.assign({}, ma);
  for (const k in mb) {
    const x = o[k], y = mb[k];
    if (!x || (y[2] + y[3]) > (x[2] + x[3])) o[k] = y;
  }
  return o;
}

function merge(a, b) {
  const out = Object.assign({}, a.ts >= b.ts ? a : b);
  out.prog = mergeMap(a.prog, b.prog);
  out.xp = Math.max(a.xp || 0, b.xp || 0);
  return out;
}

function packCloud(s) {
  const maps = { gq: s.gq, badges: s.badges };
  const hist = { hist: (s.hist || []).slice(-200) };
  const core = Object.assign({}, s);
  delete core.prog; delete core.gq; delete core.badges; delete core.hist;
  return { core, prog: { prog: s.prog }, maps, hist };
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

let failed = 0;
function eq(name, a, b) {
  const ok = Object.is(a, b) || JSON.stringify(a) === JSON.stringify(b);
  if (!ok) { failed++; console.error("FAIL", name, a, "!=", b); }
}

eq("full mock 80/80", mockScore(80, 80), 100);
eq("full mock 1/80", mockScore(1, 80), 1.25);
eq("short mock 20/40", mockScore(20, 40), 50);
eq("leitner 4 correct", [0, 1, 2, 3].reduce(b => gradeBox(b, true), 0) >= MASTER, true);
eq("leitner wrong from 5", gradeBox(5, false), 1);
eq("interval day 4", INTERVALS[4], 7);
eq("esc", esc(`a&b<"'>`), "a&amp;b&lt;&quot;&#39;&gt;");

const m = merge(
  { ts: 1, xp: 10, prog: { cat: [1, 0, 2, 0] } },
  { ts: 2, xp: 8, prog: { cat: [2, 0, 5, 1], dog: [0, 0, 1, 0] } }
);
eq("merge xp max", m.xp, 10);
eq("merge more answers wins", m.prog.cat[2] + m.prog.cat[3], 6);
eq("merge keeps extra key", m.prog.dog[2], 1);

const packed = packCloud({ ts: 1, xp: 3, prog: { a: [1] }, gq: { g: [1] }, badges: { x: 1 }, hist: [{ ts: 1 }], extra: true });
eq("pack core has no prog", packed.core.prog, undefined);
eq("pack prog isolated", packed.prog.prog.a[0], 1);

if (failed) { console.error(failed + " failed"); process.exit(1); }
console.log("ok", 11);

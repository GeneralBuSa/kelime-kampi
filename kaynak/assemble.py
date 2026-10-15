import sys, re
sp, out = sys.argv[1], sys.argv[2]
tpl = open(sp + "/template.html", encoding="utf-8").read()
def data(fn): return open(sp + "/" + fn, encoding="utf-8").read().replace("</", "<\/")
html = tpl.replace("__WORDS__", data("words.json")).replace("__GRAM__", data("grammar.json")).replace("__SENTS__", data("sents.json")).replace("__EXAM__", data("exam.json")).replace("__DEPTH__", data("depth.json"))
open(out, "w", encoding="utf-8").write(html)
scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
open(sp + "/check.js", "w", encoding="utf-8").write(scripts[-1])
print(len(html))

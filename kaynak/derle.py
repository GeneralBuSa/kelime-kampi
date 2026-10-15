"""Rebuilds ../index.html from the data files: python kaynak/derle.py"""
import os
import subprocess
import sys

base = os.path.dirname(os.path.abspath(__file__))
for script in ["build.py", "build_extra.py", "build_exam.py"]:
    subprocess.check_call([sys.executable, "-I", os.path.join(base, script)])
subprocess.check_call([sys.executable, "-I", os.path.join(base, "assemble.py"), base, os.path.join(base, "..", "index.html")])
print("index.html güncellendi")

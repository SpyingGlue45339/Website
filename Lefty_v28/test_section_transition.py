from pathlib import Path
import ast

root = Path(__file__).parent
source = (root / "section_page.py").read_text(encoding="utf-8")
main = (root / "main.py").read_text(encoding="utf-8")

ast.parse(source)
ast.parse(main)

assert "MOUSEBUTTONDOWN" in source
assert "event.button == 1" in source
assert 'return "continue"' in source
assert "continue_rect" not in source
assert "section_intro" not in main
assert "section_page" in main
assert "for q in qs:" in main
assert "get_answer(screen,q,num)" in main

print("PASS: section page advances on any left click.")
print("PASS: no section hitbox remains.")
print("PASS: main hands directly from section page to get_answer().")

from pathlib import Path
import ast

p = Path(__file__).parent / "section_intro.py"
source = p.read_text(encoding="utf-8")
tree = ast.parse(source)

assert "pygame.event.clear()" in source
assert "pygame.event.get()" in source
assert "pygame.MOUSEBUTTONDOWN" in source
assert "pygame.K_RETURN" in source
assert "pygame.K_SPACE" in source
assert 'return "continue"' in source
assert 'return "quit"' in source
assert "pygame.time.delay" not in source

print("PASS: section intro uses a live event loop with mouse/keyboard controls.")

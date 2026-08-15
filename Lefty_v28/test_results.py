# Results-page regression tests.
# There are deliberately no quadrant classification strings in the result
# interface anymore. Exact coordinates belong on ANALYSE RESULTS only.

from results import _section_score_text

assert "left" in _section_score_text("Economy", -1.0, 0.0)
assert "right" in _section_score_text("Economy", 1.0, 0.0)
assert "authority" in _section_score_text("Government", 0.0, 1.0)
assert "liberty" in _section_score_text("Culture", 0.0, -1.0)
assert "AUTHORITARIAN LEFT" not in _section_score_text("Economy", -1.0, 1.0).upper()
print("Results-page regression tests passed.")

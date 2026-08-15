
from questions import QUESTIONS, SECTIONS

assert len(SECTIONS) == 4
assert all(section_questions for _, section_questions in SECTIONS)

positions = {q["id"]: i + 1 for i, q in enumerate(QUESTIONS)}

for name, qs in SECTIONS:
    assert qs[0]["id"] in positions
    assert qs[-1]["id"] in positions
    assert positions[qs[0]["id"]] <= positions[qs[-1]["id"]]

print("PASS: all four section fronts have valid first/last question positions.")
for name, qs in SECTIONS:
    print(
        f"{name}: quiz questions "
        f"{positions[qs[0]['id']]:02d}-{positions[qs[-1]['id']]:02d}"
    )

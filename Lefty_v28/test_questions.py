from questions import QUESTIONS,SECTIONS
from scoring import score_question
assert len(QUESTIONS)==38
assert len(SECTIONS)==4
assert len({q["id"] for q in QUESTIONS})==38
for q in QUESTIONS:
    assert q["question"] and isinstance(q["x"],(int,float)) and isinstance(q["y"],(int,float))
print("PASS: 38 questions, 4 sections, valid scoring data.")

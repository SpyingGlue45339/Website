RESPONSE_LABELS = [
    "STRONGLY DISAGREE",
    "DISAGREE",
    "AGREE",
    "STRONGLY AGREE",
]

# No neutral midpoint. Every answer takes a position.
RESPONSE_MULTIPLIERS = [-1.0, -0.5, 0.5, 1.0]


def score_question(question, answer_index):
    m = RESPONSE_MULTIPLIERS[answer_index]
    return question["x"] * m, question["y"] * m

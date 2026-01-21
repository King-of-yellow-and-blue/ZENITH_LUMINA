def generate_debugger_questions(topic, level="STANDARD"):
    questions = []

    if topic == "Velocity":
        questions = [
            "What assumption are you making about the direction of motion?",
            "Does your answer change if the reference direction is reversed?",
            "Are you confusing magnitude with vector quantity?"
        ]

    elif topic == "Distance":
        questions = [
            "Are you assuming the path is straight?",
            "Would your answer change if the motion were circular?",
            "Have you implicitly equated distance with displacement?"
        ]

    else:
        questions = [
            "What is the key assumption behind your answer?",
            "Under what condition would your reasoning fail?",
            "Can you identify a counter-example?"
        ]

    return {
        "mode": "DEBUGGER",
        "instruction": "Answer the following questions one by one. Do not rush.",
        "questions": questions
    }

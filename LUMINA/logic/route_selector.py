MATHEMATICAL_TOPICS = [
    "Velocity",
    "Acceleration",
    "Equations of Motion",
    "Integration",
    "Differentiation"
]

def classify_topic(topic):
    if topic in MATHEMATICAL_TOPICS:
        return "MATHEMATICAL"
    return "NON_MATHEMATICAL"

def select_route(topic_type, explanation_length="SHORT", user_choice=None):
    if explanation_length == "SHORT":
        return ["DEFAULT"]

    if topic_type == "NON_MATHEMATICAL":
        return ["ANALOGY", "VISUAL"]

    if topic_type == "MATHEMATICAL":
        if user_choice:
            return [user_choice]
        return ["ANALOGY", "MATHEMATICAL", "VISUAL"]

    return ["DEFAULT"]

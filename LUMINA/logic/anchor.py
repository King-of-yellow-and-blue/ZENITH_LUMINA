import json

with open("knowledge/syllabus.json", "r") as f:
    SYLLABUS = json.load(f)

def anchor_topic(topic):
    matches = []

    for class_name, subjects in SYLLABUS.items():
        for subject, chapters in subjects.items():
            for chapter, topics in chapters.items():
                if topic.lower() in [t.lower() for t in topics]:
                    matches.append({
                        "class": class_name,
                        "subject": subject,
                        "chapter": chapter
                    })

    if len(matches) == 0:
        return {
            "status": "NOT_FOUND",
            "message": "Topic not found in syllabus"
        }

    if len(matches) == 1:
        return {
            "status": "RESOLVED",
            "data": matches[0]
        }

    return {
        "status": "AMBIGUOUS",
        "options": matches
    }


def generate_clarifying_question(anchor_result):
    if anchor_result["status"] != "AMBIGUOUS":
        return None

    options = anchor_result["options"]

    question = {
        "mode": "CLARIFICATION_REQUIRED",
        "question": "This topic exists in multiple contexts. Please choose one:",
        "choices": []
    }

    for idx, opt in enumerate(options, start=1):
        question["choices"].append({
            "id": idx,
            "class": opt["class"],
            "subject": opt["subject"],
            "chapter": opt["chapter"]
        })

    return question

import json

with open("knowledge/prerequisites.json", "r") as f:
    PREREQUISITES = json.load(f)

def check_prerequisites(topic, known_topics=None):
    if known_topics is None:
        known_topics = []

    required = PREREQUISITES.get(topic, [])

    missing = [t for t in required if t not in known_topics]

    if missing:
        return {
            "status": "MISSING_PREREQUISITES",
            "missing_topics": missing
        }

    return {
        "status": "CLEAR",
        "missing_topics": []
    }

def generate_bridge_course(missing_topics):
    bridge = []

    for topic in missing_topics:
        bridge.append({
            "topic": topic,
            "duration": "5 minutes",
            "structure": [
                "Why this concept matters",
                "Core definition",
                "Simple example",
                "Key formula (if applicable)",
                "Quick readiness check"
            ]
        })

    return {
        "mode": "BRIDGE_COURSE",
        "total_duration": f"{5 * len(missing_topics)} minutes",
        "modules": bridge
    }

import json

with open("knowledge/misconceptions.json", "r") as f:
    MISCONCEPTIONS = json.load(f)

def get_misconceptions(topic):
    return MISCONCEPTIONS.get(topic, [])

def build_prompt(topic, route, context):
    if route == "ANALOGY":
        prompt_file = "prompts/analogy.txt"
    elif route == "MATHEMATICAL":
        prompt_file = "prompts/mathematical.txt"
    elif route == "VISUAL":
        prompt_file = "prompts/visual.txt"
    else:
        prompt_file = "prompts/analogy.txt"

    with open(prompt_file, "r") as f:
        base_prompt = f.read()

    final_prompt = f"""
{base_prompt}

Topic: {topic}

Context:
{context}
"""

    return final_prompt

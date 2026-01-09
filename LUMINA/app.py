from flask import Flask, request, jsonify
from logic.anchor import anchor_topic
from logic.prerequisite import check_prerequisites
from logic.route_selector import classify_topic, select_route
from logic.prerequisite import generate_bridge_course
from logic.anchor import generate_clarifying_question
from logic.misconception import get_misconceptions
from logic.explainer import build_prompt
from logic.debugger import generate_debugger_questions

app = Flask(__name__)

@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        topic = request.args.get("topic")
        known = request.args.get("known", "")
        known_topics = known.split(",") if known else []
        explanation_length = "SHORT"
        user_choice = None
    else:
        data = request.json or {}
        topic = data.get("topic")
        known_topics = data.get("known_topics", [])
        explanation_length = data.get("length", "SHORT")
        user_choice = data.get("route")
        
    # --- Initialize all variables (CRITICAL) ---
    bridge_course = None
    prerequisite_result = None
    topic_type = None
    routes = None
    misconceptions = None
    explanation_prompt = None
    
    # --- Anchor & Clarification ---
    anchor_result = anchor_topic(topic)
    clarification = generate_clarifying_question(anchor_result)

    if clarification:
        return jsonify({
            "topic": topic,
            "anchor": anchor_result,
            "clarification": clarification
        })

    # 2. Prerequisite check (only AFTER clarification resolved)
    prerequisite_result = check_prerequisites(topic, known_topics)

    bridge_course = None
    if prerequisite_result["status"] == "MISSING_PREREQUISITES":
        bridge_course = generate_bridge_course(
            prerequisite_result["missing_topics"]
        )

    # 3. Route selection
    topic_type = classify_topic(topic)
    routes = select_route(
        topic_type,
        explanation_length=explanation_length,
        user_choice=user_choice
    )

    # 4. Misconceptions (only when actually teaching)
    misconceptions = get_misconceptions(topic)
    
    # --- Explanation prompt ---
    if bridge_course is None:
        explanation_prompt = build_prompt(
            topic=topic,
            route=routes[0],
            context=f"Class-level syllabus explanation for {topic}"
        )
        
    debug_mode = False
    if request.method == "POST":
        debug_mode = data.get("mode") == "DEBUGGER"
    elif request.method == "GET":
        debug_mode = request.args.get("mode") == "DEBUGGER"
        
    if debug_mode:
        debugger_output = generate_debugger_questions(topic)
        return jsonify({
            "topic": topic,
            "mode": "DEBUGGER",
            "debugger": debugger_output
        })



    return jsonify({
        "topic": topic,
        "anchor": anchor_result,
        "prerequisites": prerequisite_result,
        "bridge_course": bridge_course,
        "topic_type": topic_type,
        "routes_selected": routes,
        "misconceptions": misconceptions,
        "explanation_prompt": explanation_prompt
    })


if __name__ == "__main__":
    app.run(debug=True)

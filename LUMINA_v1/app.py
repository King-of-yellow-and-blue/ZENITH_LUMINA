# ---------- IMPORTS ----------
from flask import Flask, request, jsonify, render_template

from logic.anchor import anchor_topic, generate_clarifying_question
from logic.prerequisite import check_prerequisites, generate_bridge_course
from logic.route_selector import classify_topic, select_route
from logic.misconception import get_misconceptions
from logic.explainer import build_prompt
from logic.debugger import generate_debugger_questions

# ---------- CREATE APP (MUST BE BEFORE ROUTES) ----------
app = Flask(__name__)

# ---------- HOME ROUTE (UI) ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- MAIN API ROUTE ----------
@app.route("/ask", methods=["GET", "POST"])
def ask():
    # ----- Input handling -----
    if request.method == "GET":
        topic = request.args.get("topic")
        known = request.args.get("known", "")
        known_topics = known.split(",") if known else []
        explanation_length = "SHORT"
        user_choice = None
        debug_mode = request.args.get("mode") == "DEBUGGER"
        context_choice = request.args.get("context")
    else:
        data = request.json or {}
        topic = data.get("topic")
        known_topics = data.get("known_topics", [])
        explanation_length = data.get("length", "SHORT")
        user_choice = data.get("route")
        debug_mode = data.get("mode") == "DEBUGGER"

    # ----- Anchor -----
    anchor_result = anchor_topic(topic)

    # ----- Apply user-selected context (CRITICAL FIX) -----
    if context_choice and anchor_result["status"] == "AMBIGUOUS":
        try:
            choice_index = int(context_choice) - 1
            selected = anchor_result["options"][choice_index]

            anchor_result = {
                "status": "RESOLVED",
                "data": selected
            }
        except (IndexError, ValueError):
            pass

    # ----- Clarification (ONLY if still ambiguous) -----
    clarification = generate_clarifying_question(anchor_result)

    if clarification:
        return jsonify({
            "topic": topic,
            "anchor": anchor_result,
            "clarification": clarification
        })


    # ----- Debugger Mode -----
    if debug_mode:
        debugger_output = generate_debugger_questions(topic)
        return jsonify({
            "topic": topic,
            "mode": "DEBUGGER",
            "debugger": debugger_output
        })

    # ----- Prerequisites -----
    prerequisite_result = check_prerequisites(topic, known_topics)
    bridge_course = None

    if prerequisite_result["status"] == "MISSING_PREREQUISITES":
        bridge_course = generate_bridge_course(
            prerequisite_result["missing_topics"]
        )

    # ----- Route Selection -----
    topic_type = classify_topic(topic)
    routes = select_route(
        topic_type,
        explanation_length=explanation_length,
        user_choice=user_choice
    )

    # ----- Misconceptions -----
    misconceptions = get_misconceptions(topic)

    # ----- Explanation Prompt -----
    explanation_prompt = None
    if bridge_course is None:
        explanation_prompt = build_prompt(
            topic=topic,
            route=routes[0],
            context=f"Class-level syllabus explanation for {topic}"
        )

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

# ---------- START SERVER (LAST LINE) ----------
if __name__ == "__main__":
    app.run(debug=True)

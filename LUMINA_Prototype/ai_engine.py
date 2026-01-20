import time
import random
from rich.panel import Panel
from rich.console import Console

console = Console()

class LuminaEngine:
    def __init__(self):
        self.cognitive_load = "optimal" # Options: bored, optimal, overwhelmed
        
    def generate_explanation(self, topic, mode="default", user_state="neutral"):
        """
        Simulates the LLM generation. 
        In production, this calls OpenAI/Gemini API.
        """
        
        # Feature #10: Sentiment Adjustment
        prefix = ""
        if user_state == "frustrated":
            prefix = "[It's okay. Let's take a deep breath and try a simpler angle.]\n"

        # Feature #5: Generative Analogy-to-Visual
        visual_prompt = f"[STABLE DIFFUSION GENERATION]: Diagram of '{topic}' using real-world objects."
        
        explanations = {
            "Gravity": f"{prefix}Gravity is like an invisible rubber band pulling everything to the center.",
            "Integration": f"{prefix}Integration is like adding up infinite tiny slices of a cake to find the whole volume.",
            "Trigonometry": f"{prefix}Trig is just the math of triangles and circles dancing together."
        }
        
        content = explanations.get(topic, "Simulating complex neural generation...")
        
        return content, visual_prompt

    def run_socratic_debugger(self, topic):
        """Feature #6: The Socratic Debugger"""
        console.print(Panel(f"[bold magenta]MODE SWITCH: Socratic Debugger ({topic})[/bold magenta]", title="LUMINA CORE"))
        questions = [
            f"Explain to me: What is the fundamental cause of {topic}?",
            "Why does that happen? digging deeper...",
            "Can you give me a counter-example where this logic fails?",
            "So, if I changed X, how would {topic} change?"
        ]
        
        for q in questions:
            console.print(f"[bold cyan]LUMINA:[/bold cyan] {q}")
            user_ans = input("YOU: ")
            time.sleep(1) # Simulating "Thinking"
            console.print("[italic dim]Analyzing logic gaps...[/italic dim]\n")
        
        return True # Return True if passed

    def run_feynman_simulator(self, topic):
        """Feature #2: The Feynman Simulator (Active Recall)"""
        console.print(Panel(f"[bold yellow]MODE SWITCH: Feynman Simulator[/bold yellow]", title="TEACH ME"))
        console.print(f"[bold cyan]LUMINA:[/bold cyan] I am a 5-year-old. Teach me {topic}.")
        
        user_explanation = input("YOU (Teacher): ")
        
        # Feature #3: Cognitive Load Balancer (Simulated analysis)
        if len(user_explanation) < 10:
            console.print("[red]Gap Detected:[/red] Your explanation was too brief. You might have missing foundations.")
            return False
        else:
            console.print("[green]Analysis:[/green] Great analogy! You simplified the jargon well.")
            return True
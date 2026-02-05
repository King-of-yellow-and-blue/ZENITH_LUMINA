import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.markdown import Markdown

# Import our modules
from knowledge_graph import KnowledgeGraphEngine
from user_profile import UserProfile
from ai_engine import LuminaEngine

console = Console()
kg = KnowledgeGraphEngine()
ai = LuminaEngine()

# Initialize a Mock User
user = UserProfile("Student_01")
# Let's say user already knows Algebra for this demo
user.mark_mastery("Algebra") 

def main():
    console.clear()
    console.print(Panel.fit("[bold white]LUMINA[/bold white]\n[dim]Learning, Understanding & Mastery through Intelligent Neural Architecture[/dim]", style="bold blue"))
    
    while True:
        console.print("\n[bold]What topic do you want to conquer today?[/bold] (or type 'exit')")
        topic_input = input(">> ").strip().title()
        
        if topic_input.lower() == 'exit':
            break

        # Feature #1: Dynamic Syllabus Mapping
        # Check if topic exists in our mock DB
        misconceptions = kg.get_misconceptions(topic_input)
        
        # Feature #4: Misconception Hunter
        if misconceptions:
            console.print(Panel(f"[bold red]WARNING - COMMON TRAPS:[/bold red]\nBefore we start, avoid these errors: {', '.join(misconceptions)}", style="red"))

        # Feature #2: Foundation Guardrail
        is_ready, missing = kg.check_readiness(topic_input, user.mastered_topics)
        
        if not is_ready:
            console.print(Panel(f"[bold orange1]FOUNDATION ALERT[/bold orange1]\nYou are missing: {missing}", style="yellow"))
            choice = input("Generate 5-min Bridge Course? (y/n): ")
            if choice.lower() == 'y':
                console.print(f"[green]Generating micro-module for {missing[0]}...[/green]")
                time.sleep(1.5)
                # Recursively learn the missing topic
                # For prototype, we just grant it
                user.mark_mastery(missing[0])
                console.print("Bridge Course Complete! Returning to main topic...")
            else:
                continue

        # Main Learning Loop
        sentiment = user.analyze_sentiment(topic_input) # Analyzing initial prompt tone
        explanation, visual_prompt = ai.generate_explanation(topic_input, user_state=sentiment)
        
        console.print(Markdown(f"## {topic_input}"))
        console.print(explanation)
        console.print(f"[italic dim]{visual_prompt}[/italic dim]") # Feature #5
        
        # Interactive Modes
        console.print("\n[bold]Choose Interaction Mode:[/bold]")
        console.print("1. Standard Learning")
        console.print("2. Socratic Debugger (Deep Thinking)")
        console.print("3. Feynman Simulator (Test Mastery)")
        
        mode = input(">> ")
        
        if mode == "2":
            passed = ai.run_socratic_debugger(topic_input)
            if passed: user.mark_mastery(topic_input)
            
        elif mode == "3":
            passed = ai.run_feynman_simulator(topic_input)
            if passed: user.mark_mastery(topic_input)

if __name__ == "__main__":
    main()
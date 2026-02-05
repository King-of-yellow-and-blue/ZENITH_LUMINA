import time
import sys

# --- SIMULATED KNOWLEDGE GRAPH (Replaces NetworkX) ---
class SimpleKnowledgeGraph:
    def __init__(self):
        # Format: "Topic": ["Prerequisite1", "Prerequisite2"]
        self.prerequisites = {
            "Integration": ["Trigonometry", "Limits"],
            "Limits": ["Algebra"],
            "Trigonometry": ["Algebra"],
            "Gravity": ["Kinematics"],
            "Kinematics": ["Algebra"]
        }
        
        # Format: "Topic": ["Misconception1", "Misconception2"]
        self.misconceptions = {
            "Integration": ["Confusing integral with derivative", "Forgetting +C"],
            "Gravity": ["Mass vs Weight", "Vacuum fall"],
            "Algebra": ["Variable confusion", "Sign errors"]
        }

    def get_missing_prereqs(self, topic, mastered_topics):
        required = self.prerequisites.get(topic, [])
        missing = [req for req in required if req not in mastered_topics]
        return missing

    def get_misconceptions(self, topic):
        return self.misconceptions.get(topic, [])

# --- USER PROFILE ---
class SimpleUserProfile:
    def __init__(self):
        self.mastered_topics = ["Algebra"] # User starts knowing Algebra
    
    def mark_mastery(self, topic):
        if topic not in self.mastered_topics:
            self.mastered_topics.append(topic)
            print(f"\n[SYSTEM] ⭐ MASTERY UNLOCKED: '{topic}' added to your Skill Tree!")

# --- AI ENGINE ---
class SimpleAIEngine:
    def generate_explanation(self, topic, sentiment="neutral"):
        prefix = ""
        if sentiment == "frustrated":
            prefix = "(Gentle Tone) It's okay, let's take a breath. "
            
        print(f"\n" + "="*50)
        print(f"LUMINA EXPLANATION: {topic.upper()}")
        print("="*50)
        
        if topic == "Gravity":
            print(f"{prefix}Gravity is like an invisible rubber band pulling everything to the center.")
            print("[VISUAL]: *Generates diagram of bent space-time fabric*")
        elif topic == "Integration":
            print(f"{prefix}Integration is like adding up infinite tiny slices of a cake to find the whole volume.")
            print("[VISUAL]: *Generates animation of slicing a 3D shape*")
        else:
            print(f"{prefix}Here is the explanation for {topic} using our cognitive engine...")
            print("[VISUAL]: *Generates relevant schema*")
            
    def run_socratic_mode(self, topic):
        print(f"\n[MODE SWITCH]: SOCRATIC DEBUGGER ({topic})")
        print("-" * 40)
        print("LUMINA: Explain to me, what is the fundamental cause of this?")
        input("YOU: ")
        print("LUMINA: Interesting. But what if I told you that was only half true?")
        input("YOU: ")
        print("LUMINA: Good logic. You passed.")
        return True

# --- MAIN CONTROLLER ---
def main():
    kg = SimpleKnowledgeGraph()
    user = SimpleUserProfile()
    ai = SimpleAIEngine()

    print("\n" + "#"*40)
    print("      WELCOME TO LUMINA (LITE VERSION)")
    print("#"*40)

    while True:
        print(f"\n[CURRENT SKILLS]: {', '.join(user.mastered_topics)}")
        topic = input("\nWhat topic do you want to learn? (or type 'exit'): ").strip().title()

        if topic.lower() == 'exit':
            break

        # 1. CHECK MISCONCEPTIONS
        misc = kg.get_misconceptions(topic)
        if misc:
            print(f"\n[WARNING] Common Traps detected: {', '.join(misc)}")

        # 2. CHECK PREREQUISITES
        missing = kg.get_missing_prereqs(topic, user.mastered_topics)
        
        if missing:
            print(f"\n[ALERT] You are missing foundations: {', '.join(missing)}")
            print("Generating 5-minute Bridge Course...")
            time.sleep(1.5)
            # Auto-teach the first missing topic
            print(f"\n[BRIDGE COURSE] Rapidly teaching {missing[0]}...")
            user.mark_mastery(missing[0])
            print("Bridge Course Complete! Returning to main topic...")
        
        # 3. SENTIMENT ANALYSIS (Simple Keyword Check)
        sentiment = "neutral"
        if "stupid" in topic.lower() or "hard" in topic.lower():
            sentiment = "frustrated"

        # 4. GENERATE CONTENT
        ai.generate_explanation(topic, sentiment)
        
        # 5. MODE SELECTION
        print("\nOptions: [1] Next Topic  [2] Socratic Mode")
        choice = input(">> ")
        if choice == "2":
            if ai.run_socratic_mode(topic):
                user.mark_mastery(topic)

if __name__ == "__main__":
    main()
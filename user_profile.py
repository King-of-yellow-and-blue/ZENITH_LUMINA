import datetime
from rich.console import Console

console = Console()

class UserProfile:
    def __init__(self, username):
        self.username = username
        self.mastered_topics = [] # List of strings
        self.review_schedule = {} # Dictionary: {topic: next_review_date}
        self.sentiment_history = [] # For Feature #10

    def mark_mastery(self, topic):
        if topic not in self.mastered_topics:
            self.mastered_topics.append(topic)
            self._schedule_srs(topic)
            console.print(f"[bold green]🌟 MASTERY UNLOCKED: {topic} added to your Skill Tree![/bold green]")

    def _schedule_srs(self, topic):
        """Feature #7: Automated Spaced Repetition Scheduler"""
        # Simple algorithm: Review in 1 day, then 3 days...
        next_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.review_schedule[topic] = next_date
        # In a real app, this would push a notification.

    def get_skill_tree(self):
        """Feature #9: Gamified Mastery Trees (Data view)"""
        return self.mastered_topics

    def analyze_sentiment(self, user_input):
        """Feature #10: Sentiment-Aware Responses (Simulated)"""
        # Simple keyword detection for prototype
        frustrated_words = ["stupid", "don't get", "hard", "hate", "impossible"]
        for word in frustrated_words:
            if word in user_input.lower():
                return "frustrated"
        return "neutral"
import networkx as nx

class KnowledgeGraphEngine:
    def __init__(self):
        # We use a directed graph to model dependencies (Prerequisites)
        self.graph = nx.DiGraph()
        self._initialize_demo_data()

    def _initialize_demo_data(self):
        """
        Populates the graph with demo data.
        In a real production app, this would pull from a Vector Database (Neo4j/Pinecone).
        """
        # Node attributes: 'misconceptions' (Feature 4), 'type'
        
        # Topic: Math Foundation
        self.graph.add_node("Algebra", type="foundation", misconceptions=["Variable confusion", "Sign errors"])
        self.graph.add_node("Trigonometry", type="foundation", misconceptions=["Sin/Cos confusion", "Unit circle errors"])
        
        # Topic: Calculus
        self.graph.add_node("Limits", type="concept", misconceptions=["Infinity paradoxes"])
        self.graph.add_node("Integration", type="advanced", misconceptions=["Confusing integral with derivative"])
        
        # Topic: Physics
        self.graph.add_node("Kinematics", type="foundation", misconceptions=["Velocity vs Acceleration"])
        self.graph.add_node("Gravity", type="concept", misconceptions=["Mass vs Weight", "Vacuum fall"])
        
        # EDGES: Define Prerequisites (The 'Foundation Guardrail')
        self.graph.add_edge("Algebra", "Limits")
        self.graph.add_edge("Trigonometry", "Integration")
        self.graph.add_edge("Limits", "Integration")
        self.graph.add_edge("Algebra", "Kinematics")
        self.graph.add_edge("Kinematics", "Gravity")

    def get_prerequisites(self, topic):
        """Returns immediate prerequisites for a topic."""
        if topic not in self.graph:
            return []
        return list(self.graph.predecessors(topic))

    def get_misconceptions(self, topic):
        """Feature #4: The Misconception Hunter"""
        if topic in self.graph:
            return self.graph.nodes[topic].get('misconceptions', [])
        return []

    def check_readiness(self, topic, user_mastered_topics):
        """
        Feature #2: Foundation Guardrail Logic.
        Returns: (is_ready: bool, missing_topics: list)
        """
        prereqs = self.get_prerequisites(topic)
        missing = [p for p in prereqs if p not in user_mastered_topics]
        return (len(missing) == 0, missing)
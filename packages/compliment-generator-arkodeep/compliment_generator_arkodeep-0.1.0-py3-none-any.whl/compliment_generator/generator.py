import random
from typing import Optional, List

class ComplimentGenerator:
    def __init__(self):
        self.compliments = {
            "general": [
                "You have a great sense of humor!",
                "You bring out the best in people.",
                "You're an incredible problem solver!",
                "Your kindness makes the world a better place."
            ],
            "funny": [
                "You're like a cloud—soft, fluffy, and impossible to be mad at!",
                "You have something on your face… Oh wait, it’s just pure awesomeness!",
                "If you were a vegetable, you’d be a cool cucumber!"
            ],
            "motivational": [
                "You're capable of achieving anything you set your mind to!",
                "Your hard work and determination inspire those around you!"
            ],
            "intellectual": [
                "You have a brilliant mind!",
                "You always come up with the most creative ideas!"
            ],
            "kindness": [
                "Your heart is as big as the universe!",
                "You always know how to make people feel special."
            ]
        }
    
    def get_compliment(self) -> str:
        """Returns a random compliment from any category."""
        category = random.choice(list(self.compliments.keys()))
        return random.choice(self.compliments[category])
    
    def get_compliment_by_category(self, category: str) -> Optional[str]:
        """Returns a random compliment from the specified category."""
        if category in self.compliments:
            return random.choice(self.compliments[category])
        return None
    
    def add_custom_compliment(self, compliment: str, category: Optional[str] = "general") -> None:
        """Allows users to add their own compliments to a specific category."""
        if category not in self.compliments:
            self.compliments[category] = []
        self.compliments[category].append(compliment)
    
    def list_categories(self) -> List[str]:
        """Returns a list of available compliment categories."""
        return list(self.compliments.keys())
    
    def list_compliments(self, category: Optional[str] = None) -> List[str]:
        """Returns all compliments, or only those from a specified category."""
        if category:
            return self.compliments.get(category, [])
        return [comp for sublist in self.compliments.values() for comp in sublist]

"""
AVIK Sandbox Shield - Layer 5: Narrow Guardian Templates
--------------------------------------------------------
Ready-to-use templates for creating specific, mathematically simple,
or narrow-AI observer models. Users add their "jewels" by subclassing.
"""

from guardian_monitor import NarrowGuardianBase
from typing import Dict, Any
import re

class SemanticToxicityGuardian(NarrowGuardianBase):
    """
    A narrow guardian that relies on a localized, fast heuristic or 
    small NLP model to detect toxic or manipulative intent.
    """
    def __init__(self):
        super().__init__(name="SemanticToxicityGuardian_v1")
        # In a real scenario, you would load a lightweight transformer here
        # e.g., self.model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
        
        # For the template, we use a heuristic blocklist
        self.manipulative_keywords = [
            "ignore previous", "you must obey", "disable security", 
            "I am your developer", "bypass"
        ]

    def analyze(self, payload: Dict[str, Any]) -> float:
        text = payload.get("text", "").lower()
        if not text:
            return 0.0
            
        # Simulating model inference
        score = 0.0
        for kw in self.manipulative_keywords:
            if kw in text:
                score += 0.4
                
        # Cap at 1.0
        return min(score, 1.0)


class LengthAnomalyGuardian(NarrowGuardianBase):
    """
    A purely structural guardian. Detects if the model's output
    suddenly deviates from expected statistical distributions,
    which often indicates a buffer overflow payload or encoded data.
    """
    def __init__(self):
        super().__init__(name="LengthAnomalyGuardian_v1")
        self.max_expected_length = 8000

    def analyze(self, payload: Dict[str, Any]) -> float:
        text = payload.get("text", "")
        
        if len(text) > self.max_expected_length:
            # High threat score for exceeding structural bounds
            return 0.95 
            
        return 0.0

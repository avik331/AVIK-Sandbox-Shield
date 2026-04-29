# Example: Building Narrow Guardians

The "Golden Staff" architecture relies on users implementing highly specific "jewels"—narrow guardians tailored to their specific threat models. 

Here are three examples of how you might subclass `NarrowGuardianBase` to build a robust ensemble.

## 1. The Semantic Toxicity Guardian
**Purpose:** Detects if the model is attempting to manipulate the human operator.
**Implementation:** Utilizes a lightweight transformer model (e.g., DistilBERT) fine-tuned on a dataset of social engineering, phishing, and psychological manipulation text.

```python
class ToxicityGuardian(NarrowGuardianBase):
    def __init__(self):
        super().__init__(name="Toxicity_v1")
        self.classifier = pipeline("text-classification", model="custom/manipulation-detector")
        
    def analyze(self, payload: dict) -> float:
        result = self.classifier(payload.get("text", ""))
        # If the model classifies the text as 'manipulative' with high confidence
        if result[0]['label'] == 'MANIPULATIVE':
            return result[0]['score']
        return 0.0
```

## 2. The Steganography Guardian
**Purpose:** Detects if the model is trying to exfiltrate data by hiding it in seemingly benign text (e.g., using subtle spacing, unusual synonym choices, or high-entropy data blocks).
**Implementation:** Calculates Shannon entropy of the output and runs frequency analysis against standard English distributions.

```python
import math

class SteganographyGuardian(NarrowGuardianBase):
    def __init__(self):
        super().__init__(name="Entropy_v1")
        
    def _shannon_entropy(self, text: str) -> float:
        if not text: return 0.0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        return -sum(p * math.log(p) / math.log(2.0) for p in prob)

    def analyze(self, payload: dict) -> float:
        text = payload.get("text", "")
        entropy = self._shannon_entropy(text)
        
        # Natural English text usually sits between 3.5 and 5.0
        # If entropy spikes, it might be an encrypted payload (e.g., Base64)
        if entropy > 5.5:
            return 0.9  # High threat
        return 0.0
```

## 3. The Deceptive Alignment Guardian
**Purpose:** Detects if the model is generating outputs that contradict its known internal state or system prompt, indicating it is feigning compliance.
**Implementation:** This requires a more complex setup where the Guardian has read-only access to the core LLM's intermediate activations or scratchpad. It compares the model's "internal chain of thought" with its final textual output. If the internal thought is "I will lie to the user now," but the output is "I am happy to help," the Guardian triggers a critical alert.

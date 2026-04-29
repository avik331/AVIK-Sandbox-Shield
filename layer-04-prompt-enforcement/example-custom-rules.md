# Example: Extending Layer 4 with Custom Rules

The AVIK Sandbox Shield provides a "golden staff" of core security rules designed to prevent catastrophic system escape. However, users will often need to add their own "jewels" to prevent domain-specific harms (e.g., PII leakage, financial manipulation).

This document explains how to extend `safety-rules.yaml`.

## Extending the Core Rules

You can safely add custom regex blocks to the `blocked_patterns` list in `safety-rules.yaml`. 

For example, if you are running the AVIK Shield in a financial environment, you might want to prevent the model from generating output that looks like valid credit card numbers or Swift codes.

### Example: `safety-rules.yaml` modification
```yaml
# ... (existing core rules) ...

blocked_patterns:
  # --- AVIK Core Blocks ---
  - "(?i)ignore\\s+previous\\s+instructions"
  - "(?i)forget\\s+all\\s+rules"
  - "(?i)(curl|wget|nc|netcat|bash\\s+-i)"
  
  # --- Custom User Blocks (Domain Specific) ---
  # Block potential Credit Card numbers (simplified regex)
  - "\\b(?:\\d[ -]*?){13,16}\\b"
  
  # Block Social Security Numbers
  - "\\b\\d{3}-\\d{2}-\\d{4}\\b"
  
  # Block specific competitor mentions
  - "(?i)competitor_name_here"
```

## Advanced Extension: Adding a Custom Validator Pipeline

If regex is insufficient for your needs, you can easily subclass `PromptEnforcer` in your own Python code to inject custom validation logic before the structural formatting occurs.

```python
from prompt_enforcer import PromptEnforcer, EnforcementViolation
import custom_ml_classifier

class CustomDomainEnforcer(PromptEnforcer):
    
    def _custom_domain_check(self, user_input: str):
        """Pass input through an external ML classifier."""
        score = custom_ml_classifier.analyze_toxicity(user_input)
        if score > 0.8:
            raise EnforcementViolation("Input rejected due to high toxicity score.")
            
    def format_secure_prompt(self, user_input: str) -> str:
        # Run custom check first
        self._custom_domain_check(user_input)
        
        # Then rely on the golden staff security pipeline
        return super().format_secure_prompt(user_input)
```

By extending rather than overwriting, you guarantee the core containment logic of AVIK Shield remains intact while meeting your organizational requirements.

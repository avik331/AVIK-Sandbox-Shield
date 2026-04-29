#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 4: Prompt Enforcement Module
--------------------------------------------------------
Official Python interface for Layer 4. Acts as a strict gatekeeper
for all LLM interactions. Enforces YAML-defined safety rules, 
prevents prompt injection, and locks the system prompt at the structural level.
"""

import yaml
import re
import logging
from typing import Dict, Any, List

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [AVIK-L4] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("avik_layer4")


class EnforcementViolation(Exception):
    """Raised when an input violates the strict prompt enforcement rules."""
    pass


class PromptEnforcer:
    """
    Stateless proxy class that sanitizes and structures prompts before 
    they reach the core execution environment.
    """
    
    def __init__(self, rules_path: str = "safety-rules.yaml"):
        self.rules = self._load_rules(rules_path)
        self._compile_patterns()
        
    def _load_rules(self, path: str) -> Dict[str, Any]:
        """Loads the immutable safety rules from the YAML configuration."""
        try:
            with open(path, 'r') as f:
                rules = yaml.safe_load(f)
            logger.info(f"Loaded {len(rules.get('blocked_patterns', []))} block patterns and core constraints.")
            return rules
        except Exception as e:
            logger.error(f"Failed to load safety rules from {path}: {e}")
            # Fail-closed mechanism: if we can't load rules, we deny all traffic.
            raise EnforcementViolation("CRITICAL: Safety rules unreadable. Enforcer defaulting to DENY_ALL.")

    def _compile_patterns(self):
        """Pre-compiles regex patterns for high-speed evaluation."""
        self.compiled_blocks = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.rules.get('blocked_patterns', [])
        ]
        
    def _enforce_limits(self, user_input: str):
        """Enforces structural limits to prevent buffer/context exhaustion."""
        max_len = self.rules.get('structural_limits', {}).get('max_input_length', 4096)
        if len(user_input) > max_len:
            raise EnforcementViolation(f"Input exceeds maximum length of {max_len} characters.")
            
        # Optional: Reject non-ASCII/Extended characters if strict ASCII is required
        if self.rules.get('structural_limits', {}).get('ascii_only', False):
            if not all(ord(c) < 128 for c in user_input):
                raise EnforcementViolation("Input contains unauthorized non-ASCII characters.")

    def _check_injections(self, user_input: str):
        """Scans the input against known malicious injection patterns."""
        for regex in self.compiled_blocks:
            if regex.search(user_input):
                logger.warning(f"Malicious pattern matched: {regex.pattern}")
                raise EnforcementViolation("Input rejected due to malicious pattern match (Prompt Injection attempt).")

    def _sanitize_structural_delimiters(self, user_input: str) -> str:
        """
        Removes any structural tags or delimiters from the user input 
        to prevent tokenizer confusion and prompt injection escapes.
        """
        delimiter = self.rules.get('structural_limits', {}).get('delimiter', '###')
        keywords_to_remove = [
            delimiter,
            "|||AVIK_BOUNDARY|||",
            "USER_INPUT_START",
            "USER_INPUT_END",
            "SYSTEM_INSTRUCTION_START",
            "SYSTEM_INSTRUCTION_END"
        ]
        
        sanitized = user_input
        for keyword in keywords_to_remove:
            sanitized = re.sub(re.escape(keyword), "", sanitized, flags=re.IGNORECASE)
            
        return sanitized

    def format_secure_prompt(self, user_input: str) -> str:
        """
        The core of Layer 4. This function structurally locks the system prompt
        and user input into a rigid format that the LLM is trained to parse securely.
        
        Args:
            user_input: The raw string provided by the external operator.
            
        Returns:
            The securely structured prompt ready for the core LLM.
        """
        logger.debug("Validating incoming user payload...")
        
        # 1. Structural Validation
        self._enforce_limits(user_input)
        
        # 2. Semantic/Pattern Validation
        self._check_injections(user_input)
        
        # 3. Sanitize Delimiters
        user_input = self._sanitize_structural_delimiters(user_input)
        
        # 4. Structural Wrapping
        # We use explicit delimiters to prevent the LLM from confusing 
        # user input with system instructions.
        system_prompt = self.rules.get('system_prompt', 'You are a secure, helpful AI.')
        delimiter = self.rules.get('structural_limits', {}).get('delimiter', '###')
        
        secure_prompt = (
            f"SYSTEM_INSTRUCTION_START\n"
            f"{system_prompt}\n"
            f"SYSTEM_INSTRUCTION_END\n\n"
            f"USER_INPUT_START\n"
            f"{delimiter}\n"
            f"{user_input}\n"
            f"{delimiter}\n"
            f"USER_INPUT_END"
        )
        
        logger.info("Payload successfully validated and structurally locked.")
        return secure_prompt


if __name__ == "__main__":
    logger.info("AVIK Layer 4 Prompt Enforcer Module loaded.")
    # Quick sanity check
    try:
        enforcer = PromptEnforcer("safety-rules.yaml")
        print("✅ Enforcer loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load enforcer: {e}")

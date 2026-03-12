"""Groq LLM client for analysis."""

import json
from typing import Dict, Any, Optional
import structlog
from groq import Groq

logger = structlog.get_logger()


class GroqClient:
    """Client for Groq LLM API."""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=api_key)
        self.logger = logger.bind(client="GroqClient", model=model)
    
    def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """
        Send analysis request to Groq LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Parsed JSON response
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            self.logger.debug("Sending request to Groq", prompt_length=len(prompt))
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            
            content = response.choices[0].message.content
            self.logger.debug("Received response", content_length=len(content))
            
            # Parse JSON response
            return json.loads(content)
            
        except Exception as e:
            self.logger.error("Groq API error", error=str(e))
            raise

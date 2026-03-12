"""Theme extraction using Groq LLM."""

import json
from typing import List, Dict, Any
import structlog

from .groq_client import GroqClient

logger = structlog.get_logger()


class ThemeAnalyzer:
    """Analyzes reviews to extract key themes."""
    
    SYSTEM_PROMPT = """You are an expert product analyst specializing in fintech apps.
Your task is to analyze user reviews and identify the main themes.

Guidelines:
- Focus on areas like: onboarding, KYC, payments, statements, withdrawals, UI/UX, performance, customer support
- Group similar issues together
- Consider the sentiment and frequency of mentions
- Be specific but concise

Respond ONLY in JSON format."""

    def __init__(self, groq_client: GroqClient, max_themes: int = 5):
        self.groq_client = groq_client
        self.max_themes = max_themes
        self.logger = logger.bind(analyzer="ThemeAnalyzer")
    
    def analyze(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract themes from reviews.
        
        Args:
            reviews: List of review dictionaries
            
        Returns:
            List of theme dictionaries with name, description, review_count, sentiment
        """
        # Prepare review text for analysis
        review_texts = []
        for i, review in enumerate(reviews[:100], 1):  # Limit to 100 reviews for API
            text = review.get("text", "")
            rating = review.get("rating", 0)
            review_texts.append(f"{i}. [Rating: {rating}/5] {text[:300]}")
        
        reviews_block = "\n".join(review_texts)
        
        prompt = f"""Analyze the following {len(review_texts)} user reviews from the Groww investment app and identify up to {self.max_themes} major themes.

Reviews:
{reviews_block}

Provide your analysis in the following JSON format:
{{
  "themes": [
    {{
      "name": "Theme Name (e.g., 'Withdrawal Issues', 'App Performance')",
      "description": "Brief description of what this theme covers (1-2 sentences)",
      "review_count": number of reviews mentioning this theme,
      "sentiment": "negative|mixed|positive",
      "severity": "high|medium|low"
    }}
  ]
}}

Return ONLY the JSON, no other text."""
        
        try:
            self.logger.info("Analyzing themes", review_count=len(reviews))
            
            response = self.groq_client.analyze(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.3,
                max_tokens=1500,
            )
            
            themes = response.get("themes", [])
            
            # Limit to max_themes
            themes = themes[:self.max_themes]
            
            self.logger.info("Theme analysis complete", theme_count=len(themes))
            
            return themes
            
        except Exception as e:
            self.logger.error("Theme analysis failed", error=str(e))
            # Return empty list on failure
            return []

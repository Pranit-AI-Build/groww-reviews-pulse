"""Quote extraction using Groq LLM."""

from typing import List, Dict, Any
import structlog

from .groq_client import GroqClient

logger = structlog.get_logger()


class QuoteExtractor:
    """Extracts representative user quotes for themes."""
    
    SYSTEM_PROMPT = """You are an expert at identifying impactful user quotes.
Your task is to select quotes that best represent each theme.

Guidelines:
- Select quotes that are concise and impactful
- Avoid quotes with PII (names, emails, phone numbers)
- Choose quotes that clearly illustrate the theme
- Prefer quotes that explain the "why" behind the sentiment

Respond ONLY in JSON format."""

    def __init__(self, groq_client: GroqClient, max_quotes: int = 3):
        self.groq_client = groq_client
        self.max_quotes = max_quotes
        self.logger = logger.bind(analyzer="QuoteExtractor")
    
    def extract(
        self,
        reviews: List[Dict[str, Any]],
        themes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract representative quotes for each theme.
        
        Args:
            reviews: List of review dictionaries
            themes: List of theme dictionaries
            
        Returns:
            List of quote dictionaries with text, theme, and context
        """
        quotes = []
        
        for theme in themes:
            theme_name = theme.get("name", "")
            theme_quotes = self._extract_for_theme(reviews, theme_name)
            quotes.extend(theme_quotes)
        
        # Limit total quotes
        return quotes[:self.max_quotes]
    
    def _extract_for_theme(
        self,
        reviews: List[Dict[str, Any]],
        theme_name: str
    ) -> List[Dict[str, Any]]:
        """Extract quotes for a specific theme."""
        
        # Prepare review text
        review_texts = []
        for i, review in enumerate(reviews[:50], 1):
            text = review.get("text", "")
            review_texts.append(f"{i}. {text[:400]}")
        
        reviews_block = "\n".join(review_texts)
        
        prompt = f"""From the following reviews, select up to 2 most impactful quotes that represent the theme: "{theme_name}"

Reviews:
{reviews_block}

Provide your selection in the following JSON format:
{{
  "quotes": [
    {{
      "text": "The exact quote from the review (keep it concise, max 150 characters)",
      "theme": "{theme_name}",
      "context": "Brief context about what this quote illustrates"
    }}
  ]
}}

Requirements:
- Select quotes that are specific and impactful
- Avoid generic complaints like "bad app" or "don't use"
- Prefer quotes that explain the specific problem
- Return ONLY the JSON, no other text."""
        
        try:
            self.logger.info("Extracting quotes", theme=theme_name)
            
            response = self.groq_client.analyze(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.3,
                max_tokens=800,
            )
            
            theme_quotes = response.get("quotes", [])
            
            self.logger.info("Quote extraction complete", 
                           theme=theme_name, 
                           quote_count=len(theme_quotes))
            
            return theme_quotes
            
        except Exception as e:
            self.logger.error("Quote extraction failed", 
                            theme=theme_name, 
                            error=str(e))
            return []

"""Action idea generation using Groq LLM."""

from typing import List, Dict, Any
import structlog

from .groq_client import GroqClient

logger = structlog.get_logger()


class ActionGenerator:
    """Generates actionable recommendations based on themes and reviews."""
    
    SYSTEM_PROMPT = """You are a senior product manager specializing in fintech apps.
Your task is to generate actionable recommendations based on user feedback analysis.

Guidelines:
- Focus on practical, implementable actions
- Prioritize by impact and feasibility
- Be specific about what needs to be done
- Consider quick wins vs long-term improvements

Respond ONLY in JSON format."""

    def __init__(self, groq_client: GroqClient, max_actions: int = 3):
        self.groq_client = groq_client
        self.max_actions = max_actions
        self.logger = logger.bind(analyzer="ActionGenerator")
    
    def generate(
        self,
        themes: List[Dict[str, Any]],
        quotes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate action ideas based on themes and quotes.
        
        Args:
            themes: List of theme dictionaries
            quotes: List of quote dictionaries
            
        Returns:
            List of action dictionaries
        """
        # Prepare themes summary
        themes_summary = []
        for theme in themes:
            themes_summary.append(
                f"- {theme.get('name', '')}: {theme.get('description', '')} "
                f"({theme.get('review_count', 0)} reviews, {theme.get('sentiment', '')} sentiment)"
            )
        
        themes_block = "\n".join(themes_summary)
        
        # Prepare quotes summary
        quotes_summary = []
        for quote in quotes:
            quotes_summary.append(f"- [{quote.get('theme', '')}] {quote.get('text', '')}")
        
        quotes_block = "\n".join(quotes_summary)
        
        prompt = f"""Based on the following analysis of user reviews, generate {self.max_actions} actionable recommendations.

TOP THEMES:
{themes_block}

USER QUOTES:
{quotes_block}

Provide your recommendations in the following JSON format:
{{
  "actions": [
    {{
      "title": "Short action title (5-7 words)",
      "description": "Detailed explanation of what to do and why (2-3 sentences)",
      "priority": "high|medium|low",
      "effort": "small|medium|large",
      "impact": "high|medium|low",
      "related_theme": "Name of the theme this addresses"
    }}
  ]
}}

Requirements:
- Actions should be specific and implementable
- Prioritize by user impact
- Include mix of quick wins and strategic improvements
- Return ONLY the JSON, no other text."""
        
        try:
            self.logger.info("Generating action ideas", 
                           theme_count=len(themes), 
                           quote_count=len(quotes))
            
            response = self.groq_client.analyze(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.4,
                max_tokens=1200,
            )
            
            actions = response.get("actions", [])
            
            # Limit to max_actions
            actions = actions[:self.max_actions]
            
            self.logger.info("Action generation complete", action_count=len(actions))
            
            return actions
            
        except Exception as e:
            self.logger.error("Action generation failed", error=str(e))
            return []

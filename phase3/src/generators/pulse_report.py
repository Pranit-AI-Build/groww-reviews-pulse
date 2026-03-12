"""Weekly pulse report generator."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger()


class PulseReportGenerator:
    """Generates the weekly pulse report."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.logger = logger.bind(generator="PulseReportGenerator")
    
    def generate(
        self,
        themes: List[Dict[str, Any]],
        quotes: List[Dict[str, Any]],
        actions: List[Dict[str, Any]],
        review_count: int,
        date_range: tuple,
    ) -> Dict[str, Any]:
        """
        Generate the weekly pulse report.
        
        Args:
            themes: List of theme dictionaries
            quotes: List of quote dictionaries
            actions: List of action dictionaries
            review_count: Total number of reviews analyzed
            date_range: (start_date, end_date) tuple
            
        Returns:
            Report data dictionary
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "week_range": f"{date_range[0]} to {date_range[1]}",
            "total_reviews": review_count,
            "themes": themes[:3],  # Top 3 themes
            "quotes": quotes[:3],  # 3 quotes
            "actions": actions[:3],  # 3 actions
        }
        
        # Save JSON
        json_path = self.output_dir / "weekly_pulse.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Generate Markdown
        markdown = self._generate_markdown(report)
        md_path = self.output_dir / "weekly_pulse.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        # Generate text for email
        text = self._generate_text(report)
        txt_path = self.output_dir / "weekly_pulse.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        self.logger.info("Report generated", 
                        json_path=str(json_path),
                        md_path=str(md_path),
                        txt_path=str(txt_path))
        
        return report
    
    def _generate_markdown(self, report: Dict[str, Any]) -> str:
        """Generate Markdown format report."""
        lines = [
            "# Weekly Pulse - Groww Reviews",
            f"",
            f"**Week:** {report['week_range']}",
            f"**Reviews Analyzed:** {report['total_reviews']}",
            f"",
            "---",
            f"",
            "## Top 3 Themes",
            f"",
        ]
        
        for i, theme in enumerate(report['themes'], 1):
            lines.append(f"{i}. **{theme['name']}** - {theme.get('review_count', 0)} mentions")
            lines.append(f"   - {theme.get('description', '')}")
            lines.append(f"   - Sentiment: {theme.get('sentiment', 'unknown')} | Severity: {theme.get('severity', 'unknown')}")
            lines.append("")
        
        lines.extend([
            "## User Voices",
            "",
        ])
        
        for quote in report['quotes']:
            lines.append(f"> \"{quote.get('text', '')}\"")
            lines.append(f"> — *{quote.get('theme', '')}*")
            lines.append("")
        
        lines.extend([
            "## Suggested Actions",
            "",
        ])
        
        for i, action in enumerate(report['actions'], 1):
            lines.append(f"{i}. **{action.get('title', '')}**")
            lines.append(f"   {action.get('description', '')}")
            lines.append(f"   Priority: {action.get('priority', 'unknown')} | Effort: {action.get('effort', 'unknown')} | Impact: {action.get('impact', 'unknown')}")
            lines.append("")
        
        lines.extend([
            "---",
            f"",
            f"*Generated on {report['generated_at'][:10]}*",
        ])
        
        return "\n".join(lines)
    
    def _generate_text(self, report: Dict[str, Any]) -> str:
        """Generate plain text format for email."""
        lines = [
            "WEEKLY PULSE - GROWW REVIEWS",
            "",
            f"Week: {report['week_range']}",
            f"Reviews Analyzed: {report['total_reviews']}",
            "",
            "=" * 50,
            "",
            "TOP 3 THEMES",
            "",
        ]
        
        for i, theme in enumerate(report['themes'], 1):
            lines.append(f"{i}. {theme['name']} - {theme.get('review_count', 0)} mentions")
            lines.append(f"   {theme.get('description', '')}")
            lines.append(f"   Sentiment: {theme.get('sentiment', 'unknown')} | Severity: {theme.get('severity', 'unknown')}")
            lines.append("")
        
        lines.extend([
            "USER VOICES",
            "",
        ])
        
        for quote in report['quotes']:
            lines.append(f'"{quote.get("text", "")}"')
            lines.append(f"— {quote.get('theme', '')}")
            lines.append("")
        
        lines.extend([
            "SUGGESTED ACTIONS",
            "",
        ])
        
        for i, action in enumerate(report['actions'], 1):
            lines.append(f"{i}. {action.get('title', '')}")
            lines.append(f"   {action.get('description', '')}")
            lines.append(f"   Priority: {action.get('priority', 'unknown')} | Effort: {action.get('effort', 'unknown')}")
            lines.append("")
        
        lines.extend([
            "=" * 50,
            f"",
            f"Generated on {report['generated_at'][:10]}",
        ])
        
        return "\n".join(lines)

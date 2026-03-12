#!/usr/bin/env python3
"""
Phase 3 CLI: Analysis Layer with Groq LLM

This script:
1. Reads processed reviews from Phase 2
2. Extracts themes using Groq LLM
3. Extracts representative quotes
4. Generates action ideas
5. Creates weekly pulse report
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import click
import structlog
import sqlite3
from datetime import datetime

from config import get_settings
from analyzers import GroqClient, ThemeAnalyzer, QuoteExtractor, ActionGenerator
from generators import PulseReportGenerator


structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
)

logger = structlog.get_logger()


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def cli(verbose: bool):
    """Phase 3: Analysis Layer with Groq LLM"""
    pass


@cli.command()
def analyze():
    """Run full analysis on processed reviews."""
    settings = get_settings()
    
    # Check input database
    input_db = settings.input_db_path.resolve()
    if not input_db.exists():
        raise click.ClickException(f"Input database not found: {input_db}")
    
    click.echo("📥 Loading reviews from Phase 2...")
    
    # Load reviews
    with sqlite3.connect(input_db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM reviews ORDER BY review_date DESC")
        reviews = [dict(row) for row in cursor.fetchall()]
        
        # Get date range
        cursor = conn.execute("SELECT MIN(review_date), MAX(review_date) FROM reviews")
        date_range = cursor.fetchone()
    
    click.echo(f"✅ Loaded {len(reviews)} reviews")
    click.echo(f"📅 Date range: {date_range[0][:10]} to {date_range[1][:10]}")
    
    # Initialize Groq client
    click.echo("\n🤖 Initializing Groq LLM...")
    groq_client = GroqClient(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )
    
    # Step 1: Theme Analysis
    click.echo("\n🔍 Step 1: Extracting themes...")
    theme_analyzer = ThemeAnalyzer(groq_client, max_themes=settings.max_themes)
    themes = theme_analyzer.analyze(reviews)
    
    click.echo(f"✅ Found {len(themes)} themes:")
    for theme in themes:
        click.echo(f"   • {theme['name']} ({theme.get('review_count', 0)} reviews)")
    
    # Step 2: Quote Extraction
    click.echo("\n💬 Step 2: Extracting representative quotes...")
    quote_extractor = QuoteExtractor(groq_client, max_quotes=settings.max_quotes)
    quotes = quote_extractor.extract(reviews, themes)
    
    click.echo(f"✅ Extracted {len(quotes)} quotes:")
    for quote in quotes:
        text = quote.get('text', '')[:60]
        click.echo(f'   • "{text}..."')
    
    # Step 3: Action Generation
    click.echo("\n💡 Step 3: Generating action ideas...")
    action_generator = ActionGenerator(groq_client, max_actions=settings.max_actions)
    actions = action_generator.generate(themes, quotes)
    
    click.echo(f"✅ Generated {len(actions)} actions:")
    for action in actions:
        click.echo(f"   • {action.get('title', '')}")
    
    # Step 4: Generate Report
    click.echo("\n📊 Step 4: Generating weekly pulse report...")
    report_generator = PulseReportGenerator(settings.output_dir)
    report = report_generator.generate(
        themes=themes,
        quotes=quotes,
        actions=actions,
        review_count=len(reviews),
        date_range=(date_range[0][:10], date_range[1][:10]),
    )
    
    click.echo("\n" + "=" * 50)
    click.echo("✅ ANALYSIS COMPLETE!")
    click.echo("=" * 50)
    click.echo(f"\n📁 Reports saved to: {settings.output_dir}")
    click.echo(f"   • weekly_pulse.json - Machine readable")
    click.echo(f"   • weekly_pulse.md - Markdown format")
    click.echo(f"   • weekly_pulse.txt - Plain text (for email)")
    
    # Show summary
    click.echo(f"\n📋 SUMMARY:")
    click.echo(f"   Themes: {len(themes)}")
    click.echo(f"   Quotes: {len(quotes)}")
    click.echo(f"   Actions: {len(actions)}")


@cli.command()
def config():
    """Show current configuration."""
    settings = get_settings()
    
    click.echo("\n⚙️  Phase 3 Configuration")
    click.echo("=" * 40)
    click.echo(f"Groq Model: {settings.groq_model}")
    click.echo(f"Input DB: {settings.input_db_path}")
    click.echo(f"Output Dir: {settings.output_dir}")
    click.echo(f"Max Themes: {settings.max_themes}")
    click.echo(f"Max Quotes: {settings.max_quotes}")
    click.echo(f"Max Actions: {settings.max_actions}")


if __name__ == "__main__":
    cli()

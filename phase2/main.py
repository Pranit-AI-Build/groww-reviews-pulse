#!/usr/bin/env python3
"""
Phase 2 CLI: Data Processing Layer

This script:
1. Reads raw reviews from Phase 1 database
2. Applies PII sanitization
3. Normalizes text (emojis, unicode, whitespace)
4. Stores processed reviews in Phase 2 database
5. Exports to readable files
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import click
import structlog
import sqlite3
import json
import shutil
from datetime import datetime

from config import get_settings
from processors import PIISanitizer, TextNormalizer, ReviewStorage, filter_reviews


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
    """Phase 2: Data Processing Layer"""
    pass


@cli.command()
def process():
    """Process reviews from Phase 1 database."""
    settings = get_settings()
    
    input_db = settings.input_db_path.resolve()
    output_db = settings.output_db_path
    
    if not input_db.exists():
        raise click.ClickException(f"Input database not found: {input_db}")
    
    click.echo(f"📥 Reading from: {input_db}")
    click.echo(f"📤 Writing to: {output_db}")
    
    # Initialize processors
    sanitizer = PIISanitizer()
    normalizer = TextNormalizer()
    storage = ReviewStorage(output_db)
    
    # Read from Phase 1 database
    with sqlite3.connect(input_db) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM reviews ORDER BY review_date DESC")
        rows = cursor.fetchall()
    
    click.echo(f"\n📊 Found {len(rows)} reviews in Phase 1 database")
    
    # Process reviews
    processed_reviews = []
    for row in rows:
        review = {
            "review_id": row["id"],
            "source": row["source"],
            "rating": row["rating"],
            "title": row["title"],
            "text": row["text"],
            "date": row["review_date"],
            "version": row["app_version"],
            "language": row["language"],
        }
        
        # Normalize
        review["text"] = normalizer.normalize(review["text"])
        review["title"] = normalizer.normalize(review.get("title"))
        
        # Sanitize PII
        review = sanitizer.sanitize_review(review)
        
        processed_reviews.append(review)
    
    # Apply quality filters
    click.echo(f"\n🔍 Applying quality filters...")
    filtered_reviews = filter_reviews(
        processed_reviews,
        min_words=4,
        min_chars=20,
    )
    
    click.echo(f"  Original: {len(processed_reviews)} reviews")
    click.echo(f"  After filtering: {len(filtered_reviews)} reviews")
    click.echo(f"  Removed: {len(processed_reviews) - len(filtered_reviews)} reviews")
    
    # Save to Phase 2 database
    result = storage.save_reviews(filtered_reviews)
    
    click.echo(f"\n✅ Processing complete!")
    click.echo(f"  Total processed: {len(filtered_reviews)}")
    click.echo(f"  Inserted: {result['inserted']}")
    click.echo(f"  Skipped: {result['skipped']}")
    
    # Export to files
    export_to_files(filtered_reviews, settings.data_dir)


def export_to_files(reviews: list, data_dir: Path):
    """Export processed reviews to readable files."""
    
    # Export to JSON
    json_path = data_dir / "processed_reviews.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    # Export to text
    text_path = data_dir / "processed_reviews.txt"
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("PROCESSED REVIEWS - PHASE 2 OUTPUT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total reviews: {len(reviews)}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("\n" + "=" * 70 + "\n\n")
        
        for i, review in enumerate(reviews, 1):
            stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
            f.write(f"{i}. [{stars}] {review['date'][:10]}\n")
            if review.get('title'):
                f.write(f"   Title: {review['title']}\n")
            f.write(f"   {review['text']}\n")
            if review.get('version'):
                f.write(f"   Version: {review['version']}\n")
            f.write("\n" + "-" * 70 + "\n\n")
    
    click.echo(f"\n📁 Exported to:")
    click.echo(f"  JSON: {json_path}")
    click.echo(f"  Text: {text_path}")


@cli.command()
def stats():
    """Show processed database statistics."""
    settings = get_settings()
    storage = ReviewStorage(settings.output_db_path)
    
    stats_data = storage.get_stats()
    
    click.echo("\n📊 Phase 2 Database Statistics")
    click.echo("=" * 40)
    click.echo(f"Total reviews: {stats_data['total_reviews']}")
    
    if stats_data['earliest_review']:
        click.echo(f"Date range: {stats_data['earliest_review'][:10]} to {stats_data['latest_review'][:10]}")
    
    if stats_data['rating_distribution']:
        click.echo("\nRating distribution:")
        max_count = max(stats_data['rating_distribution'].values()) if stats_data['rating_distribution'] else 1
        for rating, count in sorted(stats_data['rating_distribution'].items()):
            bar = "█" * (count * 20 // max(max_count, 1) + 1)
            click.echo(f"  {rating}★: {bar} {count}")


@cli.command()
@click.option("--limit", "-l", type=int, default=10, help="Number of reviews to show")
def list_reviews(limit: int):
    """List processed reviews."""
    settings = get_settings()
    storage = ReviewStorage(settings.output_db_path)
    
    reviews = storage.get_reviews(limit=limit)
    
    if not reviews:
        click.echo("No reviews found in database.")
        return
    
    click.echo(f"\n📋 Processed Reviews (showing {len(reviews)})")
    click.echo("=" * 60)
    
    for i, review in enumerate(reviews, 1):
        stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
        click.echo(f"\n{i}. [{stars}] {review['date'][:10]}")
        if review.get('title'):
            click.echo(f"   Title: {review['title']}")
        text = review['text'][:200] + "..." if len(review['text']) > 200 else review['text']
        click.echo(f"   {text}")


if __name__ == "__main__":
    cli()

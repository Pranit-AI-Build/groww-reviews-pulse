#!/usr/bin/env python3
"""
Phase 1 CLI: Groww Play Store Review Collector

This script collects reviews from the Groww app on Play Store,
sanitizes them for PII, and stores them in a SQLite database.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import click
import structlog
from datetime import datetime

from config import get_settings
from collectors import PlayStoreCollector
from processors import PIISanitizer, TextNormalizer
from processors.storage import ReviewStorage


# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@click.group()
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose logging"
)
def cli(verbose: bool):
    """Groww Play Store Review Collector - Phase 1"""
    if verbose:
        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(10)  # DEBUG
        )


@cli.command()
@click.option(
    "--weeks", "-w",
    type=int,
    default=None,
    help="Number of weeks to collect (default: from config)"
)
@click.option(
    "--max-reviews", "-m",
    type=int,
    default=None,
    help="Maximum number of reviews to collect"
)
@click.option(
    "--dry-run", "-d",
    is_flag=True,
    help="Fetch reviews but don't save to database"
)
def collect(weeks: int, max_reviews: int, dry_run: bool):
    """Collect reviews from Play Store."""
    settings = get_settings()
    
    # Override weeks if provided
    weeks_to_collect = weeks or settings.weeks_to_collect
    
    logger.info(
        "Starting review collection",
        app_id=settings.playstore_app_id,
        weeks=weeks_to_collect,
        max_reviews=max_reviews,
        dry_run=dry_run,
    )
    
    # Initialize components
    collector = PlayStoreCollector(
        app_id=settings.playstore_app_id,
        language=settings.language,
        country=settings.country,
        weeks_to_collect=weeks_to_collect,
        min_rating=settings.min_rating,
        max_rating=settings.max_rating,
    )
    
    sanitizer = PIISanitizer()
    normalizer = TextNormalizer()
    
    if not dry_run:
        storage = ReviewStorage(settings.database_path)
    
    # Fetch reviews
    reviews = []
    review_count = 0
    
    try:
        for review in collector.fetch_reviews(max_reviews=max_reviews):
            # Process review
            review_dict = review.to_dict()
            
            # Normalize text
            review_dict["text"] = normalizer.normalize(review_dict["text"])
            review_dict["title"] = normalizer.normalize(review_dict.get("title"))
            
            # Sanitize PII
            review_dict = sanitizer.sanitize_review(review_dict)
            
            reviews.append(review_dict)
            review_count += 1
            
            if review_count % 100 == 0:
                logger.info(f"Processed {review_count} reviews...")
        
        logger.info(
            "Review fetching complete",
            total_collected=review_count,
        )
        
        if dry_run:
            logger.info(
                "Dry run mode - not saving to database",
                would_save=len(reviews),
            )
            # Print sample
            if reviews:
                click.echo("\nSample review:")
                sample = reviews[0]
                click.echo(f"  ID: {sample['review_id']}")
                click.echo(f"  Rating: {sample['rating']}")
                click.echo(f"  Date: {sample['date']}")
                click.echo(f"  Title: {sample.get('title', 'N/A')}")
                click.echo(f"  Text: {sample['text'][:200]}...")
        else:
            # Save to database
            result = storage.save_reviews(
                reviews,
                app_id=settings.playstore_app_id,
                weeks_collected=weeks_to_collect,
            )
            
            click.echo(f"\n✓ Collection complete!")
            click.echo(f"  Total fetched: {review_count}")
            click.echo(f"  Inserted: {result['inserted']}")
            click.echo(f"  Skipped (duplicates): {result['skipped']}")
    
    except Exception as e:
        logger.error("Collection failed", error=str(e))
        raise click.ClickException(f"Collection failed: {e}")


@cli.command()
def stats():
    """Show database statistics."""
    settings = get_settings()
    storage = ReviewStorage(settings.database_path)
    
    stats_data = storage.get_stats()
    
    click.echo("\n📊 Database Statistics")
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
    
    if stats_data['last_collection']:
        last = stats_data['last_collection']
        click.echo(f"\nLast collection:")
        click.echo(f"  Date: {last['date'][:19] if last['date'] else 'N/A'}")
        click.echo(f"  Reviews added: {last['count']}")
        click.echo(f"  App ID: {last['app_id'] or 'N/A'}")


@cli.command()
@click.option(
    "--limit", "-l",
    type=int,
    default=10,
    help="Number of reviews to show"
)
@click.option(
    "--rating", "-r",
    type=int,
    help="Filter by rating (1-5)"
)
def list_reviews(limit: int, rating: int):
    """List recent reviews from database."""
    settings = get_settings()
    storage = ReviewStorage(settings.database_path)
    
    reviews = storage.get_reviews(
        min_rating=rating,
        max_rating=rating,
        limit=limit,
    )
    
    if not reviews:
        click.echo("No reviews found in database.")
        return
    
    click.echo(f"\n📋 Recent Reviews (showing {len(reviews)})")
    click.echo("=" * 60)
    
    for i, review in enumerate(reviews, 1):
        click.echo(f"\n{i}. [{review['rating']}★] {review['date'][:10]}")
        if review.get('title'):
            click.echo(f"   Title: {review['title']}")
        text = review['text'][:200] + "..." if len(review['text']) > 200 else review['text']
        click.echo(f"   {text}")


@cli.command()
def config():
    """Show current configuration."""
    settings = get_settings()
    
    click.echo("\n⚙️  Current Configuration")
    click.echo("=" * 40)
    click.echo(f"App Name: {settings.app_name}")
    click.echo(f"Play Store App ID: {settings.playstore_app_id}")
    click.echo(f"Play Store URL: {settings.playstore_url}")
    click.echo(f"Weeks to collect: {settings.weeks_to_collect}")
    click.echo(f"Rating range: {settings.min_rating}-{settings.max_rating}")
    click.echo(f"Language: {settings.language}")
    click.echo(f"Country: {settings.country}")
    click.echo(f"Database path: {settings.database_path}")


if __name__ == "__main__":
    cli()

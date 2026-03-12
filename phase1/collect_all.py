#!/usr/bin/env python3
"""Collect all available reviews without limits."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from datetime import datetime, timedelta
from collectors import PlayStoreCollector
from processors import PIISanitizer, TextNormalizer
from processors.storage import ReviewStorage
from config import get_settings
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
)

settings = get_settings()

# Use 12 weeks to get maximum history
collector = PlayStoreCollector(
    app_id=settings.playstore_app_id,
    language=settings.language,
    country=settings.country,
    weeks_to_collect=12,
)

sanitizer = PIISanitizer()
normalizer = TextNormalizer()
storage = ReviewStorage(settings.database_path)

print("Collecting all available reviews (this may take a while)...")
print(f"Cutoff date: {collector.cutoff_date.date()}")

reviews = []
for review in collector.fetch_reviews():
    review_dict = review.to_dict()
    review_dict["text"] = normalizer.normalize(review_dict["text"])
    review_dict["title"] = normalizer.normalize(review_dict.get("title"))
    review_dict = sanitizer.sanitize_review(review_dict)
    reviews.append(review_dict)
    
    if len(reviews) % 100 == 0:
        print(f"  Fetched {len(reviews)} reviews...")

print(f"\nTotal fetched: {len(reviews)}")

if reviews:
    dates = [r["date"] for r in reviews]
    print(f"Date range: {min(dates)[:10]} to {max(dates)[:10]}")
    
    # Save to database
    result = storage.save_reviews(
        reviews,
        app_id=settings.playstore_app_id,
        weeks_collected=12,
    )
    print(f"\nSaved to database:")
    print(f"  Inserted: {result['inserted']}")
    print(f"  Skipped: {result['skipped']}")
else:
    print("No reviews found!")

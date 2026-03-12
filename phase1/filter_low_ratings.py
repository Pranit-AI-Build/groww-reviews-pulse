#!/usr/bin/env python3
"""Filter database to keep only reviews with rating <= 2 stars and export to file."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import sqlite3
import json
from datetime import datetime
from config import get_settings

settings = get_settings()

def filter_and_export():
    db_path = settings.database_path
    
    # Connect to database
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        
        # Count before
        cursor = conn.execute('SELECT COUNT(*), rating FROM reviews GROUP BY rating ORDER BY rating')
        print("Current reviews by rating:")
        for row in cursor.fetchall():
            print(f"  {row[1]}★: {row[0]} reviews")
        
        # Get all reviews with rating <= 2
        cursor = conn.execute(
            'SELECT * FROM reviews WHERE rating <= 2 ORDER BY review_date DESC'
        )
        low_rating_reviews = [dict(row) for row in cursor.fetchall()]
        
        print(f"\nFound {len(low_rating_reviews)} reviews with rating <= 2")
        
        # Delete reviews with rating > 2
        cursor = conn.execute('DELETE FROM reviews WHERE rating > 2')
        deleted = cursor.rowcount
        conn.commit()
        
        print(f"Deleted {deleted} reviews with rating > 2")
        
        # Count after
        cursor = conn.execute('SELECT COUNT(*) FROM reviews')
        remaining = cursor.fetchone()[0]
        print(f"Remaining reviews in database: {remaining}")
    
    # Export to JSON file
    export_path = settings.data_dir / "low_rating_reviews.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(low_rating_reviews, f, indent=2, ensure_ascii=False)
    
    print(f"\nExported {len(low_rating_reviews)} reviews to: {export_path}")
    
    # Also export to text file for easy reading
    text_path = settings.data_dir / "low_rating_reviews.txt"
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("LOW RATING REVIEWS (1-2 STARS) - GROWW APP\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total reviews: {len(low_rating_reviews)}\n")
        f.write(f"Date range: {low_rating_reviews[-1]['review_date'][:10] if low_rating_reviews else 'N/A'} to {low_rating_reviews[0]['review_date'][:10] if low_rating_reviews else 'N/A'}\n")
        f.write("\n" + "=" * 70 + "\n\n")
        
        for i, review in enumerate(low_rating_reviews, 1):
            f.write(f"{i}. [{'★' * review['rating']}{'☆' * (5 - review['rating'])}] {review['review_date'][:10]}\n")
            if review['title']:
                f.write(f"   Title: {review['title']}\n")
            f.write(f"   {review['text']}\n")
            if review['app_version']:
                f.write(f"   Version: {review['app_version']}\n")
            f.write("\n" + "-" * 70 + "\n\n")
    
    print(f"Also exported to text file: {text_path}")
    
    # Show sample
    if low_rating_reviews:
        print("\n" + "=" * 70)
        print("SAMPLE REVIEWS:")
        print("=" * 70)
        for review in low_rating_reviews[:3]:
            print(f"\n[{'★' * review['rating']}{'☆' * (5 - review['rating'])}] {review['review_date'][:10]}")
            if review['title']:
                print(f"Title: {review['title']}")
            print(f"{review['text'][:200]}...")

if __name__ == "__main__":
    filter_and_export()

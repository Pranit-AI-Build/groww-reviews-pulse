"""SQLite storage layer for reviews."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import structlog

logger = structlog.get_logger()


class ReviewStorage:
    """SQLite storage for reviews with deduplication."""
    
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL DEFAULT 'playstore',
        rating INTEGER NOT NULL,
        title TEXT,
        text TEXT NOT NULL,
        review_date TIMESTAMP NOT NULL,
        app_version TEXT,
        language TEXT DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);
    CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
    CREATE INDEX IF NOT EXISTS idx_reviews_source ON reviews(source);
    
    CREATE TABLE IF NOT EXISTS collection_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_collection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reviews_count INTEGER DEFAULT 0,
        app_id TEXT,
        weeks_collected INTEGER
    );
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.logger = logger.bind(storage="ReviewStorage", db_path=str(db_path))
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database with schema."""
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(self.SCHEMA)
        
        self.logger.info("Database initialized")
    
    def save_reviews(
        self,
        reviews: List[Dict[str, Any]],
        app_id: Optional[str] = None,
        weeks_collected: Optional[int] = None,
    ) -> Dict[str, int]:
        """
        Save reviews to database with deduplication.
        
        Args:
            reviews: List of review dictionaries
            app_id: App ID for metadata
            weeks_collected: Number of weeks collected for metadata
            
        Returns:
            Dict with 'inserted' and 'skipped' counts
        """
        inserted = 0
        skipped = 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for review in reviews:
                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO reviews 
                        (id, source, rating, title, text, review_date, app_version, language)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            review["review_id"],
                            review.get("source", "playstore"),
                            review["rating"],
                            review.get("title"),
                            review["text"],
                            review["date"],
                            review.get("version"),
                            review.get("language", "en"),
                        )
                    )
                    
                    if cursor.rowcount > 0:
                        inserted += 1
                    else:
                        skipped += 1
                        
                except sqlite3.Error as e:
                    self.logger.error(
                        "Error saving review",
                        review_id=review.get("review_id"),
                        error=str(e),
                    )
                    skipped += 1
            
            conn.commit()
            
            # Update metadata
            cursor.execute(
                """
                INSERT INTO collection_metadata 
                (last_collection_date, reviews_count, app_id, weeks_collected)
                VALUES (?, ?, ?, ?)
                """,
                (datetime.now().isoformat(), inserted, app_id, weeks_collected)
            )
            conn.commit()
        
        self.logger.info(
            "Reviews saved",
            inserted=inserted,
            skipped=skipped,
            total=len(reviews),
        )
        
        return {"inserted": inserted, "skipped": skipped}
    
    def get_reviews(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve reviews with optional filters.
        
        Args:
            start_date: Filter reviews from this date
            end_date: Filter reviews until this date
            min_rating: Minimum rating filter
            max_rating: Maximum rating filter
            limit: Maximum number of reviews to return
            
        Returns:
            List of review dictionaries
        """
        query = "SELECT * FROM reviews WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND review_date >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND review_date <= ?"
            params.append(end_date.isoformat())
        
        if min_rating is not None:
            query += " AND rating >= ?"
            params.append(min_rating)
        
        if max_rating is not None:
            query += " AND rating <= ?"
            params.append(max_rating)
        
        query += " ORDER BY review_date DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
        
        reviews = []
        for row in rows:
            reviews.append({
                "review_id": row["id"],
                "source": row["source"],
                "rating": row["rating"],
                "title": row["title"],
                "text": row["text"],
                "date": row["review_date"],
                "version": row["app_version"],
                "language": row["language"],
                "created_at": row["created_at"],
            })
        
        return reviews
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total reviews
            cursor.execute("SELECT COUNT(*) FROM reviews")
            total_reviews = cursor.fetchone()[0]
            
            # Date range
            cursor.execute(
                "SELECT MIN(review_date), MAX(review_date) FROM reviews"
            )
            date_range = cursor.fetchone()
            
            # Rating distribution
            cursor.execute(
                "SELECT rating, COUNT(*) FROM reviews GROUP BY rating ORDER BY rating"
            )
            rating_dist = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Last collection
            cursor.execute(
                "SELECT * FROM collection_metadata ORDER BY id DESC LIMIT 1"
            )
            last_collection = cursor.fetchone()
        
        return {
            "total_reviews": total_reviews,
            "earliest_review": date_range[0] if date_range else None,
            "latest_review": date_range[1] if date_range else None,
            "rating_distribution": rating_dist,
            "last_collection": {
                "date": last_collection[1] if last_collection else None,
                "count": last_collection[2] if last_collection else 0,
                "app_id": last_collection[3] if last_collection else None,
                "weeks_collected": last_collection[4] if last_collection else None,
            } if last_collection else None,
        }
    
    def get_review_count(self) -> int:
        """Get total number of reviews in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM reviews")
            return cursor.fetchone()[0]

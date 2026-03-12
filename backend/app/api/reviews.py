"""Reviews API endpoints."""

import sqlite3
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.get("", response_model=List[Dict[str, Any]])
async def get_reviews(limit: int = 100, offset: int = 0):
    """Get processed reviews."""
    settings = get_settings()
    
    if not settings.database_path.exists():
        raise HTTPException(status_code=404, detail="Database not found")
    
    with sqlite3.connect(settings.database_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM reviews ORDER BY review_date DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        reviews = [dict(row) for row in cursor.fetchall()]
    
    return reviews


@router.get("/stats")
async def get_stats():
    """Get review statistics."""
    settings = get_settings()
    
    if not settings.database_path.exists():
        raise HTTPException(status_code=404, detail="Database not found")
    
    with sqlite3.connect(settings.database_path) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM reviews")
        total = cursor.fetchone()[0]
        
        cursor = conn.execute(
            "SELECT rating, COUNT(*) FROM reviews GROUP BY rating ORDER BY rating"
        )
        rating_dist = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor = conn.execute(
            "SELECT MIN(review_date), MAX(review_date) FROM reviews"
        )
        date_range = cursor.fetchone()
    
    return {
        "total_reviews": total,
        "rating_distribution": rating_dist,
        "date_range": {
            "start": date_range[0] if date_range else None,
            "end": date_range[1] if date_range else None,
        }
    }

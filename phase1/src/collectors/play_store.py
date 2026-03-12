"""Play Store review collector using google-play-scraper."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterator, List, Optional
import structlog

from google_play_scraper import reviews, Sort

logger = structlog.get_logger()


@dataclass
class Review:
    """Standardized review data structure."""
    review_id: str
    source: str
    rating: int
    title: Optional[str]
    text: str
    date: datetime
    version: Optional[str]
    language: str = "en"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "review_id": self.review_id,
            "source": self.source,
            "rating": self.rating,
            "title": self.title,
            "text": self.text,
            "date": self.date.isoformat(),
            "version": self.version,
            "language": self.language,
        }


class PlayStoreCollector:
    """Collector for Google Play Store reviews."""
    
    def __init__(
        self,
        app_id: str,
        language: str = "en",
        country: str = "IN",
        weeks_to_collect: int = 10,
        min_rating: int = 1,
        max_rating: int = 5,
    ):
        self.app_id = app_id
        self.language = language
        self.country = country
        self.weeks_to_collect = weeks_to_collect
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.logger = logger.bind(collector="PlayStore", app_id=app_id)
        
        # Calculate cutoff date
        self.cutoff_date = datetime.now() - timedelta(weeks=weeks_to_collect)
        
    def fetch_reviews(
        self,
        max_reviews: Optional[int] = None,
    ) -> Iterator[Review]:
        """
        Fetch reviews from Play Store.
        
        Args:
            max_reviews: Maximum number of reviews to fetch (None for all)
            
        Yields:
            Review objects
        """
        self.logger.info(
            "Starting review collection",
            cutoff_date=self.cutoff_date.isoformat(),
            max_reviews=max_reviews,
        )
        
        continuation_token = None
        fetched_count = 0
        
        while True:
            try:
                # Fetch batch of reviews
                result, continuation_token = reviews(
                    self.app_id,
                    lang=self.language,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=100,  # Batch size
                    continuation_token=continuation_token,
                )
                
                if not result:
                    self.logger.info("No more reviews available")
                    break
                
                for review_data in result:
                    # Check if we've reached the cutoff date
                    review_date = review_data.get("at")
                    if review_date and review_date < self.cutoff_date:
                        self.logger.info(
                            "Reached cutoff date, stopping collection",
                            review_date=review_date.isoformat(),
                            cutoff_date=self.cutoff_date.isoformat(),
                            total_fetched=fetched_count,
                        )
                        return
                    
                    # Filter by rating
                    rating = review_data.get("score", 0)
                    if not (self.min_rating <= rating <= self.max_rating):
                        continue
                    
                    # Create standardized review
                    review = Review(
                        review_id=review_data.get("reviewId", ""),
                        source="playstore",
                        rating=rating,
                        title=review_data.get("title"),
                        text=review_data.get("content", ""),
                        date=review_date or datetime.now(),
                        version=review_data.get("appVersion"),
                        language=self.language,
                    )
                    
                    yield review
                    fetched_count += 1
                    
                    # Check max reviews limit
                    if max_reviews and fetched_count >= max_reviews:
                        self.logger.info(
                            "Reached max reviews limit",
                            limit=max_reviews,
                        )
                        return
                
                self.logger.debug(
                    "Fetched batch of reviews",
                    batch_size=len(result),
                    total_fetched=fetched_count,
                )
                
                # Stop if no continuation token
                if not continuation_token:
                    break
                    
            except Exception as e:
                self.logger.error(
                    "Error fetching reviews",
                    error=str(e),
                    total_fetched=fetched_count,
                )
                raise
        
        self.logger.info(
            "Review collection complete",
            total_fetched=fetched_count,
        )
    
    def fetch_all_reviews(self) -> List[Review]:
        """Fetch all reviews as a list."""
        return list(self.fetch_reviews())
    
    def collect_recent(self, days: int = 7) -> List[dict]:
        """Collect reviews from the last N days."""
        from datetime import timedelta
        
        # Temporarily update cutoff date
        original_cutoff = self.cutoff_date
        self.cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            reviews_list = []
            for review in self.fetch_reviews():
                reviews_list.append(review.to_dict())
            return reviews_list
        finally:
            # Restore original cutoff
            self.cutoff_date = original_cutoff

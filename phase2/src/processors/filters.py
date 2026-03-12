"""Review filtering utilities for Phase 2."""

import re
from typing import List, Dict, Any, Set
import structlog

logger = structlog.get_logger()


class ReviewFilter:
    """Filters reviews based on quality and content criteria."""
    
    def __init__(
        self,
        min_words: int = 4,
        min_chars: int = 20,
        remove_duplicates: bool = True,
        english_only: bool = True,
    ):
        self.min_words = min_words
        self.min_chars = min_chars
        self.remove_duplicates = remove_duplicates
        self.english_only = english_only
        self.logger = logger.bind(processor="ReviewFilter")
        
        # Track seen reviews for deduplication
        self.seen_texts: Set[str] = set()
        
        # Common non-English script ranges (Unicode blocks)
        self.non_english_patterns = [
            r'[\u0400-\u04FF]',  # Cyrillic
            r'[\u0600-\u06FF]',  # Arabic
            r'[\u0900-\u097F]',  # Devanagari (Hindi)
            r'[\u3040-\u309F]',  # Hiragana
            r'[\u30A0-\u30FF]',  # Katakana
            r'[\u4E00-\u9FFF]',  # CJK Unified Ideographs
            r'[\uAC00-\uD7AF]',  # Korean Hangul
            r'[\u0E00-\u0E7F]',  # Thai
            r'[\u0370-\u03FF]',  # Greek
            r'[\u0590-\u05FF]',  # Hebrew
        ]
    
    def filter_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply all filters to reviews.
        
        Returns:
            List of filtered reviews
        """
        filtered = []
        stats = {
            "total": len(reviews),
            "too_short_words": 0,
            "too_short_chars": 0,
            "non_english": 0,
            "only_symbols": 0,
            "duplicates": 0,
            "passed": 0,
        }
        
        for review in reviews:
            text = review.get("text", "").strip()
            
            # Filter 1: Minimum character length
            if len(text) < self.min_chars:
                stats["too_short_chars"] += 1
                continue
            
            # Filter 2: Minimum word count
            word_count = len(text.split())
            if word_count < self.min_words:
                stats["too_short_words"] += 1
                continue
            
            # Filter 3: Only emojis/symbols (no real text)
            if self._is_only_symbols(text):
                stats["only_symbols"] += 1
                continue
            
            # Filter 4: English only
            if self.english_only and not self._is_english(text):
                stats["non_english"] += 1
                continue
            
            # Filter 5: Remove duplicates
            if self.remove_duplicates:
                normalized_text = self._normalize_for_dedup(text)
                if normalized_text in self.seen_texts:
                    stats["duplicates"] += 1
                    continue
                self.seen_texts.add(normalized_text)
            
            filtered.append(review)
            stats["passed"] += 1
        
        self.logger.info(
            "Filtering complete",
            **stats
        )
        
        return filtered
    
    def _is_only_symbols(self, text: str) -> bool:
        """Check if text contains only emojis, symbols, or punctuation."""
        # Remove common symbols, emojis, punctuation, numbers
        cleaned = re.sub(r'[^\w\s]', '', text)  # Remove punctuation/symbols
        cleaned = re.sub(r'\d', '', cleaned)     # Remove numbers
        cleaned = cleaned.strip()
        
        # If less than 3 letters remain, it's mostly symbols
        letters = re.sub(r'[^a-zA-Z]', '', cleaned)
        return len(letters) < 3
    
    def _is_english(self, text: str) -> bool:
        """Check if text is entirely in English."""
        # Common non-English words (Hindi, Tamil, etc. written in Latin script or native)
        non_english_words = {
            # Hindi common words - extensive list
            'hai', 'nhi', 'nahi', 'nahin', 'kyu', 'kyon', 'kya', 'ka', 'ke', 'ki', 'ko',
            'mein', 'main', 'mera', 'meri', 'tum', 'tumhara', 'aap', 'aapka', 'aapki',
            'bohot', 'bahut', 'bht', 'jyada', 'zyaada', 'zyada', 'kam', 'acha', 'accha',
            'bura', 'ganda', 'sahi', 'galat', 'kuch', 'sab', 'yeh', 'woh', 'ye', 'vo',
            'idhar', 'udhar', 'pe', 'par', 'se', 'tak', 'aur', 'ya', 'lekin',
            'magar', 'kyunki', 'isliye', 'jab', 'tab', 'agar', 'toh', 'bhi',
            'hi', 'mat', 'karo', 'kare', 'raha', 'rahi', 'rahe', 'rha', 'rhi',
            'tha', 'thi', 'the', 'hoga', 'hogi', 'honge', 'kar', 'kiya', 'kr',
            'liye', 'baar', 'bar', 'din', 'raat', 'saal', 'mahina', 'mahine',
            'ghanta', 'ghante', 'minute', 'der', 'jaldi', 'dheere', 'tez', 'bahar',
            'andar', 'upar', 'neeche', 'niche', 'aage', 'peeche', 'piche', 'daaye', 'baaye',
            'ek', 'do', 'teen', 'char', 'paanch', 'cheh', 'saat', 'aath', 'nau', 'das',
            'hazaar', 'hazar', 'lakh', 'lakhs', 'crore', 'crores',
            'paisa', 'paise', 'rupaye', 'rupey', 'sawa', 'pauna', 'dedh', 'dhai', 'sade', 'sava',
            'bhai', 'behen', 'dost', 'doston', 'log', 'logo', 'logon',
            'gaya', 'gya', 'gayi', 'gyi', 'gaye', 'aaya', 'aayi', 'aaye',
            'dekh', 'dekho', 'sun', 'suno', 'bol', 'bolo', 'ja', 'jao',
            'karo', 'krna', 'krne', 'krwao', 'krwa', 'banao', 'bana',
            'fir', 'phir', 'pehle', 'pahle', 'baad', 'abhi', 'abi', 'tabhi',
            'wahe', 'wahi', 'yahi', 'yehin', 'vahan', 'yahan', 'idhar', 'udhar',
            'sabse', 'sbse', 'zyada', 'jyada', 'kam', 'thora', 'thoda', 'bahut',
            'acha', 'accha', 'bura', 'bekar', 'ghatiya', 'ganda', 'sundar',
            'chalo', 'chale', 'aao', 'aajao', 'niklo', 'nikal', 'nikalo',
            'mujhe', 'mujh', 'tujhe', 'tujh', 'usko', 'isko', 'unhe', 'inhe',
            'mera', 'meri', 'mere', 'tera', 'teri', 'tere', 'uska', 'uski', 'uske',
            'apna', 'apni', 'apne', 'sabka', 'sabki', 'sabke',
            'waqt', 'samay', 'ghadi', 'pal', 'lamha', 'lamhe',
            'saal', 'saalon', 'mahina', 'mahine', 'hafta', 'hafte', 'din', 'dino',
            'subah', 'shaam', 'raat', 'dopahar',
            'aaj', 'kal', 'parson', 'kal', 'aane', 'jaane', 'aana', 'jaana',
            'karna', 'krna', 'krne', 'krwao', 'krwa', 'banao', 'bana',
            'lagao', 'laga', 'lagana', 'lagao', 'khol', 'kholo', 'band', 'bandh',
            'chalu', 'band', 'on', 'off', 'start', 'stop',
            'scam', 'bekar', 'faltu', 'fuddu', 'bakwaas', 'bakwas',
            'aree', 'arey', 'arre', 'yar', 'yaar', 'janab', 'bhaijaan',
            'investment', 'paisa', 'paise', 'rupaye', 'rupya', 'rupy',
            # Tamil common words
            'enna', 'nalla', 'ketta', 'romba', 'konjam', 'adhuvum',
            'indha', 'andha', 'inga', 'anga', 'epdi', 'yaaru',
            # Telugu common words
            'emi', 'enti', 'bagundi', 'baledu', 'chala', 'koncham', 'idi',
            # Malayalam common words
            'enth', 'nallath', 'mosam', 'valare', 'kurach', 'ith',
        }
        
        # Convert to lowercase words for checking
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        if not words:
            return False
        
        # Check if any non-English words are present
        for word in words:
            if word in non_english_words:
                return False
        
        # Also check for non-Latin script characters
        for char in text:
            if char.isalpha() and not ('a' <= char.lower() <= 'z'):
                return False
        
        return True
    
    def _normalize_for_dedup(self, text: str) -> str:
        """Normalize text for duplicate detection."""
        # Lowercase, remove extra spaces, remove punctuation
        normalized = text.lower()
        normalized = re.sub(r'[^\w\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized


def filter_reviews(
    reviews: List[Dict[str, Any]],
    min_words: int = 4,
    min_chars: int = 20,
) -> List[Dict[str, Any]]:
    """
    Convenience function to filter reviews.
    
    Args:
        reviews: List of review dictionaries
        min_words: Minimum number of words required
        min_chars: Minimum number of characters required
        
    Returns:
        Filtered list of reviews
    """
    filter_obj = ReviewFilter(
        min_words=min_words,
        min_chars=min_chars,
        remove_duplicates=True,
        english_only=True,
    )
    return filter_obj.filter_reviews(reviews)

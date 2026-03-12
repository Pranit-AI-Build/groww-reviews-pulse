"""PII sanitization and text normalization for reviews."""

import re
import unicodedata
from typing import Optional
import structlog

logger = structlog.get_logger()


class PIISanitizer:
    """Removes personally identifiable information from review text."""
    
    # Patterns for PII detection
    PATTERNS = {
        # Email addresses
        "email": re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            re.IGNORECASE
        ),
        # Phone numbers (Indian format)
        "phone": re.compile(
            r'\b(?:\+91[-\s]?)?[0]?(?:\d{10}|\d{5}[-\s]?\d{5})\b'
        ),
        # PAN numbers
        "pan": re.compile(
            r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
            re.IGNORECASE
        ),
        # Aadhaar numbers (masked or full)
        "aadhaar": re.compile(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        ),
        # Account numbers (basic pattern)
        "account": re.compile(
            r'\b(?:account|acc|a/c)[\s#:]*\d{6,}\b',
            re.IGNORECASE
        ),
        # UPI IDs
        "upi": re.compile(
            r'\b[A-Za-z0-9._-]+@[A-Za-z0-9]+\b',
            re.IGNORECASE
        ),
        # URLs (might contain personal info)
        "url": re.compile(
            r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
            re.IGNORECASE
        ),
    }
    
    # Replacement text
    REPLACEMENTS = {
        "email": "[EMAIL_REDACTED]",
        "phone": "[PHONE_REDACTED]",
        "pan": "[PAN_REDACTED]",
        "aadhaar": "[AADHAAR_REDACTED]",
        "account": "[ACCOUNT_REDACTED]",
        "upi": "[UPI_REDACTED]",
        "url": "[URL_REDACTED]",
    }
    
    def __init__(self):
        self.logger = logger.bind(processor="PIISanitizer")
    
    def sanitize(self, text: Optional[str]) -> Optional[str]:
        """
        Remove PII from text.
        
        Args:
            text: Input text to sanitize
            
        Returns:
            Sanitized text with PII replaced
        """
        if not text:
            return text
        
        original_text = text
        sanitized_count = 0
        
        for pii_type, pattern in self.PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                sanitized_count += len(matches)
                text = pattern.sub(self.REPLACEMENTS[pii_type], text)
        
        if sanitized_count > 0:
            self.logger.debug(
                "Sanitized PII from text",
                sanitized_count=sanitized_count,
            )
        
        return text
    
    def sanitize_review(self, review: dict) -> dict:
        """
        Sanitize all text fields in a review dictionary.
        
        Args:
            review: Review dictionary with text fields
            
        Returns:
            Review with sanitized text fields
        """
        sanitized = review.copy()
        
        # Sanitize text fields
        if "text" in sanitized:
            sanitized["text"] = self.sanitize(sanitized["text"])
        
        if "title" in sanitized:
            sanitized["title"] = self.sanitize(sanitized["title"])
        
        return sanitized


class TextNormalizer:
    """Normalizes text encoding and handles special characters."""
    
    def __init__(self):
        self.logger = logger.bind(processor="TextNormalizer")
    
    def normalize(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize text encoding and clean special characters.
        
        Args:
            text: Input text to normalize
            
        Returns:
            Normalized text
        """
        if not text:
            return text
        
        # Normalize unicode (NFKC form)
        text = unicodedata.normalize('NFKC', text)
        
        # Replace common emoji with text descriptions
        text = self._replace_emojis(text)
        
        # Clean excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _replace_emojis(self, text: str) -> str:
        """Replace common emojis with text descriptions."""
        # Common emoji mappings
        emoji_map = {
            '😊': ':)',
            '😃': ':D',
            '😄': ':D',
            '😁': ':D',
            '😆': 'xD',
            '😂': "'.",
            '🤣': "'.",
            '😉': ';)',
            '😍': '<3',
            '🥰': '<3',
            '😘': ':*',
            '😗': ':*',
            '😚': ':*',
            '😙': ':*',
            '😋': ':P',
            '😛': ':P',
            '😜': ';P',
            '😝': 'xP',
            '😐': ':|',
            '😑': '-_-',
            '😶': '...',
            '🙄': 'rolling eyes',
            '😏': 'smirk',
            '😒': 'unamused',
            '😬': 'grimace',
            '🤥': 'lying',
            '😌': 'relieved',
            '😔': 'sad',
            '😪': 'sleepy',
            '🤤': 'drooling',
            '😴': 'sleeping',
            '😷': 'sick',
            '🤒': 'sick',
            '🤕': 'injured',
            '🤢': 'nauseated',
            '🤮': 'vomiting',
            '🤧': 'sneezing',
            '😵': 'dizzy',
            '🤯': 'mind blown',
            '🤠': 'cowboy',
            '🥳': 'party',
            '😎': 'cool',
            '🤓': 'nerd',
            '🧐': 'monocle',
            '😕': 'confused',
            '😟': 'worried',
            '🙁': 'slightly frowning',
            '☹️': 'frowning',
            '😮': ':O',
            '😯': ':O',
            '😲': 'shocked',
            '😳': 'flushed',
            '🥺': 'pleading',
            '😦': ':O',
            '😧': 'anguished',
            '😨': 'fearful',
            '😰': 'anxious',
            '😥': 'sad but relieved',
            '😢': 'crying',
            '😭': 'sobbing',
            '😱': 'screaming',
            '😖': 'confounded',
            '😣': 'persevering',
            '😞': 'disappointed',
            '😓': 'downcast',
            '😩': 'weary',
            '😫': 'tired',
            '🥱': 'yawning',
            '😤': 'triumph',
            '😡': 'angry',
            '😠': 'angry',
            '🤬': 'cursing',
            '😈': 'smiling imp',
            '👿': 'imp',
            '💀': 'skull',
            '☠️': 'skull and crossbones',
            '💩': 'poop',
            '🤡': 'clown',
            '👹': 'ogre',
            '👺': 'goblin',
            '👻': 'ghost',
            '👽': 'alien',
            '👾': 'alien monster',
            '🤖': 'robot',
            '😺': ':)',
            '😸': ':D',
            '😹': "'.",
            '😻': '<3',
            '😼': 'smirking cat',
            '😽': 'kissing cat',
            '🙀': 'shocked cat',
            '😿': 'crying cat',
            '😾': 'pouting cat',
            '❤️': '<3',
            '🧡': '<3',
            '💛': '<3',
            '💚': '<3',
            '💙': '<3',
            '💜': '<3',
            '🖤': '<3',
            '🤍': '<3',
            '🤎': '<3',
            '💔': '</3',
            '❣️': '<3',
            '💕': '<3<3',
            '💞': '<3<3',
            '💓': '<3',
            '💗': '<3',
            '💖': '<3',
            '💘': '<3',
            '💝': '<3',
            '⭐': '*',
            '🌟': '*',
            '✨': 'sparkles',
            '⚡': 'zap',
            '🔥': 'fire',
            '💯': '100',
            '💢': 'anger',
            '💥': 'boom',
            '💫': 'dizzy',
            '💦': 'sweat',
            '💨': 'dash',
            '🕳️': 'hole',
            '💣': 'bomb',
            '💬': 'speech bubble',
            '👍': 'thumbs up',
            '👎': 'thumbs down',
            '👏': 'clap',
            '🙌': 'raised hands',
            '🙏': 'pray',
            '💪': 'muscle',
            '🤝': 'handshake',
            '✍️': 'writing',
            '💅': 'nail polish',
            '🤳': 'selfie',
            '💃': 'dancer',
            '🕺': 'man dancing',
            '👯': 'people dancing',
            '🕴️': 'levitating',
            '🧘': 'meditating',
            '🧘‍♂️': 'man meditating',
            '🧘‍♀️': 'woman meditating',
            '🏃': 'running',
            '🏃‍♂️': 'man running',
            '🏃‍♀️': 'woman running',
            '👫': 'couple',
            '👭': 'two women',
            '👬': 'two men',
            '💑': 'couple with heart',
            '💏': 'kiss',
            '👪': 'family',
            '🗣️': 'speaking',
            '👤': 'bust',
            '👥': 'busts',
            '👣': 'footprints',
            '🌂': 'umbrella',
            '☂️': 'umbrella',
            '☔': 'umbrella with rain',
            '⚡': 'high voltage',
            '❄️': 'snowflake',
            '☃️': 'snowman',
            '⛄': 'snowman without snow',
            '☄️': 'comet',
            '🔥': 'fire',
            '💧': 'droplet',
            '🌊': 'water wave',
            '🎉': 'party popper',
            '🎊': 'confetti ball',
            '🎁': 'gift',
            '🎈': 'balloon',
            '🌹': 'rose',
            '🌸': 'cherry blossom',
            '🌺': 'hibiscus',
            '🌻': 'sunflower',
            '🌼': 'blossom',
            '🌷': 'tulip',
            '💐': 'bouquet',
            '🌱': 'seedling',
            '🌲': 'evergreen tree',
            '🌳': 'deciduous tree',
            '🌴': 'palm tree',
            '🌵': 'cactus',
            '🌾': 'sheaf of rice',
            '🌿': 'herb',
            '☘️': 'shamrock',
            '🍀': 'four leaf clover',
            '🍁': 'maple leaf',
            '🍂': 'fallen leaf',
            '🍃': 'leaf fluttering',
            '🍄': 'mushroom',
            '🌰': 'chestnut',
            '🦀': 'crab',
            '🦞': 'lobster',
            '🦐': 'shrimp',
            '🦑': 'squid',
            '🌍': 'earth europe',
            '🌎': 'earth americas',
            '🌏': 'earth asia',
            '🌐': 'globe with meridians',
            '🌑': 'new moon',
            '🌒': 'waxing crescent',
            '🌓': 'first quarter',
            '🌔': 'waxing gibbous',
            '🌕': 'full moon',
            '🌖': 'waning gibbous',
            '🌗': 'last quarter',
            '🌘': 'waning crescent',
            '🌙': 'crescent moon',
            '🌚': 'new moon face',
            '🌛': 'first quarter face',
            '🌜': 'last quarter face',
            '☀️': 'sun',
            '🌝': 'full moon face',
            '🌞': 'sun with face',
            '⭐': 'star',
            '🌟': 'glowing star',
            '🌠': 'shooting star',
            '☁️': 'cloud',
            '⛅': 'sun behind cloud',
            '⛈️': 'cloud with lightning',
            '🌤️': 'sun behind small cloud',
            '🌥️': 'sun behind large cloud',
            '🌦️': 'sun behind rain cloud',
            '🌧️': 'cloud with rain',
            '🌨️': 'cloud with snow',
            '🌩️': 'cloud with lightning',
            '🌪️': 'tornado',
            '🌫️': 'fog',
            '🌬️': 'wind face',
            '🌀': 'cyclone',
            '🌈': 'rainbow',
            '🌂': 'closed umbrella',
        }
        
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, f' {replacement} ')
        
        # Clean up any double spaces created
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

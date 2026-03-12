"""Weekly Pulse Scheduler - Runs at 5 PM and 9 PM for testing."""

import schedule
import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Add phase directories to path
sys.path.insert(0, str(Path(__file__).parent / "phase1"))
sys.path.insert(0, str(Path(__file__).parent / "phase2"))
sys.path.insert(0, str(Path(__file__).parent / "phase3"))
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def run_pipeline():
    """Run the complete pipeline: Collect -> Process -> Analyze -> Email."""
    print(f"\n{'='*60}")
    print(f"Starting Weekly Pulse Pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        # Step 1: Collect new reviews (last 7 days)
        print("📥 Step 1: Collecting reviews from Play Store...")
        from phase1.src.collectors.play_store import PlayStoreCollector
        collector = PlayStoreCollector(
            app_id="com.nextbillion.groww",
            weeks_to_collect=2,
            min_rating=1,
            max_rating=2
        )
        reviews = collector.collect_recent(days=7)
        print(f"   ✓ Collected {len(reviews)} new reviews")
        
        # Step 2: Process reviews
        print("\n🔧 Step 2: Processing reviews...")
        from phase2.src.processors.sanitizer import PIISanitizer
        from phase2.src.processors.normalizer import TextNormalizer
        from phase2.src.processors.filters import ReviewFilter
        
        sanitizer = PIISanitizer()
        normalizer = TextNormalizer()
        filter_processor = ReviewFilter()
        
        processed = []
        for review in reviews:
            review['text'] = sanitizer.sanitize(review['text'])
            review['text'] = normalizer.normalize(review['text'])
            if filter_processor.is_english(review['text']):
                processed.append(review)
        print(f"   ✓ Processed {len(processed)} reviews")
        
        # Step 3: Analyze with Groq
        print("\n🤖 Step 3: Analyzing with Groq LLM...")
        from phase3.src.analyzers.theme_analyzer import ThemeAnalyzer
        from phase3.src.analyzers.quote_extractor import QuoteExtractor
        from phase3.src.analyzers.action_generator import ActionGenerator
        from phase3.src.generators.pulse_report import PulseReportGenerator
        
        import os
        os.chdir(Path(__file__).parent / "phase3")
        
        theme_analyzer = ThemeAnalyzer()
        quote_extractor = QuoteExtractor()
        action_generator = ActionGenerator()
        report_generator = PulseReportGenerator()
        
        themes = theme_analyzer.analyze(processed)
        quotes = quote_extractor.extract(processed, themes)
        actions = action_generator.generate(themes)
        
        report = report_generator.generate(themes, quotes, actions, len(processed))
        print(f"   ✓ Generated report with {len(themes)} themes, {len(quotes)} quotes, {len(actions)} actions")
        
        # Step 4: Send email
        print("\n📧 Step 4: Sending email report...")
        from backend.app.core.config import get_settings
        from backend.app.api.email import send_email_via_smtp, generate_email_content
        
        settings = get_settings()
        email_body = generate_email_content(report)
        
        # Get recipient from environment or use smtp_user as fallback
        import os
        recipient = os.getenv('RECIPIENT_EMAIL', settings.smtp_user)
        
        # Send to configured email
        send_email_via_smtp(
            to_email=recipient,
            subject=f"Weekly Pulse - Groww Reviews ({datetime.now().strftime('%Y-%m-%d')})",
            html_body=email_body,
            settings=settings
        )
        print(f"   ✓ Email sent to {recipient}")
        
        print(f"\n{'='*60}")
        print(f"Pipeline completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point - runs pipeline once (for GitHub Actions)."""
    print("\n" + "="*60)
    print("Groww Reviews Weekly Pulse Scheduler")
    print("="*60)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Running pipeline once...\n")
    
    # Run pipeline immediately (GitHub Actions handles the scheduling)
    run_pipeline()

if __name__ == "__main__":
    main()

# Groww Reviews Weekly Pulse - Architecture Document

## Overview
A system that aggregates **Play Store reviews only** from the Groww app (https://play.google.com/store/apps/details?id=com.nextbillion.groww) from the last 8-12 weeks, analyzes them using Groq LLM, and generates a weekly one-page pulse report with themes, user quotes, and actionable insights.

---

## Phase 1: Data Ingestion Layer

### 1.1 Review Collection
**Components:**
- `PlayStoreCollector` - Android Play Store review fetcher

**Data Source:**
- Play Store: Google Play Scraper library (public data)
- **App URL:** https://play.google.com/store/apps/details?id=com.nextbillion.groww&hl=en_IN
- **App ID:** `com.nextbillion.groww`

**Output Schema:**
```json
{
  "review_id": "string",
  "source": "playstore",
  "rating": 1-5,
  "title": "string",
  "text": "string",
  "date": "ISO8601",
  "version": "string",
  "language": "string"
}
```

**Constraints:**
- Collect reviews from last 8-12 weeks only
- Filter for English reviews (configurable)
- No PII collection (strip usernames, emails, device IDs)
- **Play Store only** - No App Store integration needed

---

## Phase 2: Data Processing Layer

### 2.1 Data Cleaning & Normalization
**Components:**
- `PIISanitizer` - Removes personally identifiable information
- `TextNormalizer` - Standardizes text encoding, handles emojis
- `DuplicateDetector` - Removes duplicate/similar reviews

### 2.2 Review Storage
**Options:**
- SQLite (local, lightweight)
- JSON files (simple, version controlled)
- PostgreSQL (if scaling needed)

**Schema:**
```sql
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL DEFAULT 'playstore',
    rating INTEGER NOT NULL,
    title TEXT,
    text TEXT NOT NULL,
    review_date DATE NOT NULL,
    app_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Phase 3: Analysis Layer (Groq LLM Integration)

### 3.1 Theme Extraction
**Component:** `ThemeAnalyzer`

**Prompt Strategy:**
```
Analyze the following app reviews and identify up to 5 major themes.
Themes should cover areas like: onboarding, KYC, payments, statements, 
withdrawals, UI/UX, performance, customer support.

Reviews: {reviews_json}

Return JSON format:
{
  "themes": [
    {
      "name": "theme_name",
      "description": "brief description",
      "review_count": number,
      "avg_rating": number,
      "sentiment": "positive|negative|mixed"
    }
  ]
}
```

**Model:** llama-3.1-70b-versatile (or mixtral-8x7b-32768)

### 3.2 Quote Extraction
**Component:** `QuoteExtractor`

Extracts 3 representative user quotes per top theme that are:
- Concise and impactful
- Anonymous (no PII)
- Representative of the theme

### 3.3 Action Idea Generation
**Component:** `ActionGenerator`

Generates 3 actionable recommendations based on themes and sentiment analysis.

---

## Phase 4: Report Generation Layer

### 4.1 Weekly Pulse Generator
**Component:** `PulseReportGenerator`

**Output Format:**
```markdown
# Weekly Pulse - Week of [Date]

## Top 3 Themes
1. **Theme Name** - X mentions, Avg Rating: Y
2. **Theme Name** - X mentions, Avg Rating: Y
3. **Theme Name** - X mentions, Avg Rating: Y

## User Voices
> "Quote 1..." - Theme context
> "Quote 2..." - Theme context
> "Quote 3..." - Theme context

## Suggested Actions
1. **Action 1** - Brief explanation
2. **Action 2** - Brief explanation
3. **Action 3** - Brief explanation

---
*Generated from X Play Store reviews*
```

**Constraints:**
- Max 250 words
- Scannable format with clear headings
- No PII (verified via post-processing)

---

## Phase 5: Web Application Layer (NEW)

### 5.1 Backend API
**Technology:** Python FastAPI

**Components:**
- `ReviewAPI` - Endpoints to fetch processed reviews
- `ReportAPI` - Endpoints to get generated reports
- `EmailAPI` - Endpoint to send email from UI
- `AnalysisAPI` - Trigger analysis pipeline

**Endpoints:**
```
GET  /api/reviews          - List processed reviews
GET  /api/reports          - List generated reports
GET  /api/reports/{id}     - Get specific report
POST /api/reports/{id}/send-email  - Send report via email
POST /api/analyze          - Trigger new analysis
GET  /api/stats            - Get review statistics
```

**Email Service Integration:**
- SMTP (Gmail, Outlook, etc.)
- SendGrid API
- Mailgun API

### 5.2 Frontend Dashboard
**Technology:** React + Vite

**Components:**
- `Dashboard` - Overview of reviews and stats
- `ReportViewer` - View generated pulse reports
- `EmailComposer` - Compose and send email from UI
- `ReviewBrowser` - Browse filtered reviews
- `AnalysisTrigger` - Button to trigger new analysis

**Features:**
- View weekly pulse reports (Markdown rendered)
- Send email with report to any recipient
- Browse review database
- Trigger on-demand analysis
- View analysis history

**Pages:**
- `/` - Dashboard (stats + latest report)
- `/reports` - List all reports
- `/reports/{id}` - View specific report
- `/reviews` - Browse reviews
- `/settings` - Configure email settings

---

## Phase 6: Delivery Layer

### 6.1 Email Draft Generator
**Component:** `EmailDraftGenerator`

**Features:**
- Generates email-ready HTML/text
- Pre-fills subject line: "Weekly Pulse - Groww Reviews [Date Range]"
- Configurable recipient (self/alias)

### 6.2 Email Service Integration
**Options:**
- SMTP (Gmail, Outlook, etc.)
- SendGrid API
- Mailgun API

**Configuration:**
```json
{
  "email": {
    "provider": "smtp|sendgrid|mailgun",
    "from_address": "pulse@groww-reviews.local",
    "to_address": "user@example.com",
    "subject_template": "Weekly Pulse - Groww Reviews {week_range}"
  }
}
```

---

## Phase 7: Orchestration & Scheduling

### 7.1 Workflow Orchestrator
**Component:** `WeeklyPulseWorkflow`

**Steps:**
1. Fetch reviews (last 8-12 weeks)
2. Clean and store reviews
3. Run theme analysis (Groq)
4. Extract quotes (Groq)
5. Generate actions (Groq)
6. Compile pulse report
7. Draft and send email

### 7.2 Scheduling
**Options:**
- Cron job (Linux/Mac)
- Windows Task Scheduler
- GitHub Actions (weekly schedule)
- Python schedule library

**Recommended:** Weekly run (e.g., Monday 9 AM)

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| LLM | Groq API |
| Data Storage | SQLite / JSON |
| HTTP Client | httpx / requests |
| Email | smtplib / sendgrid-python |
| Scheduling | schedule / cron |
| Config | pydantic-settings |
| Logging | structlog |
| **Backend** | **FastAPI** |
| **Frontend** | **React + Vite** |
| **UI Components** | **Tailwind CSS** |

---

## Project Structure

```
groww-reviews-pulse/
├── phase1/                  # Data Collection (CLI)
│   ├── src/collectors/
│   ├── data/
│   └── main.py
├── phase2/                  # Data Processing (CLI)
│   ├── src/processors/
│   ├── data/
│   └── main.py
├── phase3/                  # Analysis (CLI)
│   ├── src/analyzers/
│   ├── outputs/
│   └── main.py
├── backend/                 # NEW: FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── reviews.py
│   │   │   ├── reports.py
│   │   │   └── email.py
│   │   ├── core/
│   │   │   └── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # NEW: React Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── reviews.db           # SQLite database
├── outputs/
│   └── weekly_pulses/       # Generated reports
├── tests/
├── .env                     # Environment variables
└── docker-compose.yml       # NEW: Orchestrate all services
```

---

## Environment Configuration

```bash
# Groq API
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-70b-versatile

# App Configuration
APP_NAME=Groww
PLAYSTORE_APP_ID=com.nextbillion.groww
PLAYSTORE_URL=https://play.google.com/store/apps/details?id=com.nextbillion.groww&hl=en_IN

# Review Collection
WEEKS_TO_COLLECT=10
MIN_RATING=1
MAX_RATING=5

# Email
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_TO=recipient@example.com

# Output
MAX_THEMES=5
MAX_WORDS=250
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1) - DATA COLLECTION
**Goal:** Collect and store Play Store reviews in database

**Implementation:**
- [x] Project setup and dependencies
- [x] Play Store review collector (google-play-scraper)
- [x] PII sanitizer and text normalizer
- [x] Data storage layer (SQLite)
- [x] Basic CLI interface

**Execution (Part of Phase 1):**
- [x] Install dependencies: `pip install -r requirements.txt`
- [x] Run collection: `python main.py collect`
- [x] Verify data in `phase1/data/reviews.db`

**Output:**
- SQLite database with reviews table
- Collection metadata tracking
- 50+ reviews stored with PII sanitized

### Phase 2: Analysis (Week 2)
- [ ] Groq LLM integration
- [ ] Theme extraction
- [ ] Quote extraction
- [ ] Action generation

### Phase 3: Reporting (Week 3)
- [ ] Pulse report generator
- [ ] Email draft generation
- [ ] Email service integration

### Phase 4: Automation (Week 4)
- [ ] Workflow orchestration
- [ ] Scheduling setup
- [ ] Error handling & logging
- [ ] Testing & validation

---

## Constraints Checklist

- [x] Public review exports only (no scraping behind logins)
- [x] Max 5 themes
- [x] Notes scannable, ≤250 words
- [x] No usernames/emails/IDs in artifacts
- [x] PII sanitization at ingestion
- [x] Anonymous quotes only

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| API rate limits | Implement exponential backoff |
| LLM hallucination | Use structured output, validation |
| PII leakage | Multi-layer sanitization, regex patterns |
| Data freshness | Timestamp validation, deduplication |
| Email delivery | Retry logic, fallback providers |

# Groww Reviews Weekly Pulse

An automated system that analyzes Play Store reviews for Groww app using Groq LLM and generates weekly pulse reports with themes, user quotes, and actionable insights.

---

## How to Re-run for a New Week

### Automatic Execution
The system runs automatically every **Monday at 9:00 AM IST** via GitHub Actions scheduler.

### Manual Execution

If you need to manually trigger the analysis for a new week:

#### Option 1: Via GitHub Actions (Recommended)
1. Go to the repository's **Actions** tab
2. Select **"Weekly Pulse Report"** workflow
3. Click **"Run workflow"** button
4. The workflow will execute all phases and generate the report

#### Option 2: Local Execution
```bash
# Navigate to project root
cd groww-reviews-pulse

# Run Phase 1: Data Collection
python phase1/main.py collect

# Run Phase 2: Data Processing  
python phase2/main.py process

# Run Phase 3: LLM Analysis & Report Generation
python phase3/main.py analyze --weeks 10

# View output in:
# - phase3/outputs/weekly_pulse.json
# - phase3/outputs/weekly_pulse.md
# - phase3/outputs/weekly_pulse.txt
```

#### Option 3: Trigger Email Manually
1. Open the Streamlit app on Streamlit Cloud
2. Click **"↻ Refresh Analysis"** to load latest data
3. Use the **"Send Report"** panel on the right
4. Enter recipient email and click **"Send Report"**

---

## Theme Legend

The system identifies common themes from user reviews. Here are the key theme categories:

### 🔥 Performance & Stability
- **App Performance** - Speed, lag, crashes, freezing issues
- **Technical Issues** - Bugs, errors, functionality problems

### ⚡ Features & Functionality  
- **Withdrawal Issues** - Problems withdrawing funds or securities
- **KYC Verification** - Know Your Customer onboarding challenges
- **Payment Problems** - Payment failures, transaction issues
- **External Funds** - Fetching holdings from other platforms

### 💡 User Experience
- **UI/UX Design** - Interface usability, navigation concerns
- **Customer Support** - Response time, support quality
- **Account Management** - Login, profile, settings issues

### 📊 Trading & Investment
- **Order Execution** - Buy/sell order placement and confirmation
- **Brokerage Charges** - Fees, charges, pricing concerns
- **Portfolio Management** - Holdings display, tracking issues

### Other Common Themes
- **Onboarding** - New user registration and setup
- **Notifications** - Alerts, updates, communication preferences
- **Security** - Account safety, authentication concerns

---

## Output Files

After each run, the following files are generated:

- `phase3/outputs/weekly_pulse.json` - Structured data (used by UI)
- `phase3/outputs/weekly_pulse.md` - Markdown report
- `phase3/outputs/weekly_pulse.txt` - Plain text summary

---

## Technology Stack

- **Data Source**: Google Play Store Reviews
- **LLM Provider**: Groq API (llama-3.3-70b-versatile)
- **Automation**: GitHub Actions (weekly scheduler)
- **Frontend**: Streamlit Cloud
- **Email**: Gmail SMTP

---

## Configuration

Key environment variables (stored in `.env`):

```bash
GROQ_API_KEY=your_api_key
PLAYSTORE_APP_ID=com.nextbillion.groww
WEEKS_TO_COLLECT=10
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

---

## Support

For issues or questions, please raise an issue on the GitHub repository.

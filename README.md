# Groww Reviews Weekly Pulse

An automated dashboard and data pipeline that analyzes Play Store reviews for the Groww app using the Groq LLM. It generates weekly pulse reports with themes, user quotes, and actionable insights.

---

## How to Re-run for a New Week

The data pipeline collects new reviews, processes them, analyzes them with the LLM, and updates the dashboard data.

### 1. Automatic Execution
The system is designed to run automatically every **Monday at 9:00 AM IST** via a GitHub Actions scheduled workflow (`.github/workflows/weekly_pulse.yml`).

### 2. Manual Execution via GitHub Actions (Recommended)
If you need to manually trigger the analysis for a new week without waiting for Monday:
1. Go to the repository's **Actions** tab on GitHub.
2. Select the **"Weekly Pulse Report"** workflow on the left sidebar.
3. Click the **"Run workflow"** button on the right.
4. The workflow will execute all phases and commit the new `weekly_pulse.json` to the repo. Streamlit Cloud will automatically pick up the new data.

### 3. Local Execution
To run the entire pipeline locally on your machine and update the local database:

```bash
# Navigate to the project root directory
cd groww-reviews-pulse

# Run the master scheduler script to execute the entire pipeline
# (Collection -> Processing -> Analysis)
python scheduler.py
```

Once `scheduler.py` finishes, the new report data will be saved to `phase3/outputs/weekly_pulse.json`. If your Streamlit app is running locally, the new data will be available immediately.

---

## Theme Legend

The LLM identifies common themes from the user reviews. Here are the key theme categories that power the dashboard:

### 🔥 Performance & Stability
- **App Performance** - Speed, lag, crashes, and freezing issues.
- **Technical Issues** - Bugs, errors, and app functionality problems.

### ⚡ Features & Functionality  
- **Withdrawal Issues** - Problems withdrawing funds, money stuck.
- **KYC Verification** - Onboarding and verification challenges.
- **Payment Problems** - Payment failures, UPI issues, transaction errors.
- **External Funds** - Fetching holdings from other platforms.

### 💡 User Experience
- **UI/UX Design** - Interface usability, navigation concerns, and layout.
- **Customer Support** - Response time and support agent quality.
- **Account Management** - Login, profile, and account settings issues.

### 📊 Trading & Investment
- **Order Execution** - Buy/sell order placement, confirmation delays.
- **Brokerage Charges** - Hidden fees, high charges, and pricing concerns.
- **Portfolio Management** - Holdings display, P&L accuracy, and tracking.

### 📌 Other Common Themes
- **Onboarding** - New user registration and setup friction.
- **Notifications** - Missing alerts, delayed updates.
- **Security** - Account safety and authentication concerns.

---

## Technology Stack

- **Data Source**: Google Play Store (`google-play-scraper`)
- **LLM Provider**: Groq API (`llama-3.3-70b-versatile`)
- **Automation**: GitHub Actions (weekly scheduler)
- **Frontend**: Streamlit Cloud
- **Email Delivery**: Standard SMTP

## Configuration

To run locally, you need a `.env` file in the `backend/` directory with the following variables:

```bash
# Required
GROQ_API_KEY=your_groq_api_key

# Optional Email Configuration (for the Send Report feature)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

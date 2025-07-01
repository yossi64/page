# Credentials Setup Instructions

## Quick Setup for Embedded Credentials

To embed your API credentials directly in the system (as requested), follow these steps:

### Option 1: Environment Variables (Recommended for Security)
Set these environment variables before running the system:

```bash
export GOOGLE_ADS_CUSTOMER_ID="YOUR_CUSTOMER_ID"
export GOOGLE_ADS_DEVELOPER_TOKEN="YOUR_DEVELOPER_TOKEN"
export GOOGLE_ADS_CLIENT_ID="YOUR_CLIENT_ID"
export GOOGLE_ADS_CLIENT_SECRET="YOUR_CLIENT_SECRET"
export GOOGLE_ADS_REFRESH_TOKEN="YOUR_REFRESH_TOKEN"
export GOOGLE_ADS_LOGIN_CUSTOMER_ID="YOUR_LOGIN_CUSTOMER_ID"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export PEXELS_API_KEY="YOUR_PEXELS_API_KEY"
```

### Option 2: Direct Embedding (Less Secure)
If you prefer to embed credentials directly in the code:

1. Open `config/config.py`
2. Replace the placeholder values with your actual API keys:
   - Replace `"YOUR_DEVELOPER_TOKEN_HERE"` with your Google Ads developer token
   - Replace `"YOUR_CLIENT_ID_HERE"` with your Google Ads OAuth client ID
   - Replace `"YOUR_CLIENT_SECRET_HERE"` with your Google Ads OAuth client secret
   - Replace `"YOUR_REFRESH_TOKEN_HERE"` with your Google Ads OAuth refresh token
   - Replace `"YOUR_OPENAI_API_KEY_HERE"` with your OpenAI API key
   - Replace `"YOUR_PEXELS_API_KEY_HERE"` with your Pexels API key

### Option 3: Create Local Environment File
Create a `.env` file in the project root with:

```
GOOGLE_ADS_CUSTOMER_ID=YOUR_CUSTOMER_ID
GOOGLE_ADS_DEVELOPER_TOKEN=YOUR_DEVELOPER_TOKEN
GOOGLE_ADS_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_ADS_CLIENT_SECRET=YOUR_CLIENT_SECRET
GOOGLE_ADS_REFRESH_TOKEN=YOUR_REFRESH_TOKEN
GOOGLE_ADS_LOGIN_CUSTOMER_ID=YOUR_LOGIN_CUSTOMER_ID
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
PEXELS_API_KEY=YOUR_PEXELS_API_KEY
```

## Business Configuration
The system is pre-configured for:
- **Business**: Air Cleaning Tech LLC
- **Phone**: (210) 873-0584
- **Service Area**: San Antonio, TX
- **Google Ads Account**: 8246122588

## Quick Start
After setting up credentials:
```bash
pip install -r requirements.txt
python run_system.py
```

Choose Option 1 for the full integrated workflow that connects campaign creation with landing page generation.

# Reddit Bot Setup Instructions

## 🚀 Getting Reddit API Credentials (FREE)

### Step 1: Go to Reddit Apps
1. Visit: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"

### Step 2: Create App
- **Name:** RISA_Framework_Bot
- **Type:** Script
- **Description:** Bot for posting RISA Framework announcements
- **About URL:** https://github.com/Nemeca99/Unified-Theory-of-UML
- **Redirect URI:** http://localhost:8080

### Step 3: Get Credentials
After creating the app, you'll get:
- **Client ID:** (under the app name, looks like: `abc123def456`)
- **Client Secret:** (click "secret" to reveal)

### Step 4: Update Bot Script
Replace in `reddit_bot.py`:
```python
"client_id": "YOUR_CLIENT_ID_HERE",  # Replace with your client ID
"client_secret": "YOUR_CLIENT_SECRET_HERE",  # Replace with your client secret
```

### Step 5: Install Dependencies
```bash
pip install praw
```

### Step 6: Run the Bot
```bash
python reddit_bot.py
```

## 🎯 What the Bot Does

The bot will automatically post to:
- **r/math** - Mathematical breakthrough announcement
- **r/physics** - Physics and consciousness framework
- **r/Python** - Python package showcase

## ⚠️ Important Notes

- **Rate Limiting:** Bot waits 30 seconds between posts
- **Free:** Reddit API is completely free for this usage
- **Safe:** Uses your existing Reddit account
- **Reversible:** You can delete posts if needed

## 🚀 Launch Sequence

1. Get Reddit API credentials (5 minutes)
2. Update the bot script with credentials
3. Run the bot
4. Your revolutionary work goes live to millions of scientists!

**The impossible will be made visible to the world!** 🔥 
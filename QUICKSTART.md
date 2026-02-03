# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install requests pandas matplotlib numpy
```

### Step 2: Run the Complete Analysis
```bash
python run_analysis.py
```

That's it! This will:
1. Fetch all videos from Jomboy Media's channel
2. Save the data to CSV and JSON files
3. Generate 5 visualization charts
4. Display summary statistics

### Step 3: View Your Results

**Data files** (in `data/` folder):
- `jomboy_videos_YYYYMMDD_HHMMSS.csv` - Spreadsheet format
- `jomboy_videos_YYYYMMDD_HHMMSS.json` - Full data structure

**Visualizations** (in `visualizations/` folder):
- `views_over_time.png` - Shows cumulative views and per-video performance
- `upload_frequency.png` - Monthly upload patterns
- `growth_rate.png` - Month-over-month growth percentage
- `engagement_analysis.png` - Likes vs views and engagement rates
- `top_videos.png` - Top 15 most viewed videos

---

## 🎯 Alternative: Run Steps Separately

If you want more control:

### Fetch data only:
```bash
python youtube_analytics.py
```

### Generate visualizations from existing data:
```bash
python visualize.py data/jomboy_videos_20260122_143000.csv
```

Or auto-detect the most recent file:
```bash
python visualize.py
```

---

## 🔄 Track Growth Over Time

Run the analysis weekly or monthly to track trends:

```bash
# Week 1
python run_analysis.py

# Week 2  
python run_analysis.py

# Week 3
python run_analysis.py
```

Each run creates timestamped files so you can compare historical data.

---

## ⚙️ Change Settings

Edit the configuration at the top of `youtube_analytics.py` or `run_analysis.py`:

```python
API_KEY = "your_api_key_here"
CHANNEL_HANDLE = "@YourChannel"
```

---

## 🛠️ Troubleshooting

**"Module not found" error?**
```bash
pip install requests pandas matplotlib numpy
```

**"Invalid API key"?**
- Double-check your API key
- Make sure YouTube Data API v3 is enabled in Google Cloud Console

**Want to analyze a different channel?**
- Change `CHANNEL_HANDLE = "@JomboyMedia"` to your target channel

---

## 📊 Understanding the Visualizations

1. **Views Over Time**: 
   - Top chart: Total cumulative views across all videos
   - Bottom chart: Views for each individual video (scatter plot)

2. **Upload Frequency**: 
   - Bar chart showing how many videos were uploaded each month
   - Blue dashed line shows the average

3. **Growth Rate**: 
   - Top: Total views from videos published each month
   - Bottom: Percentage change month-over-month (green = growth, red = decline)

4. **Engagement Analysis**:
   - Left: Scatter plot of likes vs views (shows if engagement is consistent)
   - Right: Engagement rate over time (likes + comments per view)

5. **Top Videos**: 
   - Horizontal bar chart of the most viewed videos

---

## 💡 Tips

- Run the analysis after major video releases to see immediate impact
- Compare monthly snapshots to identify seasonal trends
- Use the CSV data in Excel/Google Sheets for custom analysis
- The JSON file contains full video descriptions if you want text analysis

---

## 🔒 Security Reminder

After testing, you should:
1. Regenerate your API key (this one was posted publicly)
2. Store your new key in an environment variable or config file
3. Add that config file to `.gitignore` if using git

---

**Need help?** The main README.md has more detailed documentation!

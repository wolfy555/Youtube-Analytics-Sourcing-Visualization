# YouTube Channel Analytics Tool

Analyze and visualize growth metrics for YouTube channels, including view counts, engagement rates, and upload patterns.

## Features

- Fetches all videos from a YouTube channel
- Tracks views, likes, comments, and publication dates
- Generates comprehensive visualizations:
  - Cumulative views over time
  - Upload frequency analysis
  - Month-over-month growth rates
  - Engagement analysis
  - Top performing videos
- Saves data in CSV and JSON formats for further analysis

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a YouTube API Key

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Copy your API key

### 3. Configure the Script

Edit `youtube_analytics.py` and update:
- `API_KEY`: Your YouTube Data API key
- `CHANNEL_HANDLE`: The channel you want to analyze (e.g., "@JomboyMedia")

## Usage

### Step 1: Fetch Channel Data

```bash
python youtube_analytics.py
```

This will:
- Fetch all videos from the channel
- Save data to timestamped CSV and JSON files
- Display channel statistics

Output files:
- `jomboy_videos_YYYYMMDD_HHMMSS.csv`
- `jomboy_videos_YYYYMMDD_HHMMSS.json`

### Step 2: Generate Visualizations

```bash
python visualize.py jomboy_videos_YYYYMMDD_HHMMSS.csv
```

Or simply run without arguments to automatically use the most recent CSV:

```bash
python visualize.py
```

This will generate:
- `views_over_time.png` - Cumulative and per-video view trends
- `upload_frequency.png` - Upload patterns by month
- `growth_rate.png` - Month-over-month growth analysis
- `engagement_analysis.png` - Likes vs views and engagement rates
- `top_videos.png` - Top 15 most viewed videos
- Console summary with key statistics

## Tracking Over Time

To track channel growth over time:

1. Run `youtube_analytics.py` regularly (daily/weekly)
2. Keep all the timestamped CSV files
3. Compare metrics across different snapshots

You can modify the visualization script to compare multiple CSV files and show trends.

## API Quota

The YouTube Data API has a free quota of 10,000 units per day:
- Fetching channel info: ~3 units
- Fetching 50 videos: ~1 unit
- This tool typically uses 20-50 units for a complete fetch

A channel with 1,000 videos will use approximately 50 units per run.

## Security Note

⚠️ **Important**: Never commit your API key to version control!

- Add `youtube_analytics.py` to `.gitignore` after adding your API key
- Or use environment variables to store your API key

## Customization

### Change Channel

Edit `youtube_analytics.py`:
```python
CHANNEL_HANDLE = "@YourChannelHere"
```

### Adjust Visualizations

The `visualize.py` script can be customized:
- Change colors, sizes, and styles
- Add new metrics and plots
- Modify date ranges for analysis

### Export Options

Data is saved in both CSV and JSON formats:
- **CSV**: Easy to open in Excel/Google Sheets
- **JSON**: Preserves full data structure for custom analysis

## Troubleshooting

### "Invalid API key"
- Check that your API key is correct
- Ensure YouTube Data API v3 is enabled in Google Cloud Console

### "Quota exceeded"
- Wait until the next day (quota resets at midnight Pacific Time)
- Or request a quota increase in Google Cloud Console

### No videos fetched
- Verify the channel handle is correct (with or without @)
- Check that the channel is public

## Example Output

```
📺 Channel Found: Jomboy Media
   Subscribers: 1,234,567
   Total Videos: 1,234
   Total Views: 123,456,789

🔍 Fetching videos...
   Fetched 50 videos so far...
   Fetched 100 videos so far...
✅ Total videos fetched: 1,234

💾 Data saved to jomboy_videos_20260122_143022.csv
💾 Data saved to jomboy_videos_20260122_143022.json
```

## License

MIT License - Feel free to use and modify as needed!

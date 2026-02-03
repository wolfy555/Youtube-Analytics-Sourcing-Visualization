# Channel Comparison Analysis - Step-by-Step Guide

## Overview

You're comparing **Jomboy Media** (novelty-based sports content) vs **Bussin' With The Boys** (community-based podcast) to prove that different content types have different growth and retention patterns.

**Hypothesis:** Novelty-based content shows rapid growth decay and poor retention, while community-based content shows sustainable growth and better retention.

---

## What You'll Generate

### Individual Channel Analyses (for each channel):
1. `views_over_time.png` - Growth trajectory
2. `upload_frequency.png` - Upload patterns
3. `growth_rate.png` - Month-over-month changes
4. `engagement_analysis.png` - Engagement trends
5. `top_videos.png` - Top performers
6. `growth_decay_analysis.png` - Extrapolation vs reality
7. `mean_reversion_analysis.png` - Statistical decay patterns

### Comparison Charts (both channels together):
1. `comparison_growth_decay.png` - Side-by-side extrapolation analysis
2. `comparison_retention.png` - Views-per-video trends (retention proxy)
3. `comparison_growth_rates.png` - Growth rate decay comparison

### Statistical Report:
- Comparative metrics table
- Growth decay slopes
- Retention change percentages
- Volatility comparison
- Key findings summary

---

## Step-by-Step Instructions

### Phase 1: Collect Data for Bussin' With The Boys

**Step 1:** Make sure you're in your project folder with venv activated

```bash
cd "/Users/aidanwolf/Downloads/Jomboy Media Analysis Files Claude"
source venv/bin/activate
```

**Step 2:** Fetch Bussin' With The Boys data

```bash
python youtube_analytics.py --channel "@BussinWithTheBoys"
```

**What happens:**
- Fetches all videos from the channel
- Identifies subscriber count, total videos, total views
- Saves data as: `bussinwiththeboys_videos_YYYYMMDD_HHMMSS.csv` and `.json`
- Takes 2-5 minutes depending on video count

**Expected output:**
```
============================================================
YouTube Channel Analytics Tool
============================================================
Analyzing: @BussinWithTheBoys

📺 Channel Found: Bussin' With The Boys
   Subscribers: X,XXX,XXX
   Total Videos: X,XXX
   Total Views: XXX,XXX,XXX

🔍 Fetching videos...
   Fetched 50 videos so far...
   ...
✅ Total videos fetched: X,XXX
💾 Data saved to bussinwiththeboys_videos_20260127_XXXXXX.csv
💾 Data saved to bussinwiththeboys_videos_20260127_XXXXXX.json

============================================================
✅ Data collection complete!
============================================================
```

**Step 3:** Verify the data files exist

```bash
ls -lh *bussin*.csv
```

You should see the new CSV file.

---

### Phase 2: Generate Individual Channel Analyses

**Step 4:** Generate visualizations for Bussin' With The Boys

```bash
python visualize.py bussinwiththeboys_videos_20260127_XXXXXX.csv
```

(Replace `XXXXXX` with your actual timestamp)

**What happens:**
- Creates 7 visualization charts in `visualizations/` folder
- Generates summary statistics
- Takes 30-60 seconds

**Step 5:** Review Bussin' charts

In VS Code, open `visualizations/` folder and check:
- `growth_decay_analysis.png` - Shows their takeoff year and decay pattern
- `mean_reversion_analysis.png` - Shows retention trends
- All other standard charts

**Step 6:** (Optional) Regenerate Jomboy visualizations if needed

If you want fresh Jomboy charts with the new analysis:

```bash
python visualize.py data/jomboy_videos_20260127_134357.csv
```

---

### Phase 3: Generate Comparison Analysis

**Step 7:** Run the comparison script

```bash
python compare_channels.py \
    data/jomboy_videos_20260127_134357.csv \
    bussinwiththeboys_videos_20260127_XXXXXX.csv \
    --name1 "Jomboy Media" \
    --name2 "Bussin' With The Boys" \
    --output comparisons
```

**What happens:**
- Identifies takeoff years for both channels automatically
- Aligns data by "months since takeoff" for fair comparison
- Generates 3 comprehensive comparison charts
- Prints detailed statistical comparison report
- Saves everything to `comparisons/` folder
- Takes 1-2 minutes

**Expected output:**
```
================================================================================
YouTube Channel Comparison Tool
================================================================================
📊 Loading Jomboy Media data...
📊 Loading Bussin' With The Boys data...

✅ Loaded 3820 videos from Jomboy Media
✅ Loaded XXXX videos from Bussin' With The Boys

🚀 Jomboy Media takeoff year: 2019
🚀 Bussin' With The Boys takeoff year: XXXX

🎨 Generating comparison visualizations...
💾 Saved: comparisons/comparison_growth_decay.png
💾 Saved: comparisons/comparison_retention.png
💾 Saved: comparisons/comparison_growth_rates.png

================================================================================
📊 CHANNEL COMPARISON REPORT
================================================================================

METRIC                                   Jomboy Media         Bussin' With The Boys
--------------------------------------------------------------------------------
Total Videos                             3,820                X,XXX
Total Views                              1,720,536,591        XXX,XXX,XXX
Average Views per Video                  450,402              XXX,XXX
...

GROWTH DECAY ANALYSIS
--------------------------------------------------------------------------------
Growth Rate Decay Slope (%/month)        -X.XXX               -X.XXX
...

KEY FINDINGS
================================================================================
✓ Jomboy Media shows faster growth decay (-X.XXX%/mo vs -X.XXX%/mo)
✓ Jomboy Media has declining retention (-XX.X% change), Bussin' is more stable
✓ Jomboy Media shows significantly higher volatility (less sustainable)

================================================================================
```

---

### Phase 4: Review Your Results

**Step 8:** Open the comparison charts

In VS Code, navigate to `comparisons/` folder and open:

**A. `comparison_growth_decay.png`**
- Two panels side-by-side
- Left: Jomboy Media (red line = actual, green = extrapolation, yellow = gap)
- Right: Bussin' (same structure)
- **Key insight:** Which channel has a bigger yellow gap? That's the overestimation from extrapolating takeoff growth

**B. `comparison_retention.png`**
- Three panels:
  - Top: Views per video for both channels (aligned by takeoff)
  - Middle: Normalized retention index (both start at 100)
  - Bottom: Upload frequency comparison
- **Key insight:** Which line declines more steeply? That's worse retention

**C. `comparison_growth_rates.png`**
- Two panels:
  - Top: Rolling average growth rates overlaid (with decay trend lines)
  - Bottom: Growth volatility over time
- **Key insight:** Steeper negative slope = faster decay; Higher volatility = less sustainable

---

## Understanding Your Results

### What the Charts Will Prove:

**If your hypothesis is correct:**

1. **Growth Decay Chart** will show:
   - Jomboy: Large yellow gap (big overestimation from 2019 extrapolation)
   - BWTB: Smaller yellow gap (more sustainable growth)

2. **Retention Chart** will show:
   - Jomboy: Declining views-per-video trend (red line going down)
   - BWTB: Stable or growing views-per-video (blue line flat/up)

3. **Growth Rate Chart** will show:
   - Jomboy: Steeper negative decay slope
   - BWTB: Flatter or less negative decay slope
   - Jomboy: Higher volatility (less predictable)
   - BWTB: Lower volatility (more stable)

4. **Statistical Report** will show:
   - Jomboy retention change: Negative %
   - BWTB retention change: Positive or less negative %
   - Jomboy decay slope: More negative
   - BWTB decay slope: Less negative

### Quotes for Your Thesis:

From the statistical report, you can say:

> "Jomboy Media's growth rate decayed at -X.XX% per month post-takeoff, compared to Bussin' With The Boys at -X.XX% per month, demonstrating that novelty-based content experiences significantly faster mean reversion."

> "Views per video declined by X% for Jomboy Media from early to recent periods, while Bussin' With The Boys showed only X% decline, supporting the hypothesis that community-driven content maintains superior audience retention."

> "Extrapolating 2019 growth rates would have overestimated Jomboy's performance by X%, versus only X% for Bussin', indicating higher risk in valuation models based on viral takeoff periods."

---

## Troubleshooting

**Error: "Module not found"**
```bash
source venv/bin/activate
pip install pandas matplotlib numpy requests
```

**Error: "File not found"**
- Check the exact filename with `ls *.csv`
- Copy/paste the actual filename

**Charts look weird**
- Close and reopen PNG files in VS Code
- Or open in Finder: `open comparisons/`

**Script takes too long**
- Normal for channels with 2000+ videos
- Be patient, it's fetching all data from YouTube

---

## Next Steps After Completion

1. **Take screenshots** of key charts for your presentation
2. **Copy statistics** from the comparison report
3. **Organize findings** by:
   - Evidence of growth decay (Chart A + statistics)
   - Evidence of retention differences (Chart B + statistics)
   - Evidence of volatility/sustainability (Chart C + statistics)

4. **For your thesis, emphasize:**
   - The yellow gap in growth decay charts (overestimation %)
   - The diverging retention trends (views-per-video slopes)
   - The decay slope comparison (negative trend steepness)

---

## File Organization After Completion

```
Your Project Folder/
├── data/
│   ├── jomboy_videos_20260127_134357.csv
│   └── bussinwiththeboys_videos_20260127_XXXXXX.csv
├── visualizations/
│   ├── views_over_time.png
│   ├── growth_decay_analysis.png
│   └── ... (7 total charts for whichever channel you last analyzed)
├── comparisons/
│   ├── comparison_growth_decay.png
│   ├── comparison_retention.png
│   └── comparison_growth_rates.png
└── python scripts...
```

**Pro tip:** Rename the visualizations folder after each channel analysis:
```bash
mv visualizations visualizations_jomboy
python visualize.py bussin_data.csv
mv visualizations visualizations_bussin
```

This way you keep both sets of individual charts!

---

## Summary Commands (Quick Reference)

```bash
# Setup
cd "/path/to/project"
source venv/bin/activate

# Collect Bussin' data
python youtube_analytics.py --channel "@BussinWithTheBoys"

# Generate Bussin' visualizations
python visualize.py bussinwiththeboys_videos_TIMESTAMP.csv

# Compare both channels
python compare_channels.py \
    data/jomboy_videos_TIMESTAMP.csv \
    bussinwiththeboys_videos_TIMESTAMP.csv \
    --name1 "Jomboy Media" \
    --name2 "Bussin' With The Boys"

# View results
open comparisons/
```

---

Good luck with your analysis! This comparison will provide strong evidence for your thesis about growth decay and content-type-specific retention patterns.

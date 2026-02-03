#!/usr/bin/env python3
"""
YouTube Analytics Runner
Fetch data and generate visualizations in one command
"""

import sys
from pathlib import Path
from youtube_analytics import YouTubeAnalytics
from visualize_old import YouTubeVisualizer
from datetime import datetime


def main():
    """Run complete analysis pipeline"""
    
    print("=" * 70)
    print("YouTube Channel Analytics - Complete Pipeline")
    print("=" * 70)
    
    # Configuration
    API_KEY = "YOUR_API_KEY"
    CHANNEL_HANDLE = "CHANNEL HANDLE"
    
    # Create output directories
    data_dir = Path("data")
    viz_dir = Path("visualizations")
    data_dir.mkdir(exist_ok=True)
    viz_dir.mkdir(exist_ok=True)
    
    # Step 1: Fetch data
    print("\n" + "=" * 70)
    print("STEP 1: Fetching Channel Data")
    print("=" * 70)
    
    analyzer = YouTubeAnalytics(API_KEY)
    
    channel_id = analyzer.get_channel_id(CHANNEL_HANDLE)
    if not channel_id:
        print("❌ Could not find channel!")
        return 1
    
    videos = analyzer.get_all_videos(channel_id)
    if not videos:
        print("❌ No videos found!")
        return 1
    
    # Save data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = data_dir / f"jomboy_videos_{timestamp}.csv"
    json_file = data_dir / f"jomboy_videos_{timestamp}.json"
    
    analyzer.save_to_csv(videos, str(csv_file))
    analyzer.save_to_json(videos, str(json_file))
    
    # Step 2: Generate visualizations
    print("\n" + "=" * 70)
    print("STEP 2: Generating Visualizations")
    print("=" * 70)
    
    visualizer = YouTubeVisualizer(str(csv_file))
    visualizer.create_all_visualizations(output_dir=str(viz_dir))
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Data saved to: {data_dir}/")
    print(f"   - {csv_file.name}")
    print(f"   - {json_file.name}")
    print(f"\n📊 Visualizations saved to: {viz_dir}/")
    print(f"   - views_over_time.png")
    print(f"   - upload_frequency.png")
    print(f"   - growth_rate.png")
    print(f"   - engagement_analysis.png")
    print(f"   - top_videos.png")
    print("\n" + "=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

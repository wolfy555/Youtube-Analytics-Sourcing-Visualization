"""
YouTube Channel Analytics Tool
Tracks video views, engagement, and growth metrics for a YouTube channel
"""

import requests
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
import time


class YouTubeAnalytics:
    """Fetch and analyze YouTube channel data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def get_channel_id(self, channel_handle: str) -> Optional[str]:
        """
        Get channel ID from channel handle (e.g., @JomboyMedia)
        
        Args:
            channel_handle: Channel handle like '@JomboyMedia'
            
        Returns:
            Channel ID string or None if not found
        """
        # Remove @ if present
        handle = channel_handle.lstrip('@')
        
        url = f"{self.base_url}/channels"
        params = {
            'part': 'id,snippet,statistics',
            'forHandle': handle,
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            channel_info = data['items'][0]
            print(f"\n📺 Channel Found: {channel_info['snippet']['title']}")
            print(f"   Subscribers: {channel_info['statistics']['subscriberCount']}")
            print(f"   Total Videos: {channel_info['statistics']['videoCount']}")
            print(f"   Total Views: {channel_info['statistics']['viewCount']}")
            return channel_info['id']
        else:
            print(f"Error: {data}")
            return None
    
    def get_all_videos(self, channel_id: str) -> List[Dict]:
        """
        Fetch all videos from a channel
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            List of video dictionaries with metadata
        """
        videos = []
        next_page_token = None
        
        print(f"\n🔍 Fetching videos...")
        
        while True:
            # Get uploads playlist ID
            url = f"{self.base_url}/channels"
            params = {
                'part': 'contentDetails',
                'id': channel_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' not in data or len(data['items']) == 0:
                break
                
            uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            url = f"{self.base_url}/playlistItems"
            params = {
                'part': 'contentDetails',
                'playlistId': uploads_playlist_id,
                'maxResults': 50,
                'key': self.api_key
            }
            
            if next_page_token:
                params['pageToken'] = next_page_token
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' not in data:
                break
            
            # Extract video IDs
            video_ids = [item['contentDetails']['videoId'] for item in data['items']]
            
            # Get detailed stats for these videos
            video_details = self.get_video_details(video_ids)
            videos.extend(video_details)
            
            print(f"   Fetched {len(videos)} videos so far...")
            
            # Check for next page
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break
            
            time.sleep(0.5)  # Rate limiting
        
        print(f"✅ Total videos fetched: {len(videos)}")
        return videos
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """
        Get detailed statistics for a list of video IDs
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            List of video detail dictionaries
        """
        url = f"{self.base_url}/videos"
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': ','.join(video_ids),
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'description': item['snippet'].get('description', ''),
                'duration': item['contentDetails']['duration'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'fetched_at': datetime.now().isoformat()
            }
            videos.append(video)
        
        return videos
    
    def save_to_csv(self, videos: List[Dict], filename: str):
        """
        Save video data to CSV file
        
        Args:
            videos: List of video dictionaries
            filename: Output CSV filename
        """
        if not videos:
            print("No videos to save!")
            return
        
        fieldnames = ['video_id', 'title', 'published_at', 'duration', 
                     'view_count', 'like_count', 'comment_count', 'fetched_at']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for video in videos:
                row = {k: video[k] for k in fieldnames}
                writer.writerow(row)
        
        print(f"💾 Data saved to {filename}")
    
    def save_to_json(self, videos: List[Dict], filename: str):
        """
        Save video data to JSON file
        
        Args:
            videos: List of video dictionaries
            filename: Output JSON filename
        """
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(videos, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to {filename}")


def main():
    """Main execution function"""
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='YouTube Channel Analytics Data Collection')
    parser.add_argument('--channel', type=str, help='Channel handle (e.g., @JomboyMedia)')
    parser.add_argument('--api-key', type=str, help='YouTube API key (optional if using config)')
    
    args = parser.parse_args()
    
    # Determine which channel to analyze
    if args.channel:
        CHANNEL_HANDLE = args.channel
    else:
        # Try to import from config, otherwise use default
        try:
            from config import API_KEY, CHANNEL_HANDLE
        except ImportError:
            print("❌ No channel specified and no config.py found!")
            print("Usage: python youtube_analytics.py --channel @ChannelHandle")
            return
    
    # Get API key
    if args.api_key:
        API_KEY = args.api_key
    else:
        try:
            from config import API_KEY
        except ImportError:
            print("❌ No API key found!")
            print("Either add API_KEY to config.py or use --api-key argument")
            return
    
    print("=" * 60)
    print("YouTube Channel Analytics Tool")
    print("=" * 60)
    print(f"Analyzing: {CHANNEL_HANDLE}")
    
    # Initialize analyzer
    analyzer = YouTubeAnalytics(API_KEY)
    
    # Get channel ID
    channel_id = analyzer.get_channel_id(CHANNEL_HANDLE)
    
    if not channel_id:
        print("❌ Could not find channel!")
        return
    
    # Fetch all videos
    videos = analyzer.get_all_videos(channel_id)
    
    if not videos:
        print("❌ No videos found!")
        return
    
    # Create clean channel name for filenames
    clean_channel_name = CHANNEL_HANDLE.replace('@', '').replace(' ', '_').lower()
    
    # Save data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{clean_channel_name}_videos_{timestamp}.csv"
    json_filename = f"{clean_channel_name}_videos_{timestamp}.json"
    
    analyzer.save_to_csv(videos, csv_filename)
    analyzer.save_to_json(videos, json_filename)
    
    print("\n" + "=" * 60)
    print("✅ Data collection complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

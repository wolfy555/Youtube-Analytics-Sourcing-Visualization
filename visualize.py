"""
YouTube Channel Growth Visualization
Analyzes and visualizes video performance and channel growth trends
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path


class YouTubeVisualizer:
    """Create visualizations for YouTube channel analytics"""
    
    def __init__(self, csv_file: str):
        """
        Initialize visualizer with data file
        
        Args:
            csv_file: Path to CSV file with video data
        """
        self.df = pd.read_csv(csv_file)
        self.df['published_at'] = pd.to_datetime(self.df['published_at'])
        self.df = self.df.sort_values('published_at')
        
        print(f"📊 Loaded {len(self.df)} videos")
        print(f"   Date range: {self.df['published_at'].min().date()} to {self.df['published_at'].max().date()}")
    
    def plot_views_over_time(self, save_path: str = "views_over_time.png"):
        """
        Plot cumulative views over time
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Cumulative views
        self.df['cumulative_views'] = self.df['view_count'].cumsum()
        
        ax1.plot(self.df['published_at'], self.df['cumulative_views'], 
                linewidth=2, color='#FF0000', marker='o', markersize=3, alpha=0.7)
        ax1.set_title('Cumulative Views Over Time', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Total Views', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Format y-axis with commas
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        # Views per video
        ax2.scatter(self.df['published_at'], self.df['view_count'], 
                   alpha=0.6, s=50, color='#FF0000')
        ax2.set_title('Views Per Video', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Publication Date', fontsize=12)
        ax2.set_ylabel('Views', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_upload_frequency(self, save_path: str = "upload_frequency.png"):
        """
        Analyze and plot upload frequency over time
        """
        # Group by month
        self.df['year_month'] = self.df['published_at'].dt.to_period('M')
        monthly_uploads = self.df.groupby('year_month').size()
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = range(len(monthly_uploads))
        ax.bar(x, monthly_uploads.values, color='#FF0000', alpha=0.7, edgecolor='black')
        
        ax.set_title('Upload Frequency by Month', fontsize=16, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Number of Videos', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Set x-axis labels
        ax.set_xticks(x[::3])  # Show every 3rd month
        ax.set_xticklabels([str(m) for m in monthly_uploads.index[::3]], rotation=45, ha='right')
        
        # Add average line
        avg_uploads = monthly_uploads.mean()
        ax.axhline(y=avg_uploads, color='blue', linestyle='--', linewidth=2, 
                  label=f'Average: {avg_uploads:.1f} videos/month')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_growth_rate(self, save_path: str = "growth_rate.png"):
        """
        Calculate and plot view growth rate
        """
        # Calculate views per month
        monthly_views = self.df.groupby('year_month')['view_count'].sum()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Monthly views
        x = range(len(monthly_views))
        ax1.plot(x, monthly_views.values, marker='o', linewidth=2, 
                color='#FF0000', markersize=6)
        ax1.set_title('Monthly Total Views (All Videos Published That Month)', 
                     fontsize=16, fontweight='bold')
        ax1.set_ylabel('Views', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        ax1.set_xticks([])
        
        # Growth rate (month-over-month percentage change)
        growth_rate = monthly_views.pct_change() * 100
        
        # Cap extreme outliers at 95th percentile for better visualization
        # But still show them - just capped visually
        cap_value = growth_rate.quantile(0.95)
        growth_rate_capped = growth_rate.copy()
        
        # Track which values were capped for annotation
        capped_indices = []
        for i, val in enumerate(growth_rate.values):
            if pd.notna(val) and abs(val) > cap_value:
                capped_indices.append(i)
                # Cap at 95th percentile but keep the sign
                growth_rate_capped.iloc[i] = cap_value if val > 0 else -cap_value
        
        colors = ['green' if x >= 0 else 'red' for x in growth_rate_capped.values]
        bars = ax2.bar(x[1:], growth_rate_capped.values[1:], color=colors[1:], alpha=0.7, edgecolor='black')
        
        # Add markers for capped values
        for idx in capped_indices:
            if idx > 0:  # Skip first month (no growth rate)
                ax2.text(idx, growth_rate_capped.iloc[idx], '↑' if growth_rate.iloc[idx] > 0 else '↓', 
                        ha='center', va='bottom' if growth_rate.iloc[idx] > 0 else 'top', 
                        fontsize=12, fontweight='bold')
        
        ax2.set_title('Month-over-Month Growth Rate (Extreme outliers capped for visibility)', 
                     fontsize=16, fontweight='bold')
        ax2.set_xlabel('Month', fontsize=12)
        ax2.set_ylabel('Growth Rate (%)', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        # Set x-axis labels
        ax2.set_xticks(x[::3])
        ax2.set_xticklabels([str(m) for m in monthly_views.index[::3]], rotation=45, ha='right')
        
        # Add note about capped values
        if capped_indices:
            note_text = f"Note: ↑/↓ indicates capped outliers (actual values exceed {cap_value:.0f}%)"
            ax2.text(0.02, 0.98, note_text, transform=ax2.transAxes, 
                    fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round', 
                    facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_growth_decay_analysis(self, save_path: str = "growth_decay_analysis.png"):
        """
        Analyze growth rate decay over time - proving early explosive growth doesn't persist
        This chart shows the danger of extrapolating early growth rates
        """
        # Calculate cumulative views over time
        self.df_sorted = self.df.sort_values('published_at')
        self.df_sorted['cumulative_views'] = self.df_sorted['view_count'].cumsum()
        self.df_sorted['days_since_start'] = (self.df_sorted['published_at'] - self.df_sorted['published_at'].min()).dt.days
        
        # Calculate rolling growth rates (90-day windows)
        monthly_views = self.df.groupby('year_month')['view_count'].sum()
        growth_rate = monthly_views.pct_change() * 100
        
        # Calculate rolling average growth rate (6-month window)
        rolling_growth = growth_rate.rolling(window=6, min_periods=1).mean()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # Top chart: Cumulative views with extrapolation from 2019 peak
        # Find 2019 data (the "takeoff" year)
        year_2019_mask = self.df_sorted['published_at'].dt.year == 2019
        if year_2019_mask.any():
            # Get cumulative views at end of 2019
            end_2019 = self.df_sorted[self.df_sorted['published_at'].dt.year <= 2019]['cumulative_views'].max()
            end_2019_days = self.df_sorted[self.df_sorted['published_at'].dt.year <= 2019]['days_since_start'].max()
            
            # Calculate 2019 growth rate
            start_2019 = self.df_sorted[self.df_sorted['published_at'].dt.year < 2019]['cumulative_views'].max() if len(self.df_sorted[self.df_sorted['published_at'].dt.year < 2019]) > 0 else 0
            growth_2019 = (end_2019 - start_2019) / start_2019 if start_2019 > 0 else 0
            
            # Extrapolate 2019 growth rate forward
            max_days = self.df_sorted['days_since_start'].max()
            extrapolation_days = np.linspace(end_2019_days, max_days, 100)
            years_forward = (extrapolation_days - end_2019_days) / 365.25
            extrapolated_views = end_2019 * (1 + growth_2019) ** years_forward
            
            # Plot actual cumulative views
            ax1.plot(self.df_sorted['days_since_start'], self.df_sorted['cumulative_views'], 
                    linewidth=3, color='#FF0000', label='Actual Growth', alpha=0.8)
            
            # Plot extrapolation
            ax1.plot(extrapolation_days, extrapolated_views, 
                    linewidth=3, color='#00FF00', linestyle='--', label='2019 Growth Rate Extrapolated', alpha=0.8)
            
            # Shade the gap
            actual_final = self.df_sorted['cumulative_views'].iloc[-1]
            extrapolated_final = extrapolated_views[-1]
            gap_pct = ((extrapolated_final - actual_final) / actual_final) * 100
            
            ax1.fill_between(extrapolation_days, 
                           np.interp(extrapolation_days, self.df_sorted['days_since_start'], self.df_sorted['cumulative_views']),
                           extrapolated_views, alpha=0.3, color='yellow', 
                           label=f'Overestimation Gap: {gap_pct:.0f}%')
            
            # Add annotation for 2019 takeoff
            ax1.axvline(x=end_2019_days, color='blue', linestyle=':', linewidth=2, alpha=0.6)
            ax1.text(end_2019_days, ax1.get_ylim()[1] * 0.5, '2019 "Takeoff"\nYear End', 
                    rotation=90, verticalalignment='center', fontsize=10, color='blue')
        else:
            # If no 2019 data, just plot actual
            ax1.plot(self.df_sorted['days_since_start'], self.df_sorted['cumulative_views'], 
                    linewidth=3, color='#FF0000', label='Actual Growth')
        
        ax1.set_title('Cumulative Views: Extrapolated 2019 Growth vs. Reality\n(The Danger of Linear Extrapolation)', 
                     fontsize=16, fontweight='bold')
        ax1.set_xlabel('Days Since Channel Start', fontsize=12)
        ax1.set_ylabel('Cumulative Views', fontsize=12)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1e6):.0f}M' if x >= 1e6 else f'{int(x/1e3):.0f}K'))
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left', fontsize=10)
        
        # Bottom chart: Rolling average growth rate showing decay
        x_months = range(len(rolling_growth))
        ax2.plot(x_months, rolling_growth.values, linewidth=3, color='#FF0000', marker='o', markersize=4, alpha=0.8)
        ax2.fill_between(x_months, rolling_growth.values, alpha=0.3, color='#FF0000')
        
        # Add trend line to show decay
        valid_mask = ~np.isnan(rolling_growth.values)
        if valid_mask.sum() > 1:
            z = np.polyfit(np.array(x_months)[valid_mask], rolling_growth.values[valid_mask], 1)
            p = np.poly1d(z)
            ax2.plot(x_months, p(x_months), "b--", linewidth=2, label=f'Decay Trend (slope: {z[0]:.2f}%/month)', alpha=0.8)
        
        # Highlight 2019 period
        try:
            months_2019 = [i for i, month in enumerate(rolling_growth.index) if month.year == 2019]
            if months_2019:
                ax2.axvspan(min(months_2019), max(months_2019), alpha=0.2, color='green', label='2019 "Takeoff" Period')
        except:
            pass
        
        ax2.set_title('6-Month Rolling Average Growth Rate\n(Showing Systematic Decay Post-Takeoff)', 
                     fontsize=16, fontweight='bold')
        ax2.set_xlabel('Month', fontsize=12)
        ax2.set_ylabel('Average Growth Rate (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax2.legend(loc='upper right', fontsize=10)
        
        # Set x-axis labels
        ax2.set_xticks(x_months[::6])
        ax2.set_xticklabels([str(m) for m in rolling_growth.index[::6]], rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_mean_reversion_analysis(self, save_path: str = "mean_reversion_analysis.png"):
        """
        Show mean reversion in growth rates - proving post-takeoff normalization
        """
        # Calculate monthly metrics
        monthly_views = self.df.groupby('year_month')['view_count'].sum()
        monthly_videos = self.df.groupby('year_month').size()
        views_per_video = monthly_views / monthly_videos
        
        # Calculate growth rates
        growth_rate = monthly_views.pct_change() * 100
        
        # Separate into early period (2019-2020) and later period
        early_mask = monthly_views.index.year <= 2020
        later_mask = monthly_views.index.year > 2020
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Growth Rate Distribution: Early vs Later
        early_growth = growth_rate[early_mask].dropna()
        later_growth = growth_rate[later_mask].dropna()
        
        # Filter extreme outliers for better visualization (keep within 3 std devs)
        early_clean = early_growth[np.abs(early_growth - early_growth.mean()) < 3 * early_growth.std()]
        later_clean = later_growth[np.abs(later_growth - later_growth.mean()) < 3 * later_growth.std()]
        
        if len(early_clean) > 0:
            ax1.hist(early_clean, bins=20, alpha=0.7, color='green', 
                    label=f'2019-2020 (Takeoff)\nMean: {early_growth.mean():.1f}%', edgecolor='black')
            ax1.axvline(early_growth.mean(), color='green', linestyle='--', linewidth=2)
        
        if len(later_clean) > 0:
            ax1.hist(later_clean, bins=20, alpha=0.7, color='red', 
                    label=f'Post-2020\nMean: {later_growth.mean():.1f}%', edgecolor='black')
            ax1.axvline(later_growth.mean(), color='red', linestyle='--', linewidth=2)
        
        ax1.set_title('Growth Rate Distribution: Early Explosive vs. Normalized', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Monthly Growth Rate (%)', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # 2. Views per Video Over Time (quality/consistency metric)
        x = range(len(views_per_video))
        ax2.plot(x, views_per_video.values, linewidth=2, color='#FF0000', marker='o', markersize=4, alpha=0.8)
        
        # Add trend line
        if len(views_per_video) > 1:
            z = np.polyfit(x, views_per_video.values, 1)
            p = np.poly1d(z)
            trend_direction = "Declining" if z[0] < 0 else "Growing"
            ax2.plot(x, p(x), "b--", linewidth=2, label=f'Trend: {trend_direction}', alpha=0.8)
        
        ax2.set_title('Average Views per Video Over Time\n(Content Quality/Novelty Decay Indicator)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Views per Video', fontsize=11)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1e3):.0f}K'))
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        ax2.set_xticks(x[::6])
        ax2.set_xticklabels([str(m) for m in views_per_video.index[::6]], rotation=45, ha='right')
        
        # 3. Volatility Over Time (standard deviation of growth rates in rolling windows)
        rolling_std = growth_rate.rolling(window=6, min_periods=1).std()
        
        # Filter extreme outliers for better visualization
        rolling_std_clean = rolling_std.copy()
        outlier_threshold = rolling_std.quantile(0.95)
        rolling_std_clean[rolling_std_clean > outlier_threshold] = outlier_threshold
        
        x = range(len(rolling_std_clean))
        ax3.plot(x, rolling_std_clean.values, linewidth=2, color='purple', marker='o', markersize=4, alpha=0.8)
        ax3.fill_between(x, rolling_std_clean.values, alpha=0.3, color='purple')
        
        # Add trend
        valid_mask = ~np.isnan(rolling_std_clean.values)
        if valid_mask.sum() > 1:
            z = np.polyfit(np.array(x)[valid_mask], rolling_std_clean.values[valid_mask], 1)
            p = np.poly1d(z)
            ax3.plot(x, p(x), "b--", linewidth=2, label='Volatility Trend', alpha=0.8)
        
        ax3.set_title('Growth Rate Volatility Over Time\n(High Volatility = Unsustainable Growth)', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Growth Rate Std Dev (%) [Capped at 95th percentile]', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=10)
        
        # Better x-axis handling to avoid text overlap
        num_labels = min(10, len(rolling_std_clean))
        step = max(1, len(rolling_std_clean) // num_labels)
        ax3.set_xticks(x[::step])
        ax3.set_xticklabels([str(m) for m in rolling_std.index[::step]], rotation=45, ha='right', fontsize=9)
        
        # 4. Cumulative Views: Actual vs. Mean Growth Assumption
        cumulative_views = monthly_views.cumsum()
        
        # Use median growth rate instead of mean to avoid outlier skew
        median_growth_rate = growth_rate.median() / 100 if not growth_rate.isna().all() else 0
        
        # Project using median growth rate from start
        mean_projection = [monthly_views.iloc[0]]
        for i in range(1, len(monthly_views)):
            mean_projection.append(mean_projection[-1] * (1 + median_growth_rate))
        mean_projection_cumsum = np.cumsum(mean_projection)
        
        x = range(len(cumulative_views))
        ax4.plot(x, cumulative_views.values, linewidth=3, color='#FF0000', label='Actual', alpha=0.8)
        ax4.plot(x, mean_projection_cumsum, linewidth=3, color='blue', linestyle='--', 
                label=f'Median Growth Projection ({median_growth_rate*100:.1f}%/mo)', alpha=0.8)
        
        ax4.set_title('Cumulative Views: Actual vs. Median Growth Rate Assumption', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Cumulative Views', fontsize=11)
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1e6):.0f}M' if x >= 1e6 else f'{int(x/1e3):.0f}K'))
        ax4.grid(True, alpha=0.3)
        ax4.legend(fontsize=10)
        
        # Better x-axis handling
        ax4.set_xticks(x[::step])
        ax4.set_xticklabels([str(m) for m in cumulative_views.index[::step]], rotation=45, ha='right', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_engagement_analysis(self, save_path: str = "engagement_analysis.png"):
        """
        Analyze engagement metrics over time
        """
        # Calculate engagement rates
        self.df['engagement_rate'] = ((self.df['like_count'] + self.df['comment_count']) / 
                                     self.df['view_count'] * 100)
        
        # Calculate monthly average engagement rate
        monthly_engagement = self.df.groupby('year_month')['engagement_rate'].mean()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Monthly average engagement rate
        x = range(len(monthly_engagement))
        ax1.plot(x, monthly_engagement.values, marker='o', linewidth=2, 
                color='#FF0000', markersize=6)
        ax1.set_title('Average Engagement Rate by Month', 
                     fontsize=16, fontweight='bold')
        ax1.set_ylabel('Engagement Rate (%)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks([])
        
        # Add average line
        avg_engagement = monthly_engagement.mean()
        ax1.axhline(y=avg_engagement, color='blue', linestyle='--', linewidth=2,
                   label=f'Overall Avg: {avg_engagement:.2f}%')
        ax1.legend()
        
        # Engagement growth rate (month-over-month percentage change)
        engagement_growth = monthly_engagement.pct_change() * 100
        
        # Cap extreme outliers for better visualization
        cap_value = engagement_growth.quantile(0.95)
        engagement_growth_capped = engagement_growth.copy()
        
        # Track which values were capped
        capped_indices = []
        for i, val in enumerate(engagement_growth.values):
            if pd.notna(val) and abs(val) > cap_value:
                capped_indices.append(i)
                engagement_growth_capped.iloc[i] = cap_value if val > 0 else -cap_value
        
        colors = ['green' if x >= 0 else 'red' for x in engagement_growth_capped.values]
        ax2.bar(x[1:], engagement_growth_capped.values[1:], color=colors[1:], alpha=0.7, edgecolor='black')
        
        # Add markers for capped values
        for idx in capped_indices:
            if idx > 0:
                ax2.text(idx, engagement_growth_capped.iloc[idx], 
                        '↑' if engagement_growth.iloc[idx] > 0 else '↓', 
                        ha='center', va='bottom' if engagement_growth.iloc[idx] > 0 else 'top', 
                        fontsize=12, fontweight='bold')
        
        ax2.set_title('Month-over-Month Engagement Growth Rate', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Month', fontsize=12)
        ax2.set_ylabel('Engagement Growth Rate (%)', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        # Set x-axis labels
        ax2.set_xticks(x[::3])
        ax2.set_xticklabels([str(m) for m in monthly_engagement.index[::3]], rotation=45, ha='right')
        
        # Add note about capped values if any
        if capped_indices:
            note_text = f"Note: ↑/↓ indicates capped outliers (actual values exceed {cap_value:.0f}%)"
            ax2.text(0.02, 0.98, note_text, transform=ax2.transAxes, 
                    fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round', 
                    facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_top_performers(self, n=10, save_path: str = "top_videos.png"):
        """
        Show top performing videos
        """
        top_videos = self.df.nlargest(n, 'view_count')
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Truncate long titles and escape special characters for matplotlib
        titles = []
        for title in top_videos['title']:
            # Escape dollar signs and other special characters
            title = str(title).replace('$', r'\$').replace('_', r'\_')
            # Truncate if too long
            if len(title) > 50:
                title = title[:50] + '...'
            titles.append(title)
        
        y_pos = range(len(titles))
        ax.barh(y_pos, top_videos['view_count'].values, color='#FF0000', alpha=0.7)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(titles, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel('Views', fontsize=12)
        ax.set_title(f'Top {n} Most Viewed Videos', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Format x-axis with commas
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def generate_summary_report(self):
        """
        Print summary statistics
        """
        print("\n" + "=" * 60)
        print("📊 CHANNEL ANALYTICS SUMMARY")
        print("=" * 60)
        
        total_views = self.df['view_count'].sum()
        total_likes = self.df['like_count'].sum()
        total_comments = self.df['comment_count'].sum()
        avg_views = self.df['view_count'].mean()
        median_views = self.df['view_count'].median()
        
        print(f"\n📹 Total Videos: {len(self.df):,}")
        print(f"👀 Total Views: {total_views:,}")
        print(f"👍 Total Likes: {total_likes:,}")
        print(f"💬 Total Comments: {total_comments:,}")
        print(f"\n📊 Average Views per Video: {avg_views:,.0f}")
        print(f"📊 Median Views per Video: {median_views:,.0f}")
        
        # Calculate average monthly uploads
        months_active = (self.df['published_at'].max() - self.df['published_at'].min()).days / 30.44
        avg_monthly_uploads = len(self.df) / months_active if months_active > 0 else 0
        print(f"\n📅 Average Uploads per Month: {avg_monthly_uploads:.1f}")
        
        # Recent performance (last 30 days)
        thirty_days_ago = pd.Timestamp.now(tz='UTC') - timedelta(days=30)
        recent_videos = self.df[self.df['published_at'] >= thirty_days_ago]
        if len(recent_videos) > 0:
            print(f"\n📅 Last 30 Days:")
            print(f"   Videos uploaded: {len(recent_videos)}")
            print(f"   Total views on new videos: {recent_videos['view_count'].sum():,}")
        
        print("\n" + "=" * 60)
    
    def create_all_visualizations(self, output_dir: str = "."):
        """
        Generate all visualization plots
        
        Args:
            output_dir: Directory to save plots
        """
        print("\n🎨 Generating visualizations...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        self.plot_views_over_time(str(output_path / "views_over_time.png"))
        self.plot_upload_frequency(str(output_path / "upload_frequency.png"))
        self.plot_growth_rate(str(output_path / "growth_rate.png"))
        self.plot_engagement_analysis(str(output_path / "engagement_analysis.png"))
        self.plot_top_performers(n=15, save_path=str(output_path / "top_videos.png"))
        
        # NEW: Advanced growth analysis charts
        print("\n📉 Generating advanced growth decay analysis...")
        self.plot_growth_decay_analysis(str(output_path / "growth_decay_analysis.png"))
        self.plot_mean_reversion_analysis(str(output_path / "mean_reversion_analysis.png"))
        
        self.generate_summary_report()
        
        print("\n✅ All visualizations complete!")
        print("\n💡 For your investment thesis, focus on:")
        print("   - growth_decay_analysis.png (shows 2019 extrapolation vs reality)")
        print("   - mean_reversion_analysis.png (shows systematic decay patterns)")
        print("   - engagement_analysis.png (shows audience engagement trends)")



def main():
    """Main execution"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <csv_file>")
        print("\nLooking for most recent CSV file...")
        
        # Find most recent CSV file
        csv_files = sorted(Path('.').glob('jomboy_videos_*.csv'), reverse=True)
        if not csv_files:
            print("❌ No CSV files found! Run youtube_analytics.py first.")
            return
        
        csv_file = str(csv_files[0])
        print(f"Found: {csv_file}\n")
    else:
        csv_file = sys.argv[1]
    
    visualizer = YouTubeVisualizer(csv_file)
    visualizer.create_all_visualizations()


if __name__ == "__main__":
    main()

"""
YouTube Channel Comparison Tool
Compares growth patterns, retention rates, and decay metrics between two channels
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import argparse


class ChannelComparator:
    """Compare two YouTube channels for growth and retention analysis"""
    
    def __init__(self, channel1_csv: str, channel2_csv: str, 
                 channel1_name: str = "Channel 1", channel2_name: str = "Channel 2"):
        """
        Initialize with two channel data files
        
        Args:
            channel1_csv: Path to first channel's CSV data
            channel2_csv: Path to second channel's CSV data
            channel1_name: Display name for first channel
            channel2_name: Display name for second channel
        """
        self.ch1_name = channel1_name
        self.ch2_name = channel2_name
        
        # Load data
        print(f"📊 Loading {channel1_name} data...")
        self.df1 = pd.read_csv(channel1_csv)
        self.df1['published_at'] = pd.to_datetime(self.df1['published_at'])
        self.df1 = self.df1.sort_values('published_at')
        
        print(f"📊 Loading {channel2_name} data...")
        self.df2 = pd.read_csv(channel2_csv)
        self.df2['published_at'] = pd.to_datetime(self.df2['published_at'])
        self.df2 = self.df2.sort_values('published_at')
        
        print(f"\n✅ Loaded {len(self.df1)} videos from {channel1_name}")
        print(f"✅ Loaded {len(self.df2)} videos from {channel2_name}")
        
        # Calculate months since channel start for alignment
        self.df1['months_since_start'] = ((self.df1['published_at'] - self.df1['published_at'].min()).dt.days / 30.44).astype(int)
        self.df2['months_since_start'] = ((self.df2['published_at'] - self.df2['published_at'].min()).dt.days / 30.44).astype(int)
        
        # Identify takeoff periods
        self.ch1_takeoff_year = self._identify_takeoff(self.df1)
        self.ch2_takeoff_year = self._identify_takeoff(self.df2)
        
        print(f"\n🚀 {channel1_name} takeoff year: {self.ch1_takeoff_year}")
        print(f"🚀 {channel2_name} takeoff year: {self.ch2_takeoff_year}")
    
    def _identify_takeoff(self, df):
        """Identify the year with highest growth rate"""
        df['year'] = df['published_at'].dt.year
        yearly_views = df.groupby('year')['view_count'].sum()
        yearly_growth = yearly_views.pct_change()
        
        if len(yearly_growth) > 0:
            takeoff_year = yearly_growth.idxmax()
            return takeoff_year if pd.notna(takeoff_year) else df['year'].min()
        return df['year'].min()
    
    def _align_by_takeoff(self, df, takeoff_year):
        """Create 'months_since_takeoff' column"""
        # Make timezone-aware to match the dataframe dates
        takeoff_start = pd.Timestamp(f"{takeoff_year}-01-01", tz='UTC')
        df['months_since_takeoff'] = ((df['published_at'] - takeoff_start).dt.days / 30.44).astype(int)
        return df
    
    def plot_dual_growth_decay(self, save_path: str = "comparison_growth_decay.png"):
        """
        Side-by-side growth decay analysis showing extrapolation vs reality
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Channel 1
        self._plot_single_decay(self.df1, self.ch1_name, self.ch1_takeoff_year, ax1, '#FF0000')
        
        # Channel 2
        self._plot_single_decay(self.df2, self.ch2_name, self.ch2_takeoff_year, ax2, '#0000FF')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def _plot_single_decay(self, df, name, takeoff_year, ax, color):
        """Helper to plot single channel decay analysis"""
        df_sorted = df.sort_values('published_at')
        df_sorted['cumulative_views'] = df_sorted['view_count'].cumsum()
        df_sorted['days_since_start'] = (df_sorted['published_at'] - df_sorted['published_at'].min()).dt.days
        
        # Get takeoff year data
        year_mask = df_sorted['published_at'].dt.year == takeoff_year
        if year_mask.any():
            end_year = df_sorted[df_sorted['published_at'].dt.year <= takeoff_year]['cumulative_views'].max()
            end_year_days = df_sorted[df_sorted['published_at'].dt.year <= takeoff_year]['days_since_start'].max()
            
            start_year = df_sorted[df_sorted['published_at'].dt.year < takeoff_year]['cumulative_views'].max() if len(df_sorted[df_sorted['published_at'].dt.year < takeoff_year]) > 0 else 0
            growth_rate = (end_year - start_year) / start_year if start_year > 0 else 0
            
            # Extrapolate
            max_days = df_sorted['days_since_start'].max()
            extrapolation_days = np.linspace(end_year_days, max_days, 100)
            years_forward = (extrapolation_days - end_year_days) / 365.25
            extrapolated = end_year * (1 + growth_rate) ** years_forward
            
            # Plot
            ax.plot(df_sorted['days_since_start'], df_sorted['cumulative_views'], 
                   linewidth=3, color=color, label='Actual', alpha=0.8)
            ax.plot(extrapolation_days, extrapolated, 
                   linewidth=3, color='green', linestyle='--', label=f'{takeoff_year} Extrapolation', alpha=0.8)
            
            # Calculate gap
            actual_final = df_sorted['cumulative_views'].iloc[-1]
            extrapolated_final = extrapolated[-1]
            gap_pct = ((extrapolated_final - actual_final) / actual_final) * 100
            
            ax.fill_between(extrapolation_days,
                          np.interp(extrapolation_days, df_sorted['days_since_start'], df_sorted['cumulative_views']),
                          extrapolated, alpha=0.3, color='yellow',
                          label=f'Gap: {gap_pct:.0f}%')
            
            ax.axvline(x=end_year_days, color='blue', linestyle=':', linewidth=2, alpha=0.6)
        else:
            ax.plot(df_sorted['days_since_start'], df_sorted['cumulative_views'], 
                   linewidth=3, color=color, label='Actual')
        
        ax.set_title(f'{name}\nExtrapolation vs Reality', fontsize=14, fontweight='bold')
        ax.set_xlabel('Days Since Channel Start', fontsize=11)
        ax.set_ylabel('Cumulative Views', fontsize=11)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1e6):.0f}M' if x >= 1e6 else f'{int(x/1e3):.0f}K'))
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=9)
    
    def plot_retention_comparison(self, save_path: str = "comparison_retention.png"):
        """
        Compare views-per-video trends (retention proxy)
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 14))
        
        # Align both by months since takeoff
        df1_aligned = self._align_by_takeoff(self.df1.copy(), self.ch1_takeoff_year)
        df2_aligned = self._align_by_takeoff(self.df2.copy(), self.ch2_takeoff_year)
        
        # Calculate views per video by month since takeoff
        ch1_monthly = df1_aligned.groupby('months_since_takeoff').agg({
            'view_count': ['sum', 'count', 'mean']
        }).reset_index()
        ch1_monthly.columns = ['months_since_takeoff', 'total_views', 'video_count', 'avg_views_per_video']
        
        ch2_monthly = df2_aligned.groupby('months_since_takeoff').agg({
            'view_count': ['sum', 'count', 'mean']
        }).reset_index()
        ch2_monthly.columns = ['months_since_takeoff', 'total_views', 'video_count', 'avg_views_per_video']
        
        # Chart 1: Views per video overlay
        ax1.plot(ch1_monthly['months_since_takeoff'], ch1_monthly['avg_views_per_video'],
                linewidth=3, color='#FF0000', marker='o', markersize=4, alpha=0.8, label=self.ch1_name)
        ax1.plot(ch2_monthly['months_since_takeoff'], ch2_monthly['avg_views_per_video'],
                linewidth=3, color='#0000FF', marker='s', markersize=4, alpha=0.8, label=self.ch2_name)
        
        # Add trend lines
        if len(ch1_monthly) > 1:
            z1 = np.polyfit(ch1_monthly['months_since_takeoff'], ch1_monthly['avg_views_per_video'], 1)
            p1 = np.poly1d(z1)
            ax1.plot(ch1_monthly['months_since_takeoff'], p1(ch1_monthly['months_since_takeoff']),
                    "r--", linewidth=2, alpha=0.5, label=f'{self.ch1_name} trend (slope: {z1[0]:.0f})')
        
        if len(ch2_monthly) > 1:
            z2 = np.polyfit(ch2_monthly['months_since_takeoff'], ch2_monthly['avg_views_per_video'], 1)
            p2 = np.poly1d(z2)
            ax1.plot(ch2_monthly['months_since_takeoff'], p2(ch2_monthly['months_since_takeoff']),
                    "b--", linewidth=2, alpha=0.5, label=f'{self.ch2_name} trend (slope: {z2[0]:.0f})')
        
        ax1.set_title('Average Views Per Video: Retention Comparison\n(Aligned by Months Since Takeoff)', 
                     fontsize=16, fontweight='bold')
        ax1.set_xlabel('Months Since Takeoff', fontsize=12)
        ax1.set_ylabel('Avg Views per Video', fontsize=12)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1e3):.0f}K'))
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)
        ax1.axvline(x=0, color='green', linestyle=':', linewidth=2, alpha=0.6, label='Takeoff Year Start')
        
        # Chart 2: Normalized retention (index to 100 at takeoff)
        # Get first value after takeoff (month 0 or later)
        ch1_base = ch1_monthly[ch1_monthly['months_since_takeoff'] >= 0]['avg_views_per_video'].iloc[0] if len(ch1_monthly[ch1_monthly['months_since_takeoff'] >= 0]) > 0 else 1
        ch2_base = ch2_monthly[ch2_monthly['months_since_takeoff'] >= 0]['avg_views_per_video'].iloc[0] if len(ch2_monthly[ch2_monthly['months_since_takeoff'] >= 0]) > 0 else 1
        
        ch1_monthly['retention_index'] = (ch1_monthly['avg_views_per_video'] / ch1_base) * 100
        ch2_monthly['retention_index'] = (ch2_monthly['avg_views_per_video'] / ch2_base) * 100
        
        ax2.plot(ch1_monthly['months_since_takeoff'], ch1_monthly['retention_index'],
                linewidth=3, color='#FF0000', marker='o', markersize=4, alpha=0.8, label=self.ch1_name)
        ax2.plot(ch2_monthly['months_since_takeoff'], ch2_monthly['retention_index'],
                linewidth=3, color='#0000FF', marker='s', markersize=4, alpha=0.8, label=self.ch2_name)
        
        ax2.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Takeoff Baseline (100)')
        ax2.set_title('Normalized Retention Index (100 = Takeoff Year Performance)', 
                     fontsize=16, fontweight='bold')
        ax2.set_xlabel('Months Since Takeoff', fontsize=12)
        ax2.set_ylabel('Retention Index', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        
        # Chart 3: Upload frequency comparison
        ax3.bar(ch1_monthly['months_since_takeoff'] - 0.2, ch1_monthly['video_count'],
               width=0.4, color='#FF0000', alpha=0.7, label=self.ch1_name)
        ax3.bar(ch2_monthly['months_since_takeoff'] + 0.2, ch2_monthly['video_count'],
               width=0.4, color='#0000FF', alpha=0.7, label=self.ch2_name)
        
        ax3.set_title('Upload Frequency Comparison', fontsize=16, fontweight='bold')
        ax3.set_xlabel('Months Since Takeoff', fontsize=12)
        ax3.set_ylabel('Videos Uploaded', fontsize=12)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def plot_growth_rate_overlay(self, save_path: str = "comparison_growth_rates.png"):
        """
        Overlay both channels' rolling growth rates
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
        
        # Align by takeoff
        df1_aligned = self._align_by_takeoff(self.df1.copy(), self.ch1_takeoff_year)
        df2_aligned = self._align_by_takeoff(self.df2.copy(), self.ch2_takeoff_year)
        
        # Group by months since takeoff
        ch1_monthly_views = df1_aligned.groupby('months_since_takeoff')['view_count'].sum()
        ch2_monthly_views = df2_aligned.groupby('months_since_takeoff')['view_count'].sum()
        
        # Calculate growth rates
        ch1_growth = ch1_monthly_views.pct_change() * 100
        ch2_growth = ch2_monthly_views.pct_change() * 100
        
        # Rolling averages (6-month)
        ch1_rolling = ch1_growth.rolling(window=6, min_periods=1).mean()
        ch2_rolling = ch2_growth.rolling(window=6, min_periods=1).mean()
        
        # Chart 1: Rolling growth rates
        x1 = ch1_rolling.index
        x2 = ch2_rolling.index
        
        ax1.plot(x1, ch1_rolling.values, linewidth=3, color='#FF0000', marker='o', 
                markersize=4, alpha=0.8, label=self.ch1_name)
        ax1.plot(x2, ch2_rolling.values, linewidth=3, color='#0000FF', marker='s',
                markersize=4, alpha=0.8, label=self.ch2_name)
        
        # Add trend lines
        if len(ch1_rolling) > 1:
            valid_mask = ~np.isnan(ch1_rolling.values)
            if valid_mask.sum() > 1:
                z1 = np.polyfit(x1[valid_mask], ch1_rolling.values[valid_mask], 1)
                p1 = np.poly1d(z1)
                ax1.plot(x1, p1(x1), "r--", linewidth=2, alpha=0.5,
                        label=f'{self.ch1_name} decay: {z1[0]:.2f}%/mo')
        
        if len(ch2_rolling) > 1:
            valid_mask = ~np.isnan(ch2_rolling.values)
            if valid_mask.sum() > 1:
                z2 = np.polyfit(x2[valid_mask], ch2_rolling.values[valid_mask], 1)
                p2 = np.poly1d(z2)
                ax2_line = ax1.plot(x2, p2(x2), "b--", linewidth=2, alpha=0.5,
                        label=f'{self.ch2_name} decay: {z2[0]:.2f}%/mo')
        
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax1.axvline(x=0, color='green', linestyle=':', linewidth=2, alpha=0.6)
        ax1.set_title('6-Month Rolling Growth Rate Comparison\n(Aligned by Months Since Takeoff)', 
                     fontsize=16, fontweight='bold')
        ax1.set_xlabel('Months Since Takeoff', fontsize=12)
        ax1.set_ylabel('Growth Rate (%)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10, loc='upper right')
        
        # Chart 2: Growth rate volatility (rolling std dev)
        ch1_volatility = ch1_growth.rolling(window=6, min_periods=1).std()
        ch2_volatility = ch2_growth.rolling(window=6, min_periods=1).std()
        
        ax2.plot(ch1_volatility.index, ch1_volatility.values, linewidth=3, color='#FF0000',
                marker='o', markersize=4, alpha=0.8, label=f'{self.ch1_name}')
        ax2.plot(ch2_volatility.index, ch2_volatility.values, linewidth=3, color='#0000FF',
                marker='s', markersize=4, alpha=0.8, label=f'{self.ch2_name}')
        
        ax2.set_title('Growth Rate Volatility Comparison\n(Lower = More Stable/Sustainable)', 
                     fontsize=16, fontweight='bold')
        ax2.set_xlabel('Months Since Takeoff', fontsize=12)
        ax2.set_ylabel('Growth Rate Std Dev (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        ax2.axvline(x=0, color='green', linestyle=':', linewidth=2, alpha=0.6)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved: {save_path}")
        plt.close()
    
    def generate_comparison_report(self):
        """
        Print comprehensive comparison statistics
        """
        print("\n" + "=" * 80)
        print("📊 CHANNEL COMPARISON REPORT")
        print("=" * 80)
        
        # Align by takeoff
        df1_aligned = self._align_by_takeoff(self.df1.copy(), self.ch1_takeoff_year)
        df2_aligned = self._align_by_takeoff(self.df2.copy(), self.ch2_takeoff_year)
        
        # Basic stats
        print(f"\n{'METRIC':<40} {self.ch1_name:<20} {self.ch2_name:<20}")
        print("-" * 80)
        print(f"{'Total Videos':<40} {len(self.df1):<20,} {len(self.df2):<20,}")
        print(f"{'Total Views':<40} {self.df1['view_count'].sum():<20,} {self.df2['view_count'].sum():<20,}")
        print(f"{'Average Views per Video':<40} {self.df1['view_count'].mean():<20,.0f} {self.df2['view_count'].mean():<20,.0f}")
        print(f"{'Median Views per Video':<40} {self.df1['view_count'].median():<20,.0f} {self.df2['view_count'].median():<20,.0f}")
        
        # Takeoff analysis
        print(f"\n{'TAKEOFF ANALYSIS':<40}")
        print("-" * 80)
        print(f"{'Identified Takeoff Year':<40} {self.ch1_takeoff_year:<20} {self.ch2_takeoff_year:<20}")
        
        # Post-takeoff metrics
        ch1_post = df1_aligned[df1_aligned['months_since_takeoff'] >= 0]
        ch2_post = df2_aligned[df2_aligned['months_since_takeoff'] >= 0]
        
        print(f"{'Videos Post-Takeoff':<40} {len(ch1_post):<20,} {len(ch2_post):<20,}")
        print(f"{'Avg Views Post-Takeoff':<40} {ch1_post['view_count'].mean():<20,.0f} {ch2_post['view_count'].mean():<20,.0f}")
        
        # Retention metrics (views per video trend)
        ch1_monthly = df1_aligned.groupby('months_since_takeoff')['view_count'].mean()
        ch2_monthly = df2_aligned.groupby('months_since_takeoff')['view_count'].mean()
        
        if len(ch1_monthly) > 12:
            ch1_early = ch1_monthly.iloc[:12].mean()
            ch1_late = ch1_monthly.iloc[-12:].mean()
            ch1_retention_change = ((ch1_late - ch1_early) / ch1_early) * 100
        else:
            ch1_retention_change = 0
        
        if len(ch2_monthly) > 12:
            ch2_early = ch2_monthly.iloc[:12].mean()
            ch2_late = ch2_monthly.iloc[-12:].mean()
            ch2_retention_change = ((ch2_late - ch2_early) / ch2_early) * 100
        else:
            ch2_retention_change = 0
        
        print(f"\n{'RETENTION ANALYSIS':<40}")
        print("-" * 80)
        print(f"{'Views/Video Change (First 12mo vs Last 12mo)':<40} {ch1_retention_change:<20.1f}% {ch2_retention_change:<20.1f}%")
        
        # Growth rate decay
        ch1_monthly_total = df1_aligned.groupby('months_since_takeoff')['view_count'].sum()
        ch2_monthly_total = df2_aligned.groupby('months_since_takeoff')['view_count'].sum()
        
        ch1_growth = ch1_monthly_total.pct_change() * 100
        ch2_growth = ch2_monthly_total.pct_change() * 100
        
        ch1_rolling = ch1_growth.rolling(window=6, min_periods=1).mean()
        ch2_rolling = ch2_growth.rolling(window=6, min_periods=1).mean()
        
        # Calculate decay slopes
        if len(ch1_rolling) > 1:
            valid = ~np.isnan(ch1_rolling.values)
            if valid.sum() > 1:
                z1 = np.polyfit(ch1_rolling.index[valid], ch1_rolling.values[valid], 1)
                ch1_decay_slope = z1[0]
            else:
                ch1_decay_slope = 0
        else:
            ch1_decay_slope = 0
        
        if len(ch2_rolling) > 1:
            valid = ~np.isnan(ch2_rolling.values)
            if valid.sum() > 1:
                z2 = np.polyfit(ch2_rolling.index[valid], ch2_rolling.values[valid], 1)
                ch2_decay_slope = z2[0]
            else:
                ch2_decay_slope = 0
        else:
            ch2_decay_slope = 0
        
        print(f"\n{'GROWTH DECAY ANALYSIS':<40}")
        print("-" * 80)
        print(f"{'Growth Rate Decay Slope (%/month)':<40} {ch1_decay_slope:<20.3f} {ch2_decay_slope:<20.3f}")
        print(f"{'Avg Early Growth (first 12mo post-takeoff)':<40} {ch1_rolling[ch1_rolling.index <= 12].mean():<20.1f}% {ch2_rolling[ch2_rolling.index <= 12].mean():<20.1f}%")
        print(f"{'Avg Recent Growth (last 12mo)':<40} {ch1_rolling.iloc[-12:].mean():<20.1f}% {ch2_rolling.iloc[-12:].mean():<20.1f}%")
        
        # Volatility
        ch1_volatility = ch1_growth.rolling(window=6).std().mean()
        ch2_volatility = ch2_growth.rolling(window=6).std().mean()
        
        print(f"\n{'STABILITY METRICS':<40}")
        print("-" * 80)
        print(f"{'Average Growth Volatility (Std Dev %)':<40} {ch1_volatility:<20.1f} {ch2_volatility:<20.1f}")
        print(f"{'Interpretation':<40} {'Higher volatility' if ch1_volatility > ch2_volatility else 'Lower volatility':<20} {'Higher volatility' if ch2_volatility > ch1_volatility else 'Lower volatility':<20}")
        
        # Key findings
        print(f"\n{'KEY FINDINGS':<80}")
        print("=" * 80)
        
        if ch1_decay_slope < ch2_decay_slope:
            print(f"✓ {self.ch1_name} shows faster growth decay ({ch1_decay_slope:.3f}%/mo vs {ch2_decay_slope:.3f}%/mo)")
        else:
            print(f"✓ {self.ch2_name} shows faster growth decay ({ch2_decay_slope:.3f}%/mo vs {ch1_decay_slope:.3f}%/mo)")
        
        if ch1_retention_change < ch2_retention_change:
            print(f"✓ {self.ch1_name} has declining retention ({ch1_retention_change:.1f}% change), {self.ch2_name} is more stable ({ch2_retention_change:.1f}% change)")
        else:
            print(f"✓ {self.ch2_name} has declining retention ({ch2_retention_change:.1f}% change), {self.ch1_name} is more stable ({ch1_retention_change:.1f}% change)")
        
        if ch1_volatility > ch2_volatility * 1.5:
            print(f"✓ {self.ch1_name} shows significantly higher volatility (less sustainable)")
        elif ch2_volatility > ch1_volatility * 1.5:
            print(f"✓ {self.ch2_name} shows significantly higher volatility (less sustainable)")
        
        print("\n" + "=" * 80)
    
    def create_all_comparisons(self, output_dir: str = "comparisons"):
        """Generate all comparison visualizations"""
        print(f"\n🎨 Generating comparison visualizations...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        self.plot_dual_growth_decay(str(output_path / "comparison_growth_decay.png"))
        self.plot_retention_comparison(str(output_path / "comparison_retention.png"))
        self.plot_growth_rate_overlay(str(output_path / "comparison_growth_rates.png"))
        
        self.generate_comparison_report()
        
        print(f"\n✅ All comparisons complete! Saved to {output_dir}/")


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Compare two YouTube channels')
    parser.add_argument('channel1_csv', help='CSV file for first channel')
    parser.add_argument('channel2_csv', help='CSV file for second channel')
    parser.add_argument('--name1', default='Channel 1', help='Display name for first channel')
    parser.add_argument('--name2', default='Channel 2', help='Display name for second channel')
    parser.add_argument('--output', default='comparisons', help='Output directory for charts')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("YouTube Channel Comparison Tool")
    print("=" * 80)
    
    comparator = ChannelComparator(
        args.channel1_csv,
        args.channel2_csv,
        args.name1,
        args.name2
    )
    
    comparator.create_all_comparisons(args.output)


if __name__ == "__main__":
    main()

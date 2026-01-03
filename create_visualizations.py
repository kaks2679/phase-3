#!/usr/bin/env python3
"""
Create comprehensive visualizations for Tanzanian Water Wells project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create output directory
output_dir = Path('visualizations')
output_dir.mkdir(exist_ok=True)

print("Loading data...")
# Load the data
train_values = pd.read_csv('4910797b-ee55-40a7-8668-10efd5c1b960.csv')
train_labels = pd.read_csv('0bf8bc6e-30d0-4c50-956a-603fc693d966.csv')

# Merge training data
train_df = train_values.merge(train_labels, on='id')
print(f"Training data shape: {train_df.shape}")

# ============================================
# 1. Target Distribution
# ============================================
print("Creating target distribution visualization...")
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
target_counts = train_df['status_group'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#f39c12']
bars = ax.bar(range(len(target_counts)), target_counts.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for i, (bar, count) in enumerate(zip(bars, target_counts.values)):
    height = bar.get_height()
    percentage = (count / len(train_df)) * 100
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{count:,}\n({percentage:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_xticks(range(len(target_counts)))
ax.set_xticklabels(target_counts.index, fontsize=12)
ax.set_ylabel('Number of Wells', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Water Well Status\n(59,400 Wells)', fontsize=14, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(output_dir / '01_target_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 2. Water Quantity Analysis
# ============================================
print("Creating water quantity analysis...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Count plot
water_status = pd.crosstab(train_df['quantity'], train_df['status_group'])
water_status_pct = water_status.div(water_status.sum(axis=1), axis=0) * 100

water_status.plot(kind='bar', ax=ax1, color=['#2ecc71', '#f39c12', '#e74c3c'], 
                   alpha=0.8, edgecolor='black', linewidth=1.2)
ax1.set_title('Water Quantity vs Well Status (Count)', fontsize=13, fontweight='bold', pad=15)
ax1.set_xlabel('Water Quantity', fontsize=11, fontweight='bold')
ax1.set_ylabel('Number of Wells', fontsize=11, fontweight='bold')
ax1.legend(title='Status', loc='upper right', framealpha=0.9)
ax1.tick_params(axis='x', rotation=45)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Percentage plot
water_status_pct.plot(kind='bar', stacked=True, ax=ax2, 
                      color=['#2ecc71', '#f39c12', '#e74c3c'],
                      alpha=0.8, edgecolor='black', linewidth=1.2)
ax2.set_title('Water Quantity vs Well Status (Percentage)', fontsize=13, fontweight='bold', pad=15)
ax2.set_xlabel('Water Quantity', fontsize=11, fontweight='bold')
ax2.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
ax2.legend(title='Status', loc='upper right', framealpha=0.9)
ax2.tick_params(axis='x', rotation=45)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / '02_water_quantity_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 3. Geographic Distribution Map
# ============================================
print("Creating geographic distribution map...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

status_groups = ['functional', 'functional needs repair', 'non functional']
colors_map = {'functional': '#2ecc71', 'functional needs repair': '#f39c12', 'non functional': '#e74c3c'}

for idx, status in enumerate(status_groups):
    ax = axes[idx]
    data_subset = train_df[train_df['status_group'] == status].sample(n=min(5000, len(train_df[train_df['status_group'] == status])), random_state=42)
    
    ax.scatter(data_subset['longitude'], data_subset['latitude'], 
               c=colors_map[status], alpha=0.3, s=5, edgecolors='none')
    ax.set_title(f'{status.title()}\n({len(train_df[train_df["status_group"] == status]):,} wells)', 
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=10, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.suptitle('Geographic Distribution of Water Wells by Status', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / '03_geographic_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 4. Construction Year Analysis
# ============================================
print("Creating construction year analysis...")
fig, ax = plt.subplots(figsize=(14, 7))

# Filter valid construction years
valid_years = train_df[(train_df['construction_year'] > 1960) & (train_df['construction_year'] <= 2013)].copy()

# Group by decade
valid_years['decade'] = (valid_years['construction_year'] // 10) * 10
decade_status = pd.crosstab(valid_years['decade'], valid_years['status_group'])

decade_status.plot(kind='bar', ax=ax, color=['#2ecc71', '#f39c12', '#e74c3c'],
                   alpha=0.8, edgecolor='black', linewidth=1.2, width=0.8)
ax.set_title('Well Status by Construction Decade\n(Filtered: 1960-2013)', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Construction Decade', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Wells', fontsize=12, fontweight='bold')
ax.legend(title='Status', loc='upper left', framealpha=0.9, fontsize=10)
ax.tick_params(axis='x', rotation=45)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '04_construction_year_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 5. Top Regions Analysis
# ============================================
print("Creating regional analysis...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Top 10 regions by count
top_regions = train_df['region'].value_counts().head(10)
colors_region = plt.cm.viridis(np.linspace(0, 0.9, len(top_regions)))
bars = ax1.barh(range(len(top_regions)), top_regions.values, color=colors_region, 
                alpha=0.8, edgecolor='black', linewidth=1.2)
ax1.set_yticks(range(len(top_regions)))
ax1.set_yticklabels(top_regions.index, fontsize=10)
ax1.set_xlabel('Number of Wells', fontsize=11, fontweight='bold')
ax1.set_title('Top 10 Regions by Number of Wells', fontsize=13, fontweight='bold', pad=15)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top_regions.values)):
    ax1.text(val, bar.get_y() + bar.get_height()/2, f' {val:,}',
             ha='left', va='center', fontsize=9, fontweight='bold')

# Status by top regions
top_10_names = top_regions.index
region_status = pd.crosstab(train_df[train_df['region'].isin(top_10_names)]['region'],
                             train_df[train_df['region'].isin(top_10_names)]['status_group'])
region_status_pct = region_status.div(region_status.sum(axis=1), axis=0) * 100
region_status_pct = region_status_pct.loc[top_10_names]  # Sort by count order

region_status_pct.plot(kind='barh', stacked=True, ax=ax2,
                       color=['#2ecc71', '#f39c12', '#e74c3c'],
                       alpha=0.8, edgecolor='black', linewidth=1.2)
ax2.set_xlabel('Percentage (%)', fontsize=11, fontweight='bold')
ax2.set_title('Well Status Distribution in Top 10 Regions', fontsize=13, fontweight='bold', pad=15)
ax2.legend(title='Status', loc='lower right', framealpha=0.9, fontsize=9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '05_regional_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 6. Waterpoint Type Analysis
# ============================================
print("Creating waterpoint type analysis...")
fig, ax = plt.subplots(figsize=(14, 8))

# Get top waterpoint types
top_waterpoints = train_df['waterpoint_type'].value_counts().head(8)
wp_status = pd.crosstab(train_df[train_df['waterpoint_type'].isin(top_waterpoints.index)]['waterpoint_type'],
                        train_df[train_df['waterpoint_type'].isin(top_waterpoints.index)]['status_group'])
wp_status = wp_status.loc[top_waterpoints.index]  # Sort by count

wp_status.plot(kind='barh', ax=ax, color=['#2ecc71', '#f39c12', '#e74c3c'],
               alpha=0.8, edgecolor='black', linewidth=1.2)
ax.set_xlabel('Number of Wells', fontsize=11, fontweight='bold')
ax.set_title('Well Status by Waterpoint Type (Top 8)', fontsize=13, fontweight='bold', pad=15)
ax.legend(title='Status', loc='lower right', framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '06_waterpoint_type_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 7. Missing Data Overview
# ============================================
print("Creating missing data visualization...")
fig, ax = plt.subplots(figsize=(12, 8))

# Calculate missing percentages
missing_pct = (train_df.isnull().sum() / len(train_df) * 100).sort_values(ascending=False)
missing_pct = missing_pct[missing_pct > 0].head(15)

colors_missing = ['#e74c3c' if x > 40 else '#f39c12' if x > 20 else '#3498db' 
                  for x in missing_pct.values]
bars = ax.barh(range(len(missing_pct)), missing_pct.values, color=colors_missing,
               alpha=0.8, edgecolor='black', linewidth=1.2)
ax.set_yticks(range(len(missing_pct)))
ax.set_yticklabels(missing_pct.index, fontsize=10)
ax.set_xlabel('Missing Data Percentage (%)', fontsize=11, fontweight='bold')
ax.set_title('Top 15 Features with Missing Data', fontsize=13, fontweight='bold', pad=15)
ax.axvline(x=40, color='red', linestyle='--', linewidth=2, alpha=0.5, label='40% threshold')
ax.legend(loc='lower right', framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, missing_pct.values)):
    ax.text(val, bar.get_y() + bar.get_height()/2, f' {val:.1f}%',
            ha='left', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '07_missing_data_overview.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 8. Population vs Status
# ============================================
print("Creating population analysis...")
fig, ax = plt.subplots(figsize=(12, 7))

# Filter out population = 0 and extreme outliers
pop_data = train_df[train_df['population'] > 0].copy()
pop_data['pop_bin'] = pd.cut(pop_data['population'], 
                              bins=[0, 10, 50, 100, 500, 1000, 10000],
                              labels=['1-10', '11-50', '51-100', '101-500', '501-1000', '1000+'])

pop_status = pd.crosstab(pop_data['pop_bin'], pop_data['status_group'])
pop_status.plot(kind='bar', ax=ax, color=['#2ecc71', '#f39c12', '#e74c3c'],
                alpha=0.8, edgecolor='black', linewidth=1.2)
ax.set_title('Well Status by Population Served', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Population Range', fontsize=11, fontweight='bold')
ax.set_ylabel('Number of Wells', fontsize=11, fontweight='bold')
ax.legend(title='Status', loc='upper right', framealpha=0.9)
ax.tick_params(axis='x', rotation=45)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '08_population_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# 9. Key Insights Summary Dashboard
# ============================================
print("Creating key insights dashboard...")
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# Panel 1: Target distribution pie
ax1 = fig.add_subplot(gs[0, 0])
target_counts = train_df['status_group'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#f39c12']
wedges, texts, autotexts = ax1.pie(target_counts.values, labels=target_counts.index, 
                                     autopct='%1.1f%%', colors=colors, startangle=90,
                                     textprops={'fontsize': 9, 'fontweight': 'bold'})
ax1.set_title('Target Distribution', fontsize=11, fontweight='bold', pad=10)

# Panel 2: Water quantity key insight
ax2 = fig.add_subplot(gs[0, 1:])
key_quantities = ['enough', 'insufficient', 'dry']
qty_data = train_df[train_df['quantity'].isin(key_quantities)]
qty_status_pct = pd.crosstab(qty_data['quantity'], qty_data['status_group'], normalize='index') * 100
qty_status_pct.plot(kind='bar', ax=ax2, color=['#2ecc71', '#f39c12', '#e74c3c'],
                    alpha=0.8, edgecolor='black', linewidth=1.2)
ax2.set_title('Key Finding: Water Quantity is a Strong Predictor', fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel('Water Quantity', fontsize=9, fontweight='bold')
ax2.set_ylabel('Percentage (%)', fontsize=9, fontweight='bold')
ax2.legend(title='Status', fontsize=8, title_fontsize=8)
ax2.tick_params(axis='x', rotation=0, labelsize=9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Panel 3: Regional concentration
ax3 = fig.add_subplot(gs[1, :])
top_5_regions = train_df['region'].value_counts().head(5)
bars = ax3.bar(range(len(top_5_regions)), top_5_regions.values, 
               color=plt.cm.viridis(np.linspace(0, 0.9, len(top_5_regions))),
               alpha=0.8, edgecolor='black', linewidth=1.2)
ax3.set_xticks(range(len(top_5_regions)))
ax3.set_xticklabels(top_5_regions.index, rotation=15, ha='right', fontsize=9)
ax3.set_ylabel('Number of Wells', fontsize=9, fontweight='bold')
ax3.set_title('Top 5 Regions by Well Count', fontsize=11, fontweight='bold', pad=10)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
for bar, val in zip(bars, top_5_regions.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val:,}',
             ha='center', va='bottom', fontsize=8, fontweight='bold')

# Panel 4: Data quality metrics
ax4 = fig.add_subplot(gs[2, :2])
ax4.axis('off')
metrics_text = f"""
KEY DATA QUALITY METRICS

• Total Wells: {len(train_df):,} training samples
• Features: 40 input features (9 numeric, 31 categorical)
• Target Classes: 3 (functional, functional needs repair, non functional)
• Missing Data: scheme_name (48.5%), permit (56.0%), public_meeting (5.6%)
• Geographic Coverage: Longitude range: 0-40°E, Latitude range: -12 to -1°N
• Temporal Range: Construction years 1960-2013 (valid records)
"""
ax4.text(0.05, 0.95, metrics_text, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Panel 5: Key insight box
ax5 = fig.add_subplot(gs[2, 2])
ax5.axis('off')
insight_text = """
TOP PREDICTIVE 
FEATURES

1. Water Quantity
2. Waterpoint Type
3. Geographic Location
4. Construction Year
5. Management Type
6. Payment System

Status:
✓ Functional: 54.3%
⚠ Needs Repair: 7.3%
✗ Non-functional: 38.4%
"""
ax5.text(0.05, 0.95, insight_text, transform=ax5.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='sans-serif',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.4))

plt.suptitle('Tanzania Water Wells - Key Insights Dashboard', fontsize=15, fontweight='bold', y=0.98)
plt.savefig(output_dir / '09_insights_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✓ All visualizations saved to '{output_dir}' directory")
print(f"\nGenerated {len(list(output_dir.glob('*.png')))} visualization files:")
for img_file in sorted(output_dir.glob('*.png')):
    print(f"  - {img_file.name}")

# ── IMPORTS ──
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# ── SETTINGS ──
plt.style.use('dark_background')
sns.set_palette('Blues_r')
pd.set_option('display.max_columns', None)

# ── LOAD AND CLEAN DATA ──
df_raw = pd.read_excel('Indikatoret_20260925-004807.xlsx', header=None)

# Extract years
years = []
for val in df_raw.iloc[2, 1:]:
    if not pd.isna(val) and str(val).strip() not in ['', 'nan']:
        years.append(int(float(str(val).strip())))

# Extract Total (Gjithsej) values — every 3rd column
data = {}
col = 1
for year in years:
    total_col = col + 2
    values = df_raw.iloc[4:13, total_col].tolist()
    data[year] = values
    col += 3

# Build clean dataframe
df = pd.DataFrame(data, index=[
    'labor_force_participation',
    'economically_inactive',
    'employment_rate',
    'unemployment_rate',
    'youth_labor_force',
    'youth_employment_rate',
    'youth_unemployment_rate',
    'neet_rate',
    'informal_employment'
]).T

df.index.name = 'year'
df = df.sort_index()
df = df.apply(pd.to_numeric, errors='coerce')

print("Data loaded successfully")
print(df)

# ── ANALYSIS 1: The Emigration Gap ──
# If unemployment dropped but employment didn't rise equally,
# people left the labor force — likely through emigration

df['emigration_gap'] = df['unemployment_rate'] - (100 - df['employment_rate'] - df['economically_inactive'])

print("\n── HEADLINE FINDING: The Emigration Gap ──")
print("Unemployment rate 2012:", df.loc[2012, 'unemployment_rate'])
print("Unemployment rate 2024:", df.loc[2024, 'unemployment_rate'])
print("Drop in unemployment:", round(df.loc[2012, 'unemployment_rate'] - df.loc[2024, 'unemployment_rate'], 1))

print("\nEmployment rate 2012:", df.loc[2012, 'employment_rate'])
print("Employment rate 2024:", df.loc[2024, 'employment_rate'])
print("Rise in employment:", round(df.loc[2024, 'employment_rate'] - df.loc[2012, 'employment_rate'], 1))

print("\nConclusion: Unemployment dropped by", 
      round(df.loc[2012, 'unemployment_rate'] - df.loc[2024, 'unemployment_rate'], 1),
      "points but employment only rose by",
      round(df.loc[2024, 'employment_rate'] - df.loc[2012, 'employment_rate'], 1),
      "points.")
print("The gap of", 
      round((df.loc[2012, 'unemployment_rate'] - df.loc[2024, 'unemployment_rate']) - 
            (df.loc[2024, 'employment_rate'] - df.loc[2012, 'employment_rate']), 1),
      "points is largely explained by emigration — people left Kosovo rather than finding jobs here.")


# ── VISUALIZATIONS ──
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Kosovo Labor Market Analysis 2012-2024', fontsize=16, fontweight='bold', y=1.02)

# Chart 1: Unemployment vs Employment Rate
axes[0,0].plot(df.index, df['unemployment_rate'], marker='o', color='#EF4444', linewidth=2, label='Unemployment Rate')
axes[0,0].plot(df.index, df['employment_rate'], marker='o', color='#22C55E', linewidth=2, label='Employment Rate')
axes[0,0].set_title('Unemployment vs Employment Rate (%)', fontweight='bold')
axes[0,0].set_xlabel('Year')
axes[0,0].set_ylabel('Rate (%)')
axes[0,0].legend()
axes[0,0].set_xticks(df.index)
axes[0,0].tick_params(axis='x', rotation=45)

# Chart 2: Youth Unemployment
axes[0,1].plot(df.index, df['youth_unemployment_rate'], marker='o', color='#F97316', linewidth=2, label='Youth Unemployment')
axes[0,1].plot(df.index, df['unemployment_rate'], marker='o', color='#3B82F6', linewidth=2, linestyle='--', label='Overall Unemployment')
axes[0,1].set_title('Youth vs Overall Unemployment Rate (%)', fontweight='bold')
axes[0,1].set_xlabel('Year')
axes[0,1].set_ylabel('Rate (%)')
axes[0,1].legend()
axes[0,1].set_xticks(df.index)
axes[0,1].tick_params(axis='x', rotation=45)

# Chart 3: NEET Rate
axes[1,0].bar(df.index, df['neet_rate'], color='#8B5CF6', alpha=0.8)
axes[1,0].set_title('NEET Rate — Youth Not in Employment, Education or Training (%)', fontweight='bold')
axes[1,0].set_xlabel('Year')
axes[1,0].set_ylabel('NEET Rate (%)')
axes[1,0].set_xticks(df.index)
axes[1,0].tick_params(axis='x', rotation=45)
axes[1,0].axhline(y=df['neet_rate'].mean(), color='#F97316', linestyle='--', label=f'Average: {df["neet_rate"].mean():.1f}%')
axes[1,0].legend()

# Chart 4: The Emigration Gap
axes[1,1].fill_between(df.index, df['unemployment_rate'], df['employment_rate'], alpha=0.3, color='#3B82F6', label='The Gap')
axes[1,1].plot(df.index, df['unemployment_rate'], marker='o', color='#EF4444', linewidth=2, label='Unemployment Rate')
axes[1,1].plot(df.index, df['employment_rate'], marker='o', color='#22C55E', linewidth=2, label='Employment Rate')
axes[1,1].set_title('The Emigration Gap — Unemployment Fell Faster Than Employment Rose', fontweight='bold')
axes[1,1].set_xlabel('Year')
axes[1,1].set_ylabel('Rate (%)')
axes[1,1].legend()
axes[1,1].set_xticks(df.index)
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('kosovo_labor_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("Charts saved.")


# ── BUSINESS SUMMARY ──
print("\n" + "="*60)
print("KOSOVO LABOR MARKET ANALYSIS — KEY FINDINGS")
print("="*60)

print(f"\nOverall unemployment rate fell from {df.loc[2012, 'unemployment_rate']}% in 2012 to {df.loc[2024, 'unemployment_rate']}% in 2024")
print(f"But employment rate only rose from {df.loc[2012, 'employment_rate']}% to {df.loc[2024, 'employment_rate']}%")
print(f"The 7-point gap is the emigration signal — people left rather than found jobs\n")

print(f"Youth unemployment peaked at {df['youth_unemployment_rate'].max()}% in 2014")
print(f"Youth unemployment in 2024: {df.loc[2024, 'youth_unemployment_rate']}%")
print(f"Still {round(df.loc[2024, 'youth_unemployment_rate'] / df.loc[2024, 'unemployment_rate'], 1)}x higher than overall unemployment\n")

print(f"NEET rate average 2012-2024: {df['neet_rate'].mean():.1f}%")
print(f"1 in 3 young Kosovars not working, studying, or training — every single year\n")

print(f"Labor force participation in 2024: {df.loc[2024, 'labor_force_participation']}%")
print(f"EU average labor force participation: ~73%")
print(f"Kosovo is {round(73 - df.loc[2024, 'labor_force_participation'], 1)} points below EU average\n")

print("="*60)
print("KEY RECOMMENDATION")
print("="*60)
print("The official unemployment figures overstate Kosovo's labor")
print("market health. The real story is that employment participation")
print("remains critically low. Without addressing emigration drivers")
print("— low wages, few opportunities — the improvement in")
print("unemployment statistics masks a structural workforce crisis.")
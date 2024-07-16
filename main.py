import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('mission_launches.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'].str.extract(r'(\w+ \w+ \d+, \d+)')[0])

# Extract month and year from Date
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Plot number of rocket launches per month
launches_per_month = df['Month'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
launches_per_month.plot(kind='bar')
plt.title('Number of Rocket Launches per Month')
plt.xlabel('Month')
plt.ylabel('Number of Launches')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

# Calculate organization with most launches per year
launch_counts = df.groupby(['Year', 'Organisation']).size().reset_index(name='Count')
max_launches_per_year = launch_counts.loc[launch_counts.groupby('Year')['Count'].idxmax()]

plt.figure(figsize=(12, 8))
bars = plt.bar(max_launches_per_year['Year'].astype(str), max_launches_per_year['Count'], color='skyblue')

for bar, org in zip(bars, max_launches_per_year['Organisation']):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, org, ha='center', va='bottom', rotation=90, fontsize=10)

plt.title("Organization with Most Launches Per Year")
plt.xlabel("Year")
plt.xticks(rotation=45)
plt.ylabel("Number of Launches")
plt.tight_layout()
plt.show()

# Clean Price column and calculate average cost per year
df_clean = df.dropna(subset=['Price']).copy()
df_clean['Price'] = pd.to_numeric(df_clean['Price'], errors='coerce')
df_clean = df_clean.dropna(subset=['Price'])

average_cost_per_year = df_clean.groupby('Year')['Price'].mean().reset_index()

plt.figure(figsize=(12, 8))
bars = plt.bar(average_cost_per_year['Year'].astype(str), average_cost_per_year['Price'], color='skyblue')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"${yval:.2f}M", ha='center', va='bottom', rotation=90, fontsize=10)

plt.title("Average Cost per Year Spent on Launches")
plt.xlabel("Year")
plt.xticks(rotation=45)
plt.ylabel("Average Cost (in million USD)")
plt.tight_layout()
plt.show()

# Total launches by each organization
total_launches_per_org = df.groupby('Organisation').size().reset_index(name='Count').sort_values(by='Count', ascending=False)

plt.figure(figsize=(12, 8))
bars = plt.bar(total_launches_per_org['Organisation'], total_launches_per_org['Count'], color='skyblue')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), rotation=90, ha='center', va='bottom', fontsize=10)

plt.title("Total Launches by Each Organization")
plt.xlabel("Organization")
plt.xticks(rotation=90)
plt.ylabel("Number of Launches")
plt.tight_layout()
plt.show()

# Mission status count by organization
mission_status_counts = df_clean.groupby(['Organisation', 'Mission_Status']).size().reset_index(name='Count')

plt.figure(figsize=(14, 8))
for organisation in mission_status_counts['Organisation'].unique():
    subset = mission_status_counts[mission_status_counts['Organisation'] == organisation]
    plt.bar(subset['Mission_Status'], subset['Count'], label=organisation)

plt.xlabel('Mission Status')
plt.ylabel('Count')
plt.title('Mission Status Count by Organisation')
plt.legend(title='Organisation')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Mission status percentage by organization
total_counts = mission_status_counts.groupby('Organisation')['Count'].sum().reset_index(name='Total')
mission_status_percentages = pd.merge(mission_status_counts, total_counts, on='Organisation')
mission_status_percentages['Percentage'] = (mission_status_percentages['Count'] / mission_status_percentages['Total']) * 100

pivot_table = mission_status_percentages.pivot(index='Organisation', columns='Mission_Status', values='Percentage').fillna(0)
pivot_table.plot(kind='bar', stacked=True, figsize=(14, 8))

plt.xlabel('Organisation')
plt.ylabel('Percentage')
plt.title('Percentage of Mission Status by Organisation')
plt.legend(title='Mission Status', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Mission success and failure rates over time
yearly_status_counts = df.groupby(['Year', 'Mission_Status']).size().reset_index(name='Count')
total_missions_per_year = yearly_status_counts.groupby('Year')['Count'].sum().reset_index(name='Total')
yearly_status_percentages = pd.merge(yearly_status_counts, total_missions_per_year, on='Year')
yearly_status_percentages['Percentage'] = (yearly_status_percentages['Count'] / yearly_status_percentages['Total']) * 100

pivot_table = yearly_status_percentages.pivot(index='Year', columns='Mission_Status', values='Percentage').fillna(0)

plt.figure(figsize=(14, 8))
plt.plot(pivot_table.index, pivot_table.get('Success', [0]*len(pivot_table)), label='Success Rate', marker='o')
plt.plot(pivot_table.index, pivot_table.get('Failure', [0]*len(pivot_table)), label='Failure Rate', marker='o')

plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Mission Success and Failure Rates Over Time')
plt.legend(title='Mission Status')
plt.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('mission_launches.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

df['Date'] = df['Date'].str.extract(r'(\w+ \w+ \d+, \d+)')
df['Date'] = pd.to_datetime(df['Date'])

df['Month'] = df['Date'].dt.month
launches_per_month = df['Month'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
launches_per_month.plot(kind='bar')
plt.title('Number of Rocket Launches per Month')
plt.xlabel('Month')
plt.ylabel('Number of Launches')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

df['Year'] = df['Date'].dt.year
launch_counts = df.groupby(['Year', 'Organisation']).size().reset_index(name='Count')
max_launches_per_year = launch_counts.loc[launch_counts.groupby('Year')['Count'].idxmax()]

plt.figure(figsize=(12, 8))
plt.bar(max_launches_per_year['Year'].astype(str), max_launches_per_year['Count'], color='skyblue')
plt.title("Organization with Most Launches Per Year")
plt.xlabel("Year")
plt.xticks(rotation=45)
plt.ylabel("Number of Launches")
plt.tight_layout()
plt.show()

df['Rocket_Status'].value_counts()
df["Mission_Status"].value_counts()

## determine cost

df_clean = df.dropna()
df_price = df_clean['Price']

plt.figure(figsize=(12, 8))
plt.bar(df_price['Year'].astype(str), max_launches_per_year['Count'], color='skyblue')
plt.title("Organization with Most Launches Per Year")
plt.xlabel("Year")
plt.xticks(rotation=45)
plt.ylabel("Number of Launches")
plt.tight_layout()
plt.show()

## determine success or failure rate by orgainization

## determine if launches have become more succesfull as time as progressed
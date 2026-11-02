
# ==================== CODE CELL ====================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import files

uploaded = files.upload()
file_name = next(iter(uploaded))

df = pd.read_csv(file_name)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

display(df.head())


# ==================== CODE CELL ====================
print("Column names:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

print("\nFirst 5 rows:")
display(df.head())

print("\nLast 5 rows:")
display(df.tail())

print("\nStatistical summary:")
display(df.describe(include="all"))

print("\nMissing values:")
print(df.isnull().sum())


# ==================== CODE CELL ====================
# Remove unnecessary index column
df = df.loc[
    :, ~df.columns.astype(str).str.startswith("Unnamed")
].copy()

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Clean text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Replace empty strings with missing values
df = df.replace(r"^\s*$", np.nan, regex=True)

# Check and remove duplicate rows
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates().copy()

print("\nShape after cleaning:", df.shape)
print("\nColumns after cleaning:")
print(df.columns.tolist())

display(df.head())


# ==================== CODE CELL ====================
# Columns that should contain numerical values
numeric_columns = [
    "Mat", "Inns", "NO", "Runs", "Ave",
    "BF", "SR", "100", "50", "0", "4s", "6s"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )

# Highest score: remove the not-out marker (*) before conversion
if "HS" in df.columns:
    df["HS_NotOut"] = df["HS"].astype(str).str.contains(
        r"\*", regex=True
    )
    df["HS_Numeric"] = pd.to_numeric(
        df["HS"].astype(str).str.replace("*", "", regex=False),
        errors="coerce"
    )

print("Data types after conversion:")
print(df.dtypes)

display(df.head())


# ==================== CODE CELL ====================
print("Missing values:")
print(df.isnull().sum())

# Save cleaned data
df.to_csv("cleaned_cricket_dataset.csv", index=False)

print("\nCleaned dataset saved successfully!")

files.download("cleaned_cricket_dataset.csv")


# ==================== CODE CELL ====================
numeric_df = df.select_dtypes(include=np.number)

print("Descriptive statistics:")
display(numeric_df.describe())

print("\nMean:")
display(numeric_df.mean().to_frame("Mean"))

print("\nMedian:")
display(numeric_df.median().to_frame("Median"))

print("\nStandard deviation:")
display(numeric_df.std().to_frame("Standard Deviation"))

print("\nMinimum values:")
display(numeric_df.min().to_frame("Minimum"))

print("\nMaximum values:")
display(numeric_df.max().to_frame("Maximum"))


# ==================== CODE CELL ====================
top_scorers = df.sort_values(
    by="Runs", ascending=False
).head(10)

print("Top 10 players by total runs:")
display(top_scorers[["Player", "Runs", "Mat", "Ave", "SR"]])


# ==================== CODE CELL ====================
df["Start_Year"] = pd.to_numeric(
    df["Span"].astype(str).str.extract(r"(\d{4})")[0],
    errors="coerce"
)

career_groups = df.groupby(
    "Start_Year"
).agg(
    Number_of_Players=("Player", "count"),
    Average_Runs=("Runs", "mean"),
    Average_Batting_Average=("Ave", "mean"),
    Average_Strike_Rate=("SR", "mean")
).round(2)

print("Player statistics by career starting year:")
display(career_groups)


# ==================== CODE CELL ====================
skew_columns = [
    "Mat", "Inns", "Runs", "Ave", "SR",
    "100", "50", "BF", "4s", "6s"
]

skew_columns = [
    col for col in skew_columns if col in df.columns
]

print("Skewness of batting statistics:")
display(df[skew_columns].skew().to_frame("Skewness"))


# ==================== CODE CELL ====================
correlation_columns = [
    "Mat", "Inns", "Runs", "Ave", "SR",
    "100", "50", "BF", "4s", "6s",
    "HS_Numeric"
]

correlation_columns = [
    col for col in correlation_columns if col in df.columns
]

correlation = df[correlation_columns].corr()

print("Correlation between batting statistics:")
display(correlation.round(2))


# ==================== CODE CELL ====================
sns.set_theme(style="whitegrid")

print("Matplotlib and Seaborn are ready!")


# ==================== CODE CELL ====================
top_10 = df.nlargest(10, "Runs")

plt.figure(figsize=(12, 6))

sns.barplot(
    data=top_10,
    x="Player",
    y="Runs"
)

plt.title("Top 10 Cricket Players by Total Runs")
plt.xlabel("Player")
plt.ylabel("Total Runs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ==================== CODE CELL ====================
plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="Ave",
    bins=15,
    kde=True
)

plt.title("Distribution of Batting Averages")
plt.xlabel("Batting Average")
plt.ylabel("Number of Players")
plt.tight_layout()
plt.show()


# ==================== CODE CELL ====================
plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=df,
    x="Mat",
    y="Runs",
    hue="Ave",
    size="SR",
    sizes=(30, 200)
)

plt.title("Matches Played vs Total Runs")
plt.xlabel("Matches Played")
plt.ylabel("Total Runs")
plt.tight_layout()
plt.show()


# ==================== CODE CELL ====================
top_centuries = df.nlargest(6, "100")

plt.figure(figsize=(8, 8))

plt.pie(
    top_centuries["100"],
    labels=top_centuries["Player"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribution of Centuries Among the Top 6 Players")
plt.tight_layout()
plt.show()


# ==================== CODE CELL ====================
heatmap_columns = [
    "Mat", "Inns", "Runs", "Ave", "SR",
    "100", "50", "BF", "4s", "6s",
    "HS_Numeric"
]

heatmap_columns = [
    col for col in heatmap_columns if col in df.columns
]

plt.figure(figsize=(11, 8))

sns.heatmap(
    df[heatmap_columns].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap of Batting Statistics")
plt.tight_layout()
plt.show()


# ==================== CODE CELL ====================
yearly_runs = (
    df.dropna(subset=["Start_Year"])
      .groupby("Start_Year")["Runs"]
      .mean()
      .sort_index()
)

plt.figure(figsize=(12, 5))

plt.plot(
    yearly_runs.index,
    yearly_runs.values,
    marker="o"
)

plt.title("Average Total Runs by Career Starting Year")
plt.xlabel("Career Starting Year")
plt.ylabel("Average Total Runs")
plt.tight_layout()
plt.show()


# ==================== CODE CELL ====================
!pip -q install beautifulsoup4 requests

import requests
from bs4 import BeautifulSoup
import pandas as pd


# ==================== CODE CELL ====================
url = "https://www.espncricinfo.com/"

try:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; StudentProject/1.0)"},
        timeout=15
    )

    print("HTTP Status Code:", response.status_code)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract page title
    page_title = soup.title.get_text(strip=True) if soup.title else "No title found"

    # Extract headings
    headings = [
        heading.get_text(" ", strip=True)
        for heading in soup.find_all(["h1", "h2", "h3"])
        if heading.get_text(" ", strip=True)
    ]

    # Extract links
    links = []
    for a in soup.find_all("a", href=True):
        text_value = a.get_text(" ", strip=True)
        if text_value:
            links.append({
                "Link_Text": text_value,
                "URL": requests.compat.urljoin(url, a["href"])
            })

    print("\nPage title:", page_title)
    print("\nExtracted headings:")
    print(headings[:10])

    links_df = pd.DataFrame(links)
    print("\nExtracted links:")
    display(links_df.head(10))

except requests.exceptions.RequestException as e:
    print("Could not access the live webpage:", e)
    print("Use the local HTML fallback cell below to demonstrate parsing.")


# ==================== CODE CELL ====================
print("=" * 50)
print("HISTORICAL CRICKET BATTING ANALYSIS")
print("=" * 50)

print("Total players:", len(df))
print("Total columns:", len(df.columns))

print("\nTop 5 run scorers:")
display(
    df.nlargest(5, "Runs")[
        ["Player", "Runs", "Mat", "Ave", "SR", "100", "50"]
    ]
)

print("\nTop 5 players by centuries:")
display(
    df.nlargest(5, "100")[
        ["Player", "100", "Runs", "Ave"]
    ]
)

print("\nTop 5 players by batting average:")
display(
    df.nlargest(5, "Ave")[
        ["Player", "Ave", "Runs", "Mat"]
    ]
)

print("\nMissing values:")
print(df.isnull().sum())

print("\nConclusion:")
print(
    "This project uses Python to inspect and clean cricket batting data, "
    "calculate statistical measures, visualize player performance, "
    "study relationships between batting statistics, and demonstrate "
    "web scraping with Requests and BeautifulSoup."
)


# ==================== CODE CELL ====================




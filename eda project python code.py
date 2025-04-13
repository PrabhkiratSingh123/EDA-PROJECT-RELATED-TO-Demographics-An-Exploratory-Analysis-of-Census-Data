import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

# Load dataset
df = pd.read_csv(r"C:\Users\ssard\OneDrive\Documents\Dataset for project.csv")

# Display dataset description
print("📝 Dataset Description:\n")
print(df.describe(include="all"))
print("\n📊 Columns:\n", df.columns)

# Labels & sizes for treemap
labels = [
    "Total Population\n67,151,764",
    "Born within India\n66,333,160",
    "Born in the place of enumeration\n38,688,772",
    "Within the state of enumeration\n40,578,120",
    "States in India\nbeyond the state of enumeration\n25,755,040",
    "Uttar Pradesh\n11,619,444"
]
sizes = [67151764, 66333160, 38688772, 40578120, 25755040, 11619444]
colors = ['#a2d4c5', '#ffffcc', '#ffb3b3', '#d5ccff', '#a3c2c2', '#ffcc99']

# Clean numeric columns
cols_to_convert = [
    "Total Persons", "Total Males", "Total Females",
    "Rural Persons", "Rural Males", "Rural Females",
    "Urban Persons", "Urban Males", "Urban Females"
]
for col in cols_to_convert:
    df[col] = df[col].str.replace(",", "").astype(int)

# Aggregated data
gender_counts = df[["Total Males", "Total Females"]].sum()
urban_rural = df[["Urban Persons", "Rural Persons"]].sum()
birthplace_counts = df.groupby("Birth place ")["Total Persons"].sum().sort_values(ascending=False)
age_group_dist = df.groupby("Age-group")["Total Persons"].sum().reset_index()
top_birthplaces = birthplace_counts.head(6)
df_birth_top = df[df["Birth place "].isin(top_birthplaces.index)]

# Set seaborn style
sns.set(style="whitegrid")

# 1. Donut Chart - Gender Distribution
plt.figure(figsize=(6, 6))
plt.pie(gender_counts, labels=gender_counts.index, startangle=90,
        autopct="%1.1f%%", colors=["#5DADE2", "#F1948A"], wedgeprops=dict(width=0.4))
plt.title("Gender Distribution", fontsize=16)
plt.show()

# 2. Barplot - Urban vs Rural
plt.figure(figsize=(6, 5))
sns.barplot(x=urban_rural.index, y=urban_rural.values, palette="Accent")
plt.title("Urban vs Rural Population", fontsize=16)
plt.ylabel("Population")
plt.show()

# 3. Treemap - Top Birthplaces
plt.figure(figsize=(12, 6))
squarify.plot(sizes=sizes, label=labels, color=colors, pad=True, text_kwargs={'fontsize': 10})
plt.axis('off')
plt.title("Top 6 Birthplaces by Population", fontsize=16)
plt.show()

# 4. Lineplot - Age Group
plt.figure(figsize=(8, 5))
sns.lineplot(data=age_group_dist, x="Age-group", y="Total Persons", marker="o", color="#E67E22")
plt.title("Age Group Distribution", fontsize=16)
plt.xticks(rotation=45)
plt.show()

# 5. Heatmap - Correlation
plt.figure(figsize=(8, 6))
corr = df[cols_to_convert].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"shrink": 0.8})
plt.title("Demographic Correlation", fontsize=16)
plt.show()

# 6. Violin Plot - Population by Birthplace (Top 6)
plt.figure(figsize=(10, 6))
sns.violinplot(data=df_birth_top, x="Birth place ", y="Total Persons", palette="pastel")
plt.title("Population Distribution in Top Birthplaces", fontsize=16)
plt.xlabel("Birthplace")
plt.ylabel("Total Persons")
plt.xticks(rotation=45)
plt.show()



# 7. Pie Chart - Urban vs Rural Persons
plt.figure(figsize=(6, 6))
plt.pie(urban_rural, labels=urban_rural.index, autopct='%1.1f%%',
        startangle=140, colors=["#82E0AA", "#F5B7B1"])
plt.title("Urban vs Rural Split", fontsize=16)
plt.show()

# 🔚 Combined Grid of 4 Charts (Donut, Bar, Line, Pie)
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Gender Donut Chart
axs[0, 0].pie(gender_counts, labels=gender_counts.index, startangle=90,
              autopct="%1.1f%%", colors=["#5DADE2", "#F1948A"], wedgeprops=dict(width=0.4))
axs[0, 0].set_title("Gender Distribution")

# Urban vs Rural Barplot
sns.barplot(x=urban_rural.index, y=urban_rural.values, palette="Accent", ax=axs[0, 1])
axs[0, 1].set_title("Urban vs Rural Population")

# Age Group Line Plot
sns.lineplot(data=age_group_dist, x="Age-group", y="Total Persons", marker="o",
             color="#E67E22", ax=axs[1, 0])
axs[1, 0].set_title("Age Group Distribution")
axs[1, 0].tick_params(axis='x', rotation=45)

# Urban vs Rural Pie Chart
axs[1, 1].pie(urban_rural, labels=urban_rural.index, autopct='%1.1f%%',
              startangle=140, colors=["#82E0AA", "#F5B7B1"])
axs[1, 1].set_title("Urban vs Rural Split")

plt.tight_layout()
plt.suptitle("📊 Combined Demographic Dashboard", fontsize=18, y=1.03)
plt.show()

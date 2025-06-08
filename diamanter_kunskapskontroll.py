import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Skapar en dataframe och tar bort all data med nullvärden
data = pd.read_csv('./diamonds/diamonds.csv')
df = pd.DataFrame(data).dropna()

# Ta bort rader utan data
df = pd.DataFrame(data).dropna()

# Ta bort felaktig data för storlek
df = df[(df['x'] != 0) & (df['y'] != 0) & (df['z'] != 0)]

# Sortera baserat på carat
df = df[(df['carat'] <= 2)]

df = df.rename(columns={df.columns[0]: "id"})

colored_filtered_diamonds = df[df['color'].isin(['D', 'E', 'F', 'G'])]

g_sorted_by_clarity = colored_filtered_diamonds[
    colored_filtered_diamonds['clarity'].isin(['VVS1', 'VVS2', 'VS1', 'VS2', 'IF'])
]

g_sorted_by_cuts = g_sorted_by_clarity[
    g_sorted_by_clarity['cut'].isin(['Very Good', 'Ideal', 'Premium'])
]

distribution_by_cuts = g_sorted_by_cuts.groupby('cut').size()

fig, axes = plt.subplots(1, 3, tight_layout=True, figsize=(20, 6))

# 1. Piechart
axes[0].pie(
    distribution_by_cuts.values, 
    labels=distribution_by_cuts.index, 
    autopct='%1.1f%%', 
    startangle=90
)
axes[0].set_title('Fördelning av slipningar')

# 2. Scatterplot
sns.scatterplot(
    x='carat', 
    y='price', 
    hue='cut', 
    data=g_sorted_by_cuts, 
    ax=axes[1]
)
axes[1].set_xlabel('Carat')
axes[1].set_ylabel('Pris')
axes[1].set_title('Pris vs. Carat')

# Regressionslinje
sns.regplot(
    x='carat',
    y='price',
    data=g_sorted_by_cuts,
    scatter=False,
    ax=axes[1],
    color='black',
    line_kws={'linestyle': 'dashed', 'linewidth': 2}
)

# 3. Barplot
sns.barplot(
    x='price',
    y='clarity',
    data=g_sorted_by_cuts,
    ax=axes[2]
)
axes[2].set_xlabel('Pris')
axes[2].set_ylabel('Klarhet')
axes[2].set_title('Pris vs. Klarhet')


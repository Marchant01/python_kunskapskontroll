import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Ladda och rengör data
data = pd.read_csv('./diamonds/diamonds.csv')
df = pd.DataFrame(data).dropna()

# Ta bort felaktig data
df = df[(df['x'] != 0) & (df['y'] != 0) & (df['z'] != 0)]
df = df[df['carat'] <= 2]
df = df.rename(columns={df.columns[0]: "id"})

# Filtrera diamanter baserat på färg, klarhet och slipning
colored_filtered_diamonds = df[df['color'].isin(['D', 'E', 'F', 'G'])]

g_sorted_by_clarity = colored_filtered_diamonds[
    colored_filtered_diamonds['clarity'].isin(['VVS1', 'VVS2', 'VS1', 'VS2', 'IF'])
]

g_sorted_by_cuts = g_sorted_by_clarity[
    g_sorted_by_clarity['cut'].isin(['Very Good', 'Ideal', 'Premium'])
]

distribution_by_cuts = df.groupby(['cut']).size()
distribution_by_color = df.groupby(['color']).size()
avg_price_per_color = df.groupby('color')['price'].mean()

distribution_by_cuts = g_sorted_by_cuts.groupby('cut').size()

# Streamlit UI
st.title("Diamantanalys med Streamlit")
st.text(
  'Denna applikation visar en analys av diamanter baserat på färg, klarhet och slipning. ' \
  '\n\nSyftet med analysen är att utvärdera diamanternas egenskaper – färg, ' \
  'slipning och klarhet – för att identifiera de segment som har en stabil' \
  ' värdeutveckling och ett varierat utbud i olika prisklasser. Detta ger ' \
  'Guldfynd underlag för strategiska investeringsbeslut inom Wesselton-diamanter.'
)

st.image('./images/diamond_color_grade.png')

# 1. Piechart: Fördelning av färg

st.subheader("Fördelning av färger")
st.text(
  'Diamanter i färgintervallet D till G visar en optimal balans mellan exkluderad ' \
  'färgton och kostnadseffektivitet. Dessa stenar uppfyller kraven på att ge en ' \
  'nästan färglös framtoning, vilket är centralt för en premiumprodukt, men till ' \
  'ett pris som tillåter en bredare marknadspositionering.'
)
fig_color_pie, ax_color_pie = plt.subplots()

ax_color_pie.pie(
    distribution_by_color, 
    labels=distribution_by_color.index, 
    autopct='%1.1f%%', 
    startangle=90
)
ax_color_pie.set_title('Fördelning av färger')
st.pyplot(fig_color_pie)

# 2, Violinchart: Färg vs. pris
st.header('Pris vs. färg')
st.text(
  'Mängden av diamanter med färgen "G" kan förklaras för dess popularitet, ' \
  'bland annat för att de är nära färglösa på GIA-skalan. Generiellt brukar ' \
  'diamanter med på GIA-skalan från D till F vara dyrare eftersom att de är ' \
  'färglösa men med stapeldiagramet kan vi se att medelpriset per diamant är ' \
  'lägre än färgen G. Om priset är lägre än G, kan det innebära att Guldfynd ' \
  'kan erbjuda färglösa diamanter till ett mer konkurrenskraftigt pris. '
)
fig_violin, ax_violin = plt.subplots()
sns.violinplot(
    x='color', 
    y='price', 
    data=df, 
    ax=ax_violin
)
ax_violin.set_title('Färg vs. pris')
st.pyplot(fig_violin)

# 3. Piechart: Fördelning av slipningar
st.subheader("Fördelning av slipningar")
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(
    distribution_by_cuts.values, 
    labels=distribution_by_cuts.index, 
    autopct='%1.1f%%', 
    startangle=90
)
st.text(
  'Pie-charten visar att majoriteten av diamanterna i det filtrerade segmentet ' \
  'har Ideal- eller Premium-slipning. Detta speglar en betoning på hög ' \
  'ljusreflektion och stilren design, vilket stärker den visuella ' \
  'attraktionskraften hos guldfynds sortiment. Dessa slipningsgrader ' \
  'säkerställer även en enhetlig utformning med stark marknadsefterfrågan.'
)
ax_pie.set_title('Fördelning av slipningar')
st.pyplot(fig_pie)

# 4. Scatterplot: Pris vs. Carat
st.subheader("Pris vs. Carat")
fig_scatter, ax_scatter = plt.subplots()
sns.scatterplot(
    x='carat', 
    y='price', 
    hue='cut', 
    data=g_sorted_by_cuts, 
    ax=ax_scatter
)
ax_scatter.set_xlabel('Carat')
ax_scatter.set_ylabel('Pris')
ax_scatter.set_title('Pris vs. Carat')
st.text(
  'Pris och carat har ett tydligt samband: ju större diamanten är, desto dyrare ' \
  'blir den. Detta beror på att större diamanter är mer sällsynta och kräver ' \
  'att fler råmaterial bevaras vid slipning. Men priset ökar inte helt linjärt ' \
  '– en diamant som är dubbelt så stor kostar oftast mer än dubbelt så mycket ' \
  'eftersom efterfrågan på större stenar är hög och utbudet är begränsat. ' \
  'Andra faktorer som klarhet, färg och slipning påverkar också priset.'
)

# Lägg till regressionslinje
sns.regplot(
    x='carat',
    y='price',
    data=g_sorted_by_cuts,
    scatter=False,
    ax=ax_scatter,
    color='black',
    line_kws={'linestyle': 'dashed', 'linewidth': 2}
)

st.pyplot(fig_scatter)
st.text(
  'Analysen indikerar att de utvalda klarhetsgraderna uppvisar en stabil ' \
  'prisbild med en begränsad prisspridning. Trots mindre visuella inneslutningar' \
  ' kan dessa diamanter ge ett stabilt värdeuttag och uppfylla kundernas krav på' \
  ' kvalitet, vilket gör dem väl lämpade för både premium- och mellanklassmarknaden.'
)

# 5. Barplot: Pris vs. Klarhet
st.subheader("Pris vs. Klarhet")
fig_bar, ax_bar = plt.subplots()
sns.barplot(
    x='price',
    y='clarity',
    data=g_sorted_by_cuts,
    ax=ax_bar
)
ax_bar.set_xlabel('Pris')
ax_bar.set_ylabel('Klarhet')
ax_bar.set_title('Pris vs. Klarhet')
st.text(
  'Utifrån scatter- och barplot-graferna visar att det finns ett ' \
  'tydligt, positivt samband mellan carat och pris, samt att klarhetsgraderna ' \
  'ger en förutsägbar prissättning. Detta medför fördelen att Guldfynd kan ' \
  'erbjuda diamanter i olika storlekar och prisklasser utan att kompromissa ' \
  'med den visuella och kvalitativa standarden.'
)

st.pyplot(fig_bar)

st.text(
  'Utifrån analysen av diamantdata visar det att diamanter med färger mellan ' \
  'D och G, i kombination med slipningsgraderna Premium, Ideal och Very Good ' \
  'samt klarheter i segmenten VS1, VS2, VVS1, VVS2 och IF, utgör en attraktiv ' \
  'och stabil produktkategori för Guldfynd. Dessa diamanter – ofta benämnda ' \
  'som Wesselton-diamanter – erbjuder en mångsidighet i prisklasser och en ' \
  'balanserad kombination av visuell kvalitet, stabil värdeutveckling ' \
  'och ett varierat utbud.'
)
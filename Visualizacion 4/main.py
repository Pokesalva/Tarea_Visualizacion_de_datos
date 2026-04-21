"""
Visualización de Datos — Luis Suárez: Rendimiento por Club
Gráfico: Treemap jerárquico → Club → Temporada → Competición
Datos: Estadísticas reales de carrera (fuente: Transfermarkt)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# DATASET MANUAL — Goles por Club / Temporada / Competición
# Fuente: Transfermarkt (datos públicos verificables)
# Solo incluye los clubes principales de los 2010s
# ─────────────────────────────────────────────
data = [
    # AJAX (temporada parcial, vendido en enero 2011)
    {"Club": "Ajax",            "Season": "2010/11", "Competition": "Eredivisie",        "Goals": 7},
    {"Club": "Ajax",            "Season": "2010/11", "Competition": "UEFA Europa League","Goals": 4},

    # LIVERPOOL
    {"Club": "Liverpool",       "Season": "2010/11", "Competition": "Premier League",    "Goals": 4},
    {"Club": "Liverpool",       "Season": "2011/12", "Competition": "Premier League",    "Goals": 17},
    {"Club": "Liverpool",       "Season": "2011/12", "Competition": "FA Cup",            "Goals": 3},
    {"Club": "Liverpool",       "Season": "2012/13", "Competition": "Premier League",    "Goals": 23},
    {"Club": "Liverpool",       "Season": "2012/13", "Competition": "FA Cup",            "Goals": 2},
    {"Club": "Liverpool",       "Season": "2013/14", "Competition": "Premier League",    "Goals": 31},
    {"Club": "Liverpool",       "Season": "2013/14", "Competition": "UEFA Europa League","Goals": 2},
    {"Club": "Liverpool",       "Season": "2013/14", "Competition": "FA Cup",            "Goals": 1},

    # BARCELONA
    {"Club": "Barcelona",       "Season": "2014/15", "Competition": "LaLiga",            "Goals": 25},
    {"Club": "Barcelona",       "Season": "2014/15", "Competition": "Champions League",  "Goals": 7},
    {"Club": "Barcelona",       "Season": "2014/15", "Competition": "Copa del Rey",      "Goals": 3},
    {"Club": "Barcelona",       "Season": "2015/16", "Competition": "LaLiga",            "Goals": 40},
    {"Club": "Barcelona",       "Season": "2015/16", "Competition": "Champions League",  "Goals": 6},
    {"Club": "Barcelona",       "Season": "2015/16", "Competition": "Copa del Rey",      "Goals": 3},
    {"Club": "Barcelona",       "Season": "2015/16", "Competition": "Club World Cup",    "Goals": 5},
    {"Club": "Barcelona",       "Season": "2016/17", "Competition": "LaLiga",            "Goals": 29},
    {"Club": "Barcelona",       "Season": "2016/17", "Competition": "Champions League",  "Goals": 5},
    {"Club": "Barcelona",       "Season": "2016/17", "Competition": "Copa del Rey",      "Goals": 3},
    {"Club": "Barcelona",       "Season": "2017/18", "Competition": "LaLiga",            "Goals": 25},
    {"Club": "Barcelona",       "Season": "2017/18", "Competition": "Champions League",  "Goals": 4},
    {"Club": "Barcelona",       "Season": "2017/18", "Competition": "Copa del Rey",      "Goals": 3},
    {"Club": "Barcelona",       "Season": "2018/19", "Competition": "LaLiga",            "Goals": 21},
    {"Club": "Barcelona",       "Season": "2018/19", "Competition": "Champions League",  "Goals": 4},
    {"Club": "Barcelona",       "Season": "2018/19", "Competition": "Copa del Rey",      "Goals": 1},
    {"Club": "Barcelona",       "Season": "2019/20", "Competition": "LaLiga",            "Goals": 16},
    {"Club": "Barcelona",       "Season": "2019/20", "Competition": "Champions League",  "Goals": 2},
    {"Club": "Barcelona",       "Season": "2019/20", "Competition": "Copa del Rey",      "Goals": 3},

    # ATLÉTICO MADRID
    {"Club": "Atlético Madrid", "Season": "2020/21", "Competition": "LaLiga",            "Goals": 21},
    {"Club": "Atlético Madrid", "Season": "2020/21", "Competition": "Champions League",  "Goals": 3},
    {"Club": "Atlético Madrid", "Season": "2020/21", "Competition": "Copa del Rey",      "Goals": 1},
]

df = pd.DataFrame(data)

# Totales por club para ordenar
club_totals = df.groupby("Club")["Goals"].sum().to_dict()
df["Club_label"] = df["Club"].apply(lambda c: f"{c}  ({club_totals[c]} goles)")

# Colores por club
club_colors = {
    "Ajax":            "#D50000",
    "Liverpool":       "#C62828",
    "Barcelona":       "#1A237E",
    "Atlético Madrid": "#B71C1C",
}

# ─────────────────────────────────────────────
# TREEMAP — Club → Temporada → Competición
# ─────────────────────────────────────────────
print("📊 Generando Treemap: Rendimiento de Suárez por Club...")

# Agregar columna de color basada en club
df["color_club"] = df["Club"].map(club_colors)

fig = px.treemap(
    df,
    path=["Club", "Season", "Competition"],
    values="Goals",
    color="Club",
    color_discrete_map=club_colors,
    title="🟡 Luis Suárez — Rendimiento por Club, Temporada y Competición (2010s)",
    custom_data=["Goals"],
)

fig.update_traces(
    texttemplate="<b>%{label}</b><br>%{value} goles",
    textfont=dict(size=13, color="white"),
    hovertemplate="<b>%{label}</b><br>Goles: %{value}<br>%{percentRoot:.1%} del total<extra></extra>",
    marker=dict(
        line=dict(width=2, color="#0d1117"),
        cornerradius=6,
    ),
)

fig.update_layout(
    paper_bgcolor="#0d1117",
    font=dict(color="white", family="Arial"),
    title=dict(
        font=dict(size=17, color="white"),
        x=0.01,
    ),
    margin=dict(t=70, l=10, r=10, b=10),
    height=680,
)

output = os.path.join(OUTPUT_DIR, "suarez_treemap.html")
fig.write_html(output)
print(f"✅ Guardado: {output}")

# ─────────────────────────────────────────────
# ESTADÍSTICAS EN CONSOLA
# ─────────────────────────────────────────────
print("\n📈 Resumen de carrera:")
print(f"   Total goles: {df['Goals'].sum()}")
print("\n   Por club:")
for club, total in sorted(club_totals.items(), key=lambda x: -x[1]):
    print(f"   - {club}: {total} goles")

print("\n   Mejor temporada:")
best = df.groupby("Season")["Goals"].sum().idxmax()
best_total = df.groupby("Season")["Goals"].sum().max()
print(f"   - {best}: {best_total} goles")

fig.show()
print("\n✅ ¡Listo!")

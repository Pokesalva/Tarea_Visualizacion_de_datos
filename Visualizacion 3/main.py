import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
DATA_PATH = "data/data.csv"
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Títulos de Champions ganados con CR7
UCL_TITLES = ["2013/14", "2015/16", "2016/17", "2017/18"]

# Orden lógico de fases en Champions
FASES_ORDEN = [
    "Group Stage",
    "Round of 16",
    "Quarter-finals",
    "Semi-finals",
    "Final",
]

# Mapeo flexible por si los nombres en el CSV varían
FASES_MAP = {
    "group stage":    "Group Stage",
    "groups":         "Group Stage",
    "group":          "Group Stage",
    "round of 16":    "Round of 16",
    "last 16":        "Round of 16",
    "round of 32":    "Round of 32",
    "quarter-finals": "Quarter-finals",
    "quarter finals": "Quarter-finals",
    "quarterfinals":  "Quarter-finals",
    "semi-finals":    "Semi-finals",
    "semi finals":    "Semi-finals",
    "semifinals":     "Semi-finals",
    "final":          "Final",
}

print("Cargando dataset...")
df = pd.read_csv(DATA_PATH)
print("Columnas:", df.columns.tolist())

real_madrid = df[df["Club"].str.contains("Real Madrid", case=False, na=False)].copy()
print(f"Goles con el Real Madrid: {len(real_madrid)}")

temporadas_orden = sorted(real_madrid["Season"].dropna().unique())


print("\nGenerando Criterio 1: Heatmap Champions League por fase...")


ucl = real_madrid[
    real_madrid["Competition"].str.contains("Champions|UEFA CL|UCL", case=False, na=False)
].copy()

print(f"   Goles en UCL: {len(ucl)}")
print("   Matchdays únicos en UCL:", ucl["Matchday"].unique())

# Normalizar nombres de fases
ucl["Phase"] = ucl["Matchday"].str.strip().str.lower().map(FASES_MAP)
ucl = ucl[ucl["Phase"].notna()]

fases_presentes = [f for f in FASES_ORDEN if f in ucl["Phase"].unique()]

pivot = (
    ucl.groupby(["Phase", "Season"])
    .size()
    .reset_index(name="Goals")
    .pivot(index="Phase", columns="Season", values="Goals")
    .fillna(0)
    .reindex(index=fases_presentes, columns=temporadas_orden, fill_value=0)
)

text_matrix = pivot.map(lambda v: str(int(v)) if v > 0 else "")

ticktext = []
for t in temporadas_orden:
    if t in UCL_TITLES:
        ticktext.append(f"<b>{t}<br>UCL</b>")
    else:
        ticktext.append(t)

fig1 = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        text=text_matrix.values,
        texttemplate="%{text}",
        textfont=dict(size=14, color="white"),
        colorscale=[
            [0.0,  "#0d1117"],
            [0.01, "#0D47A1"],
            [0.4,  "#1565C0"],
            [0.7,  "#C62828"],
            [1.0,  "#FFD600"],
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="Goles", font=dict(color="white")),
            tickfont=dict(color="white"),
        ),
        hovertemplate="<b>Fase: %{y}</b><br>Temporada: %{x}<br>Goles: %{z}<extra></extra>",
    )
)

fig1.update_layout(
    title=dict(
        text="CR7 en Champions League — Goles por Fase y Temporada (Real Madrid)",
        font=dict(size=17, color="white"),
    ),
    plot_bgcolor="#0d1117",
    paper_bgcolor="#0d1117",
    font=dict(color="white"),
    xaxis=dict(
        tickvals=temporadas_orden,
        ticktext=ticktext,
        tickangle=-30,
        gridcolor="#2a2a2a",
        title=dict(text="Temporada", font=dict(color="white")),
    ),
    yaxis=dict(
        gridcolor="#2a2a2a",
        title=dict(text="Fase", font=dict(color="white")),
        autorange="reversed",
    ),
    margin=dict(l=160, r=40, t=90, b=120),
    height=420,
)

output1 = os.path.join(OUTPUT_DIR, "criterio1_ucl_heatmap.html")
fig1.write_html(output1)


print("\nGenerando Criterio 2: Sunburst...")

print("   Tipos de gol únicos:", real_madrid["Type"].unique() if "Type" in real_madrid.columns else real_madrid.get("Type_of_goal", real_madrid.get("Goal_type", pd.Series())).unique())

# Detectar nombre correcto de la columna de tipo de gol
type_col = None
for candidate in ["Type", "Type_of_goal", "Goal_type", "GoalType"]:
    if candidate in real_madrid.columns:
        type_col = candidate
        break

if type_col is None:
    print("No se encontró columna de tipo de gol. Usando 'Normal' como valor por defecto.")
    real_madrid["_type"] = "Normal"
    type_col = "_type"

sunburst_data = (
    real_madrid.groupby(["Season", "Competition", type_col])
    .size()
    .reset_index(name="Goals")
)

# Paleta de colores
color_seq = px.colors.qualitative.Vivid

fig2 = px.sunburst(
    sunburst_data,
    path=["Season", "Competition", type_col],
    values="Goals",
    color="Competition",
    color_discrete_sequence=color_seq,
    title="Jerarquía de Goles de CR7 — Temporada → Competición → Tipo de Gol (Real Madrid)",
)

fig2.update_traces(
    textfont=dict(size=12, color="white"),
    insidetextorientation="radial",
    hovertemplate="<b>%{label}</b><br>Goles: %{value}<br>%{percentRoot:.1%} del total<extra></extra>",
)

fig2.update_layout(
    paper_bgcolor="#0d1117",
    font=dict(color="white"),
    title=dict(
        font=dict(size=16, color="white"),
    ),
    margin=dict(t=80, l=10, r=10, b=10),
    height=650,
)

output2 = os.path.join(OUTPUT_DIR, "criterio2_sunburst.html")
fig2.write_html(output2)


fig1.show()
fig2.show()

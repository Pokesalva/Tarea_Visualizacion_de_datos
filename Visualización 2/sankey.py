import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("SP1(1).csv")

def classify_favorite(row):
    h = row["AvgH"]
    d = row["AvgD"]
    a = row["AvgA"]
    min_odd = min(h, d, a)
    if min_odd == h:
        return "Favorito Local"
    elif min_odd == a:
        return "Favorito Visitante"
    else:
        return "Cuotas Igualadas"

df["fav"] = df.apply(classify_favorite, axis=1)

def classify_dominance(row):
    diff = row["HS"] - row["AS"]
    if diff > 3:
        return "Domina Local"
    elif diff < -3:
        return "Domina Visitante"
    else:
        return "Equilibrado"

df["dom"] = df.apply(classify_dominance, axis=1)

def map_result(x):
    if x == "H":
        return "Victoria Local"
    elif x == "A":
        return "Derrota Local"
    else:
        return "Empate"

df["res"] = df["FTR"].apply(map_result)

flow1 = df.groupby(["fav", "dom"]).size().reset_index(name="value")
flow2 = df.groupby(["dom", "res"]).size().reset_index(name="value")

labels = [
    "Favorito Local", "Cuotas Igualadas", "Favorito Visitante",
    "Domina Local", "Equilibrado", "Domina Visitante",
    "Victoria Local", "Empate", "Derrota Local"
]

label_to_index = {label: i for i, label in enumerate(labels)}

node_colors = [
    "#1f77b4", 
    "#ff7f0e", 
    "#2ca02c", 
    "#d62728", 
    "#9467bd", 
    "#8c564b", 
    "#e377c2", 
    "#7f7f7f", 
    "#bcbd22"  
]

def hex_to_rgba(hex_color, alpha=0.4):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'

source = []
target = []
value = []
color = []

for _, row in flow1.iterrows():
    src_idx = label_to_index[row["fav"]]
    source.append(src_idx)
    target.append(label_to_index[row["dom"]])
    value.append(row["value"])
    color.append(hex_to_rgba(node_colors[src_idx], 0.4))

for _, row in flow2.iterrows():
    src_idx = label_to_index[row["dom"]]
    source.append(src_idx)
    target.append(label_to_index[row["res"]])
    value.append(row["value"])
    color.append(hex_to_rgba(node_colors[src_idx], 0.4))

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=color
    )
)])

fig.update_layout(
    title=dict(
        text="Flujo de PREDICCIÓN vs RESULTADO.<br><span style='font-size:14px; color:gray;'>Clasificación de partidos según favoritismo y dominio, y su relación con el resultado final.</span>",
        font=dict(size=24, color="black"),
        x=0.5,
        xanchor="center"
    ),
    font=dict(size=14)
)

fig.show()
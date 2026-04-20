import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("SP1(1).csv")

def classify_favorite(row):
    h = row["AvgH"]
    d = row["AvgD"]
    a = row["AvgA"]
    
    min_odd = min(h, d, a)
    
    if min_odd == h:
        return "HomeFav"
    elif min_odd == a:
        return "AwayFav"
    else:
        return "Even"

df["fav"] = df.apply(classify_favorite, axis=1)

def classify_dominance(row):
    diff = row["HS"] - row["AS"]
    
    if diff > 3:
        return "HomeDominant"
    elif diff < -3:
        return "AwayDominant"
    else:
        return "Balanced"

df["dom"] = df.apply(classify_dominance, axis=1)

def map_result(x):
    if x == "H":
        return "HomeWin"
    elif x == "A":
        return "AwayWin"
    else:
        return "Draw"

df["res"] = df["FTR"].apply(map_result)

flow1 = df.groupby(["fav", "dom"]).size().reset_index(name="value")

flow2 = df.groupby(["dom", "res"]).size().reset_index(name="value")

labels = list(pd.concat([
    flow1["fav"],
    flow1["dom"],
    flow2["res"]
]).unique())

label_to_index = {label: i for i, label in enumerate(labels)}

source = []
target = []
value = []

for _, row in flow1.iterrows():
    source.append(label_to_index[row["fav"]])
    target.append(label_to_index[row["dom"]])
    value.append(row["value"])

for _, row in flow2.iterrows():
    source.append(label_to_index[row["dom"]])
    target.append(label_to_index[row["res"]])
    value.append(row["value"])

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
)])

fig.update_layout(title_text="Odds → Dominio → Resultado", font_size=10)
fig.show()
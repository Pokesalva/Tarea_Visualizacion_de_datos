import pandas as pd
import plotly.express as px

df = pd.read_csv("SP1(1).csv")


result_map = {
    "H": 0,   # Home Win
    "D": 1,   # Draw
    "A": 2    # Away Win
}

df["FTR_num"] = df["FTR"].map(result_map)

features = [
    "HS", "AS",
    "HST", "AST",
    "HF", "AF",
    "HC", "AC",
    "HY", "AY"
]

df_clean = df.dropna(subset=features + ["FTR_num"])

fig = px.parallel_coordinates(
    df_clean,
    dimensions=features,
    color="FTR_num",
    color_continuous_scale=px.colors.diverging.Tealrose,
    labels={
        "HS": "Shots Home",
        "AS": "Shots Away",
        "HST": "Shots on Target Home",
        "AST": "Shots on Target Away",
        "HF": "Fouls Home",
        "AF": "Fouls Away",
        "HC": "Corners Home",
        "AC": "Corners Away",
        "HY": "Yellow Home",
        "AY": "Yellow Away"
    }
)

fig.update_layout(
    title="Parallel Coordinates: Estadísticas del partido vs Resultado",
    coloraxis_colorbar=dict(
        title="Resultado",
        tickvals=[0, 1, 2],
        ticktext=["Home Win", "Draw", "Away Win"]
    )
)

fig.show()
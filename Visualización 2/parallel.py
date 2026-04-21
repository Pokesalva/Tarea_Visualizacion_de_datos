import pandas as pd
import plotly.express as px

df = pd.read_csv("SP1(1).csv")

result_map = {
    "H": 0,   
    "D": 1,   
    "A": 2    
}
df["FTR_num"] = df["FTR"].map(result_map)

def clasificar_horario_tres(t):
    try:
        # Extraer solo la hora
        hora = int(str(t).split(":")[0])
        
        if hora < 14:
            return 0 # Mañana / Mediodía (Antes de las 14:00)
        elif 14 <= hora < 18:
            return 1 # Tarde (14:00 a 17:59)
        else:
            return 2 # Noche (18:00 en adelante)
    except:
        return None 

df["Horario_num"] = df["Time"].apply(clasificar_horario_tres)

features = [
    "Horario_num",  
    "HS", "AS",
    "HST", "AST",
    "HF", "AF",
    "HC", "AC",
    "HY", "AY"
]

df_clean = df.dropna(subset=features + ["FTR_num"])

df_sample = df_clean.sample(frac=0.3, random_state=42)

fig = px.parallel_coordinates(
    data_frame=df_sample, 
    dimensions=features,
    color="FTR_num",
    color_continuous_scale=px.colors.diverging.Portland, 
    labels={
        "Horario_num": "Horario (0=Mañana, 1=Tarde, 2=Noche)", 
        "HS": "Tiros Local",
        "AS": "Tiros Visita",
        "HST": "Tiros Arco Local",
        "AST": "Tiros Arco Visita",
        "HF": "Faltas Local",
        "AF": "Faltas Visita",
        "HC": "Córners Local",
        "AC": "Córners Visita",
        "HY": "Amarillas Local",
        "AY": "Amarillas Visita"
    }
)

fig.update_layout(
    title=dict(
        text="Coordenadas Paralelas: Impacto de las Estadísticas en el Partido<br><span style='font-size:14px; color:gray;'>Análisis multifactorial de métricas de juego (Muestra del 30%).</span>",
        font=dict(size=22, color="black"),
        x=0.5,
        xanchor="center"
    ),
    margin=dict(t=160, b=50, l=50, r=50), 
    coloraxis_colorbar=dict(
        title="Resultado",
        tickvals=[0, 1, 2],
        ticktext=["Victoria Local", "Empate", "Derrota Local"],
        len=0.75
    )
)

fig.show()

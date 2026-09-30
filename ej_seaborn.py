"""
Ejemplo 3 · seaborn: dos gráficos a partir de una tabla de ventas.
 
Genera las mismas ventas que ejemplo_pandas.py, dibuja dos gráficos, los guarda
como imágenes en la carpeta graficos/ y los muestra en una ventana.
Cierra la ventana para que el programa termine.
"""
from pathlib import Path
 
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
 
# ---- Crear los datos (igual que en ejemplo_pandas.py) ----
generador = np.random.default_rng(2026)
n = 240
ventas = pd.DataFrame({
    "fecha": pd.to_datetime("2026-01-01") + pd.to_timedelta(generador.integers(0, 181, n), unit="D"),
    "tienda": generador.choice(["Madrid", "Barcelona", "Valencia", "Sevilla"], n, p=[0.32, 0.28, 0.21, 0.19]),
    "categoria": generador.choice(["Electrónica", "Hogar", "Moda", "Deportes"], n),
    "unidades": generador.integers(1, 7, n),
})
precio_base = ventas["categoria"].map({"Electrónica": 250, "Hogar": 60, "Moda": 50, "Deportes": 90})
ventas["precio_unitario"] = (precio_base * generador.uniform(0.5, 1.5, n)).round(2)
ventas["importe"] = ventas["unidades"] * ventas["precio_unitario"]
ventas["mes"] = ventas["fecha"].dt.month
 
# La carpeta de salida se crea junto a este archivo, en Windows y en Mac
SALIDA = Path(__file__).parent / "graficos"
SALIDA.mkdir(exist_ok=True)
 
sns.set_theme(style="whitegrid")
orden_tiendas = ["Madrid", "Barcelona", "Valencia", "Sevilla"]
 
# Gráfico 1: facturación por tienda, separada por categoría
fig1, ax1 = plt.subplots(figsize=(9, 5))
sns.barplot(data=ventas, x="tienda", y="importe", hue="categoria", order=orden_tiendas,
            estimator="sum", errorbar=None, ax=ax1)
ax1.set_title("Facturación por tienda y categoría (enero-junio 2026)")
ax1.set_xlabel("")
ax1.set_ylabel("Importe (EUR)")
fig1.tight_layout()
fig1.savefig(SALIDA / "facturacion_por_tienda.png", dpi=120)
 
# Gráfico 2: evolución mensual de cada tienda
mensual = ventas.groupby(["mes", "tienda"], as_index=False)["importe"].sum()
fig2, ax2 = plt.subplots(figsize=(9, 5))
sns.lineplot(data=mensual, x="mes", y="importe", hue="tienda", hue_order=orden_tiendas,
             marker="o", ax=ax2)
ax2.set_title("Facturación mensual por tienda")
ax2.set_xlabel("Mes")
ax2.set_ylabel("Importe (EUR)")
ax2.set_xticks(range(1, 7))
fig2.tight_layout()
fig2.savefig(SALIDA / "evolucion_mensual.png", dpi=120)
 
print("Gráficos guardados en la carpeta 'graficos':")
for imagen in sorted(SALIDA.glob("*.png")):
    print("  ", imagen.name)

plt.close("all")
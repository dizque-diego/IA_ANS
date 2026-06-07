# =============================================================
# SISTEMA DE AGRUPAMIENTO - METRO DE MEDELLIN
# Modelo: K-Means Clustering (Aprendizaje No Supervisado)
# Materia: Inteligencia Artificial
# =============================================================
#
# A diferencia del aprendizaje supervisado, aqui el modelo NO
# conoce las respuestas de antemano. En su lugar, analiza los
# datos y descubre por si mismo grupos con comportamiento similar.
#
# Pasos del proceso:
#   1. Cargar el dataset
#   2. Explorar los datos
#   3. Seleccionar y escalar las variables numericas
#   4. Determinar el numero optimo de clusters (Metodo del Codo)
#   5. Entrenar el modelo K-Means
#   6. Analizar los clusters encontrados
#   7. Visualizaciones de los resultados
#   8. Interpretar los grupos descubiertos

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

import warnings
warnings.filterwarnings('ignore')


# ─────────────────────────────────────────────
# PASO 1: CARGAR EL DATASET
# ─────────────────────────────────────────────

print("=" * 62)
print("  SISTEMA DE AGRUPAMIENTO — METRO DE MEDELLIN")
print("  Aprendizaje No Supervisado: K-Means Clustering")
print("=" * 62)

print("\n[1] Cargando dataset...")

df = pd.read_csv("../data/raw/datos_metro.csv")
print(f"    Dataset cargado: {df.shape[0]} registros, {df.shape[1]} columnas")


# ─────────────────────────────────────────────
# PASO 2: EXPLORAR LOS DATOS
# ─────────────────────────────────────────────

print("\n[2] Explorando los datos...")

print("\n    Primeras 5 filas:")
print(df[['linea','estacion','hora','tipo_dia',
          'pasajeros_estimados','ocupacion_porcentaje']].head().to_string(index=False))

print("\n    Distribucion por tipo de dia:")
for tipo, cant in df['tipo_dia'].value_counts().items():
    print(f"      {tipo:<10}: {cant} registros")

print("\n    Distribucion por linea:")
for linea, cant in df['linea'].value_counts().items():
    print(f"      Linea {linea:<4}: {cant} registros")

print("\n    Estadisticas de variables numericas clave:")
cols = ['pasajeros_estimados','tiempo_espera_min',
        'frecuencia_trenes_min','ocupacion_porcentaje']
print(df[cols].describe().round(1).to_string())


# ─────────────────────────────────────────────
# PASO 3: SELECCIONAR Y ESCALAR VARIABLES
# ─────────────────────────────────────────────
#
# K-Means usa distancias entre puntos para agruparlos.
# Si una variable tiene valores grandes (ej: pasajeros: 800)
# y otra tiene valores pequeños (ej: tiempo_espera: 5),
# la primera dominaria el calculo. Por eso escalamos los datos:
# todos quedan con media 0 y desviacion estandar 1.

print("\n[3] Seleccionando y escalando variables...")

variables_modelo = [
    'hora',
    'pasajeros_estimados',
    'tiempo_espera_min',
    'frecuencia_trenes_min',
    'ocupacion_porcentaje'
]

X = df[variables_modelo].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"    Variables seleccionadas: {variables_modelo}")
print(f"    Escalado aplicado: StandardScaler (media=0, std=1)")
print(f"    Forma de los datos escalados: {X_scaled.shape}")


# ─────────────────────────────────────────────
# PASO 4: DETERMINAR NUMERO OPTIMO DE CLUSTERS
# ─────────────────────────────────────────────
#
# No sabemos cuantos grupos existen en los datos.
# Usamos dos metodos para determinarlo:
#
# METODO DEL CODO: grafica la inercia (suma de distancias
# al centroide) para cada k. El "codo" de la curva indica
# el k optimo — despues de ese punto, agregar mas clusters
# no mejora significativamente el modelo.
#
# COEFICIENTE DE SILUETA: mide que tan bien separados estan
# los clusters. Valores cercanos a 1 = muy bien separados.

print("\n[4] Determinando numero optimo de clusters...")

inercias    = []
siluetas    = []
rango_k     = range(2, 8)

for k in rango_k:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inercias.append(km.inertia_)
    sil = silhouette_score(X_scaled, km.labels_)
    siluetas.append(sil)
    print(f"    k={k}: Inercia={km.inertia_:.1f} | Silueta={sil:.3f}")

k_optimo = rango_k.start + siluetas.index(max(siluetas))
print(f"\n    Numero optimo de clusters: k={k_optimo}")
print(f"    Coeficiente de silueta optimo: {max(siluetas):.3f}")


# ─────────────────────────────────────────────
# PASO 5: ENTRENAR EL MODELO K-MEANS
# ─────────────────────────────────────────────
#
# K-Means funciona asi:
# 1. Coloca k centroides aleatoriamente
# 2. Asigna cada punto al centroide mas cercano
# 3. Mueve los centroides al centro de su grupo
# 4. Repite hasta que los grupos no cambien

print(f"\n[5] Entrenando modelo K-Means con k={k_optimo}...")

modelo_kmeans = KMeans(
    n_clusters=k_optimo,
    random_state=42,
    n_init=10,
    max_iter=300
)

modelo_kmeans.fit(X_scaled)
df['cluster'] = modelo_kmeans.labels_

print(f"    Modelo entrenado correctamente.")
print(f"    Inercia final: {modelo_kmeans.inertia_:.2f}")
print(f"    Iteraciones realizadas: {modelo_kmeans.n_iter_}")

print("\n    Distribucion de registros por cluster:")
for c, cant in df['cluster'].value_counts().sort_index().items():
    pct = (cant / len(df)) * 100
    print(f"      Cluster {c}: {cant} registros ({pct:.1f}%)")


# ─────────────────────────────────────────────
# PASO 6: ANALIZAR LOS CLUSTERS
# ─────────────────────────────────────────────

print("\n[6] Analizando caracteristicas de cada cluster...")

medias = df.groupby('cluster')[variables_modelo].mean().round(1)

etiquetas_cluster = {}
for c in range(k_optimo):
    pax  = medias.loc[c, 'pasajeros_estimados']
    ocup = medias.loc[c, 'ocupacion_porcentaje']
    hora = medias.loc[c, 'hora']
    if ocup >= 80:
        etiqueta = "ALTA CONGESTION"
    elif ocup >= 60:
        etiqueta = "CONGESTION MEDIA"
    else:
        etiqueta = "BAJA CONGESTION"
    etiquetas_cluster[c] = etiqueta

print(f"\n    {'Cluster':<10} {'Pasajeros':<12} {'Espera(min)':<14} "
      f"{'Freq(min)':<12} {'Ocupacion%':<12} {'Hora prom':<12} {'Perfil'}")
print("    " + "-" * 80)

for c in range(k_optimo):
    row = medias.loc[c]
    print(f"    {c:<10} {row['pasajeros_estimados']:<12.0f} "
          f"{row['tiempo_espera_min']:<14.1f} "
          f"{row['frecuencia_trenes_min']:<12.1f} "
          f"{row['ocupacion_porcentaje']:<12.1f} "
          f"{row['hora']:<12.1f} "
          f"{etiquetas_cluster[c]}")

print("\n    Composicion de cada cluster por tipo de dia:")
composicion = df.groupby(['cluster', 'tipo_dia']).size().unstack(fill_value=0)
print(composicion.to_string())

print("\n    Composicion de cada cluster por linea:")
por_linea = df.groupby(['cluster', 'linea']).size().unstack(fill_value=0)
print(por_linea.to_string())


# ─────────────────────────────────────────────
# PASO 7: VISUALIZACIONES
# ─────────────────────────────────────────────

print("\n[7] Generando visualizaciones...")

colores = ['#1565C0', '#2E7D32', '#E65100', '#6A1B9A', '#B71C1C', '#00838F']
colores_cluster = [colores[i] for i in range(k_optimo)]

# --- Figura 1: Metodo del Codo + Silueta ---
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.plot(list(rango_k), inercias, 'bo-', linewidth=2, markersize=7)
ax1.axvline(x=k_optimo, color='red', linestyle='--', alpha=0.7,
            label=f'k optimo = {k_optimo}')
ax1.set_xlabel('Numero de Clusters (k)', fontsize=11)
ax1.set_ylabel('Inercia', fontsize=11)
ax1.set_title('Metodo del Codo\nDeterminacion del k optimo', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

ax2.plot(list(rango_k), siluetas, 'go-', linewidth=2, markersize=7)
ax2.axvline(x=k_optimo, color='red', linestyle='--', alpha=0.7,
            label=f'k optimo = {k_optimo}')
ax2.set_xlabel('Numero de Clusters (k)', fontsize=11)
ax2.set_ylabel('Coeficiente de Silueta', fontsize=11)
ax2.set_title('Coeficiente de Silueta\nCalidad de los clusters', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.suptitle('Determinacion del Numero Optimo de Clusters\nMetro de Medellin',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('../docs/metodo_codo_silueta.png', dpi=150, bbox_inches='tight')
plt.close()
print("    Guardado: docs/metodo_codo_silueta.png")

# --- Figura 2: Clusters en 2D con PCA ---
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
var_exp = pca.explained_variance_ratio_

fig2, ax = plt.subplots(figsize=(9, 6))
for c in range(k_optimo):
    mask = df['cluster'] == c
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
               c=colores_cluster[c], label=f'Cluster {c}: {etiquetas_cluster[c]}',
               s=90, alpha=0.85, edgecolors='white', linewidth=0.5)

centroides_pca = pca.transform(modelo_kmeans.cluster_centers_)
ax.scatter(centroides_pca[:, 0], centroides_pca[:, 1],
           c='black', marker='X', s=200, zorder=5, label='Centroides')

ax.set_xlabel(f'Componente Principal 1 ({var_exp[0]*100:.1f}% varianza)', fontsize=11)
ax.set_ylabel(f'Componente Principal 2 ({var_exp[1]*100:.1f}% varianza)', fontsize=11)
ax.set_title('Clusters Visualizados en 2D (PCA)\nMetro de Medellin — K-Means',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=9, loc='best')
ax.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('../docs/clusters_pca.png', dpi=150, bbox_inches='tight')
plt.close()
print("    Guardado: docs/clusters_pca.png")

# --- Figura 3: Perfil de cada cluster (radar / barras) ---
fig3, axes = plt.subplots(1, k_optimo, figsize=(5 * k_optimo, 5), sharey=False)
if k_optimo == 1:
    axes = [axes]

vars_graf = ['pasajeros_estimados', 'tiempo_espera_min',
             'frecuencia_trenes_min', 'ocupacion_porcentaje']
labels_graf = ['Pasajeros', 'Espera (min)', 'Frecuencia (min)', 'Ocupacion (%)']

for c, ax in enumerate(axes):
    valores = [medias.loc[c, v] for v in vars_graf]
    barras = ax.bar(labels_graf, valores, color=colores_cluster[c], alpha=0.85,
                    edgecolor='white')
    ax.set_title(f'Cluster {c}\n{etiquetas_cluster[c]}',
                 fontsize=11, fontweight='bold', color=colores_cluster[c])
    ax.set_ylim(0, max(df['pasajeros_estimados'].max(), 100) * 1.15)
    for bar, val in zip(barras, valores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
                f'{val:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.tick_params(axis='x', rotation=15)
    ax.grid(True, alpha=0.2, axis='y')

plt.suptitle('Perfil Promedio de cada Cluster\nMetro de Medellin',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../docs/perfil_clusters.png', dpi=150, bbox_inches='tight')
plt.close()
print("    Guardado: docs/perfil_clusters.png")

# --- Figura 4: Dispersion Pasajeros vs Ocupacion coloreado por cluster ---
fig4, ax4 = plt.subplots(figsize=(9, 6))
for c in range(k_optimo):
    mask = df['cluster'] == c
    ax4.scatter(
        df.loc[mask, 'pasajeros_estimados'],
        df.loc[mask, 'ocupacion_porcentaje'],
        c=colores_cluster[c], s=100, alpha=0.85,
        label=f'Cluster {c}: {etiquetas_cluster[c]}',
        edgecolors='white', linewidth=0.5
    )

ax4.set_xlabel('Pasajeros Estimados', fontsize=11)
ax4.set_ylabel('Ocupacion (%)', fontsize=11)
ax4.set_title('Pasajeros vs Ocupacion por Cluster\nMetro de Medellin',
              fontsize=12, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('../docs/pasajeros_vs_ocupacion.png', dpi=150, bbox_inches='tight')
plt.close()
print("    Guardado: docs/pasajeros_vs_ocupacion.png")


# ─────────────────────────────────────────────
# PASO 8: INTERPRETAR RESULTADOS
# ─────────────────────────────────────────────

print("\n[8] Interpretacion de los grupos descubiertos...")
print("\n" + "=" * 62)

for c in range(k_optimo):
    datos_c  = df[df['cluster'] == c]
    row      = medias.loc[c]
    tipos    = datos_c['tipo_dia'].value_counts().to_dict()
    lineas   = datos_c['linea'].value_counts().to_dict()

    print(f"\n  CLUSTER {c} — {etiquetas_cluster[c]}")
    print(f"  {'-' * 55}")
    print(f"  Registros:         {len(datos_c)} ({len(datos_c)/len(df)*100:.1f}% del total)")
    print(f"  Pasajeros prom:    {row['pasajeros_estimados']:.0f}")
    print(f"  Ocupacion prom:    {row['ocupacion_porcentaje']:.1f}%")
    print(f"  Espera prom:       {row['tiempo_espera_min']:.1f} min")
    print(f"  Frecuencia prom:   {row['frecuencia_trenes_min']:.1f} min")
    print(f"  Hora promedio:     {row['hora']:.1f}h")
    print(f"  Tipos de dia:      {tipos}")
    print(f"  Lineas:            {lineas}")

print("\n" + "=" * 62)
print("  PROCESO COMPLETADO EXITOSAMENTE")
print(f"  Clusters encontrados: {k_optimo}")
print(f"  Coeficiente de silueta: {max(siluetas):.3f}")
print("  Archivos generados en docs/:")
print("    - metodo_codo_silueta.png")
print("    - clusters_pca.png")
print("    - perfil_clusters.png")
print("    - pasajeros_vs_ocupacion.png")
print("=" * 62)

# Pruebas del Modelo — K-Means Clustering
## Sistema de Agrupamiento | Metro de Medellín

---

## 1. Descripción General de las Pruebas

Las pruebas realizadas validan el funcionamiento del modelo de aprendizaje no supervisado basado en **K-Means Clustering**, aplicado a los datos operativos simulados del Metro de Medellín.

A diferencia del aprendizaje supervisado, aquí el modelo no recibe etiquetas ni respuestas correctas. Su objetivo es descubrir por sí mismo grupos de registros con comportamiento similar, basándose únicamente en las variables numéricas del dataset.

---

## 2. Prueba 1 — Determinación del Número Óptimo de Clusters

Para determinar cuántos grupos existen en los datos se aplicaron dos métodos:

### Método del Codo

Se entrenaron modelos con k entre 2 y 7 y se registró la inercia (suma de distancias de cada punto a su centroide):

| k | Inercia | Coeficiente de Silueta |
|---|---|---|
| 2 | 83.2 | **0.461** ← Óptimo |
| 3 | 60.5 | 0.349 |
| 4 | 40.0 | 0.406 |
| 5 | 30.9 | 0.404 |
| 6 | 25.3 | 0.385 |
| 7 | 19.5 | 0.403 |

### Coeficiente de Silueta

Mide qué tan bien separados están los clusters. El valor más alto fue **0.461** para k=2, lo que indica que 2 clusters es la agrupación más natural para estos datos.

**Resultado:** El número óptimo de clusters es **k = 2**.

---

## 3. Prueba 2 — Entrenamiento del Modelo

| Parámetro | Valor |
|---|---|
| Algoritmo | K-Means |
| Número de clusters (k) | 2 |
| Criterio | Distancia euclidiana |
| Inercia final | 83.17 |
| Iteraciones realizadas | 3 |
| Coeficiente de silueta | 0.461 |

El modelo convergió en solo **3 iteraciones**, lo que indica que los grupos son bien diferenciados desde el inicio.

---

## 4. Prueba 3 — Análisis de los Clusters Descubiertos

### Distribución de registros

| Cluster | Registros | Porcentaje | Perfil descubierto |
|---|---|---|---|
| Cluster 0 | 22 | 55.0% | CONGESTIÓN MEDIA |
| Cluster 1 | 18 | 45.0% | BAJA CONGESTIÓN |

### Características promedio por cluster

| Variable | Cluster 0 | Cluster 1 |
|---|---|---|
| Pasajeros estimados | 686 | 369 |
| Ocupación (%) | 76.1% | 45.7% |
| Tiempo de espera (min) | 5.7 | 9.1 |
| Frecuencia trenes (min) | 4.5 | 8.1 |
| Hora promedio | 12.0h | 13.8h |

---

## 5. Prueba 4 — Composición por Tipo de Día

| Tipo de día | Cluster 0 | Cluster 1 |
|---|---|---|
| Laboral | 19 | 1 |
| Sábado | 3 | 7 |
| Domingo | 0 | 10 |

**Hallazgo clave:** El modelo descubrió por sí solo que los días laborales corresponden casi en su totalidad al cluster de mayor congestión, mientras que los domingos pertenecen completamente al cluster de baja congestión. Esto es completamente coherente con la realidad del transporte masivo urbano.

---

## 6. Prueba 5 — Composición por Línea

| Línea | Cluster 0 | Cluster 1 |
|---|---|---|
| Línea A | 10 | 9 |
| Línea B | 7 | 5 |
| Línea K | 5 | 4 |

Las tres líneas del sistema están presentes en ambos clusters de forma proporcional, lo que indica que el nivel de congestión no depende de la línea sino del contexto (hora, día, pasajeros).

---

## 7. Interpretación de los Grupos Descubiertos

### Cluster 0 — Congestión Media (55% de los registros)

Este grupo agrupa los registros con mayor afluencia de pasajeros. Sus características principales son:
- Promedio de **686 pasajeros** con **76% de ocupación**
- Tiempo de espera reducido: **5.7 minutos**
- Trenes frecuentes: cada **4.5 minutos**
- Compuesto casi exclusivamente por días **laborales**
- Representa las horas de mayor demanda del sistema

### Cluster 1 — Baja Congestión (45% de los registros)

Este grupo agrupa los registros con menor actividad del sistema:
- Promedio de **369 pasajeros** con solo **45.7% de ocupación**
- Tiempo de espera mayor: **9.1 minutos**
- Menor frecuencia de trenes: cada **8.1 minutos**
- Compuesto principalmente por **domingos y sábados**
- Representa los momentos de menor demanda del sistema

---

## 8. Archivos Generados

Al ejecutar el código (`src/clustering_transporte.py`) se generan automáticamente los siguientes archivos en la carpeta `docs/`:

| Archivo | Descripción |
|---|---|
| `metodo_codo_silueta.png` | Gráficas del Método del Codo y Coeficiente de Silueta para elegir k |
| `clusters_pca.png` | Visualización de los clusters en 2D usando PCA |
| `perfil_clusters.png` | Gráfico de barras con el perfil promedio de cada cluster |
| `pasajeros_vs_ocupacion.png` | Dispersión de pasajeros vs ocupación coloreada por cluster |

---

## 9. Conclusiones

1. El modelo K-Means identificó **2 grupos naturales** en los datos del Metro de Medellín con un coeficiente de silueta de **0.461**, lo que indica una separación moderada-buena entre los clusters.

2. El algoritmo descubrió de forma autónoma que el principal factor diferenciador entre los grupos es el **tipo de día** (laboral vs. fin de semana), sin que nadie le indicara esta información.

3. El **Cluster 0** (Congestión Media) agrupa días laborales con alta demanda, mientras que el **Cluster 1** (Baja Congestión) agrupa principalmente fines de semana con menor afluencia.

4. El preprocesamiento con **StandardScaler** fue fundamental para evitar que variables con rangos distintos (pasajeros vs. minutos) distorsionaran el cálculo de distancias del algoritmo.

5. Este modelo podría ser utilizado en una aplicación real para **anticipar el comportamiento del sistema** según el día y la hora, permitiendo planificar mejor la frecuencia de trenes y los recursos operativos.

---

*Documento generado como parte de la Actividad 4 — Métodos de Aprendizaje No Supervisado*
*Materia: Inteligencia Artificial | Universidad Iberoamericana de Colombia*

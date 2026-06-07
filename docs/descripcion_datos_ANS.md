# Descripción de los Datos
## Sistema de Agrupamiento — Metro de Medellín

---

## 1. Fuente de Datos

El dataset utilizado fue construido con fines académicos como representación simulada del funcionamiento del Metro de Medellín. No corresponde a datos oficiales ni históricos de la operación real del sistema.

El archivo se encuentra en: `data/raw/datos_metro.csv`

---

## 2. Estructura del Dataset

| Característica | Valor |
|---|---|
| Archivo | `datos_metro.csv` |
| Total de registros | 40 |
| Total de columnas | 10 |
| Tipo de aprendizaje | No supervisado — sin variable objetivo |

---

## 3. Descripción de Variables

| Variable | Tipo | Descripción |
|---|---|---|
| `id_registro` | Numérica | Identificador único de cada registro |
| `linea` | Categórica | Línea del metro: A, B o K (MetroCable) |
| `estacion` | Categórica | Nombre de la estación registrada |
| `hora` | Numérica | Hora del día en que se tomó el registro (6 a 21) |
| `dia_semana` | Categórica | Día de la semana del registro |
| `tipo_dia` | Categórica | Clasificación del día: Laboral, Sábado o Domingo |
| `pasajeros_estimados` | Numérica | Cantidad estimada de pasajeros en el registro |
| `tiempo_espera_min` | Numérica | Tiempo de espera estimado en minutos |
| `frecuencia_trenes_min` | Numérica | Frecuencia aproximada de paso de trenes en minutos |
| `ocupacion_porcentaje` | Numérica | Porcentaje estimado de ocupación del sistema |

---

## 4. Variables Utilizadas en el Modelo

Para el modelo de clustering se utilizaron exclusivamente las variables numéricas, ya que K-Means trabaja con distancias entre puntos:

| Variable | Rango | Media | Desv. Estándar |
|---|---|---|---|
| `hora` | 6 — 21 | 12.8 | 4.4 |
| `pasajeros_estimados` | 230 — 940 | 543.8 | 194.6 |
| `tiempo_espera_min` | 4 — 11 | 7.2 | 2.0 |
| `frecuencia_trenes_min` | 3 — 10 | 6.1 | 2.1 |
| `ocupacion_porcentaje` | 31 — 93 | 62.4 | 17.9 |

---

## 5. Distribución de los Datos

### Por tipo de día

| Tipo de día | Registros | Porcentaje |
|---|---|---|
| Laboral | 20 | 50% |
| Sábado | 10 | 25% |
| Domingo | 10 | 25% |

### Por línea del sistema

| Línea | Registros | Porcentaje |
|---|---|---|
| Línea A | 19 | 47.5% |
| Línea B | 12 | 30.0% |
| Línea K | 9 | 22.5% |

---

## 6. Diferencia con el Aprendizaje Supervisado

A diferencia de la actividad anterior, este dataset **no tiene una variable objetivo** (como `nivel_congestion`). El modelo de aprendizaje no supervisado debe descubrir por sí mismo los grupos que existen en los datos, sin que nadie le indique de antemano cuántos grupos hay ni cómo deben clasificarse los registros.

---

## 7. Preprocesamiento Aplicado

Antes de entrenar el modelo se aplicó **StandardScaler** a todas las variables numéricas. Este proceso transforma cada variable para que tenga media igual a 0 y desviación estándar igual a 1. Esto es necesario porque K-Means usa distancias euclidianas: sin escalar, variables con valores grandes (como `pasajeros_estimados`) dominarían el cálculo sobre variables con valores pequeños (como `tiempo_espera_min`).

---

## 8. Limitaciones del Dataset

- El dataset es simulado y no refleja datos reales de operación del Metro de Medellín.
- Con solo 40 registros, el tamaño es reducido para un modelo de clustering robusto.
- Un dataset más grande y con datos reales permitiría descubrir patrones más complejos y representativos del sistema.

---

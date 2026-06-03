# Aprendizaje no supervisado aplicado al Metro de Medellín

El proyecto toma como referencia el funcionamiento del sistema de transporte masivo urbano Metro de Medellín, con el fin de analizar posibles patrones de comportamiento en estaciones, líneas y franjas horarias.

## Objetivo del proyecto

Aplicar técnicas de aprendizaje no supervisado para identificar agrupamientos o patrones dentro de los datos relacionados con la operación del sistema Metro.

## Técnica propuesta

Se propone el agrupamiento mediante clustering, puesto que permite encontrar datos con características similares sin necesidad de contar con una variable objetivo previamente seleccionada.

## Fuente de datos

El proyecto utiliza un dataset simulado. Este archivo contiene una muestra de datos con fines académicos. Aparte de datos como estaciones y líneas, los datos no corresponden a información oficial ni a datos históricos de la operación del Metro de Medellín. Esta información es una representación simulada para facilitar el ejercicio de desarrollo de un modelo de aprendizaje no supervisado.

## CSV

El archivo `datos_metro.csv` contiene registros asociados a estaciones, líneas, horarios y variables operativas que pueden relacionarse con el sistema Metro.

El archivo contiene las siguientes variables:

- id_registro: identificador único de cada registro.
- linea
- estacion
- hora
- dia_semana
- tipo_dia
- pasajeros_estimados
- tiempo_espera_min: tiempo de espera estimado en minutos.
- frecuencia_trenes_min: frecuencia aproximada de trenes en minutos.
- ocupacion_porcentaje: porcentaje estimado de ocupación del sistema.

## Variables útiles

Para el modelo de aprendizaje, las siguientes variables numéricas son de alto grado de importancia:

- hora
- pasajeros_estimados
- tiempo_espera_min
- frecuencia_trenes_min
- ocupacion_porcentaje

Estas variables facilitarán analizar semejanzas entre registros y agruparlos por comportamiento similar.

## Resultados esperados

Utilizando el modelo de clustering se espera encontrar grupos como:

- Registros con baja ocupación.
- Registros con ocupación intermedia.
- Registros con alta congestión.
- Franjas horarias con comportamientos similares.
- Estaciones o líneas con patrones determinados.
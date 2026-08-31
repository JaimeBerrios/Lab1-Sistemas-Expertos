# FitExpert 2.0.0 | Parcial 1 v 2.0.0 · Sistemas Expertos

![Versión](https://img.shields.io/badge/versión-v2.0.0-1f7a4d)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab)
![Flask](https://img.shields.io/badge/Flask-3.x-20232a)
![Pruebas](https://img.shields.io/badge/pruebas-13%20aprobadas-198754)

FitExpert es un sistema basado en conocimiento que recomienda recetas a partir
de los ingredientes disponibles, el objetivo nutricional y el tipo de comida.
La versión 2.0.0 incorpora una base normalizada, coincidencia parcial con umbral
estricto, scoring nutricional diferenciado, explicación de las conclusiones y
validación robusta de la API.

> **Estado para la evaluación:** los cinco requerimientos del Primer Parcial
> están implementados, documentados y cubiertos por pruebas automatizadas.

## Ficha del Proyecto

| Campo | Valor |
| --- | --- |
| Evaluación | Parcial 1 v 2.0.0 · Sistemas Expertos |
| Sistema | FitExpert |
| Versión | v2.0.0 |
| Área de conocimiento | Nutrición y recomendación de recetas |
| Paradigma | Sistema basado en conocimiento con reglas de producción |
| Estrategia | Evaluación hacia adelante con coincidencia parcial |
| Backend | Python y Flask |
| Frontend | HTML, CSS y JavaScript |
| Base de conocimiento | `info.json` |
| Endpoint principal | `POST /api/recommend` |

## Cumplimiento de Requerimientos del Parcial

| Requerimiento de la cátedra | Implementación en FitExpert 2.0.0 | Evidencia |
| --- | --- | --- |
| Normalizar y extender la base | Fuente única con 27 ingredientes, 32 recetas y 32 reglas | `info.json` |
| Agregar una segunda categoría | `tipo_comida`: desayuno, almuerzo, cena, snack o todos | `info.json`, `lab1.py`, interfaz |
| Calcular confianza y filtrar | Cobertura porcentual de ingredientes; solo se conserva $P > 50\%$ | `calcular_coincidencia()`, `motor_inferencia()` |
| Ordenar y desempatar | Confianza descendente, scoring descendente y nombre ascendente | `recomendar_recetas()` |
| Corregir scoring y validación | Cuatro componentes nutricionales y respuestas HTTP 400 consistentes | `evaluar_objetivo()`, `validar_payload()` |
| Incorporar pruebas | Consistencia, inferencia, API, frontend y compatibilidad | `tests/test_lab1.py` |

### 1. Normalización y Extensión de la Base de Conocimiento

`info.json` es la fuente canónica: el código no mantiene una copia paralela de
ingredientes, recetas o reglas. Al iniciar, `lab1.py` carga el JSON y construye
índices por identificador.

| Entidad | Total | Identificación | Atributos uniformes |
| --- | ---: | --- | --- |
| Ingredientes | 27 | ID en `snake_case` | nombre, categoría, porción y nutrición |
| Recetas | 32 | ID en `snake_case` | nombre, descripción, ingredientes, tipo, dificultad y tiempo |
| Reglas | 32 | `R001` a `R032` | condiciones y conclusión |
| Objetivos | 3 | ID semántico | nombre y criterio de scoring |
| Tipos de comida | 5 | ID semántico | nombre y condición de filtro |

Cada ingrediente utiliza el mismo esquema nutricional:

```json
{
  "id": "pollo",
  "nombre": "Pollo",
  "categoria": "proteina_animal",
  "porcion": "100 g",
  "nutricion": {
    "calorias": 165,
    "proteinas": 31,
    "carbohidratos": 0,
    "grasas": 3.6
  }
}
```

Cada receta posee metadatos consistentes:

```json
{
  "id": "bowl_de_pollo",
  "nombre": "Bowl de pollo",
  "descripcion": "Pollo acompañado de arroz y brócoli.",
  "ingredientes": ["pollo", "arroz", "brocoli"],
  "tipo_comida": "almuerzo",
  "dificultad": "facil",
  "tiempo_preparacion_min": 30
}
```

Los hechos iniciales también se normalizan antes de inferir:

```json
{
  "objetivo_id": "perder_grasa",
  "tipo_comida_id": "almuerzo",
  "ingredientes_disponibles": ["pollo", "arroz"]
}
```

Los identificadores duplicados se eliminan conservando el orden de entrada.
Un ingrediente inexistente no se ignora silenciosamente: produce un error de
validación.

### 2. Segunda Categoría de Inferencia: `tipo_comida`

| Valor | Significado |
| --- | --- |
| `desayuno` | Evalúa únicamente reglas de desayuno |
| `almuerzo` | Evalúa únicamente reglas de almuerzo |
| `cena` | Evalúa únicamente reglas de cena |
| `snack` | Evalúa únicamente reglas de snack |
| `todos` | Omite el filtro de categoría y evalúa todas las reglas |

El tipo de comida actúa como filtro categórico. El objetivo nutricional no
descarta reglas: calcula la adecuación nutricional de las recetas que superaron
el filtro y el umbral. Las dos dimensiones cumplen funciones diferentes:

| Dimensión | Función |
| --- | --- |
| `tipo_comida` | Decide qué conjunto de reglas puede participar |
| `objetivo` | Determina cómo se puntúan y desempatan las recetas |

Una regla de producción normalizada combina ingredientes y tipo:

```json
{
  "id": "R010",
  "condiciones": {
    "ingredientes": ["pollo", "arroz", "brocoli"],
    "tipo_comida": "almuerzo"
  },
  "conclusion": {
    "receta_id": "bowl_de_pollo"
  }
}
```

### 3. Algoritmo de Confianza y Umbral Estricto

Sea $D$ el conjunto de ingredientes disponibles y $R$ el conjunto de
ingredientes requeridos por una regla. FitExpert calcula:

$$
P =
\frac{
  |\text{Ingredientes Disponibles} \cap \text{Ingredientes Requeridos}|
}{
  |\text{Ingredientes Requeridos}|
}
\times 100
$$

En notación compacta:

$$
P = \frac{|D \cap R|}{|R|} \times 100
$$

Ejemplo para una regla que requiere pollo, arroz y brócoli:

$$
P = \frac{|\{pollo, arroz\}|}{|\{pollo, arroz, brócoli\}|}
\times 100 = 66.67\%
$$

La condición de activación es estricta:

$$
P > 50\%
$$

Por tanto:

| Confianza | Resultado |
| ---: | --- |
| 100 % | Se recomienda; receta completa |
| 66.67 % | Se recomienda; se informan ingredientes faltantes |
| 50 % | Se descarta |
| Menor que 50 % | Se descarta |

Este valor es un **factor de confianza determinista por cobertura**, no una
probabilidad estadística obtenida mediante aprendizaje automático.

### 4. Ordenamiento Descendente y Desempate

Las recetas que superan el umbral se ordenan con una clave compuesta:

1. Mayor a menor confianza $P$.
2. Si $P$ empata, mayor puntuación nutricional para el objetivo seleccionado.
3. Si ambos valores empatan, nombre de receta en orden alfabético.

La confianza tiene prioridad sobre el scoring. Una receta con 100 % siempre
aparece antes que una con 66.67 %, aunque la segunda tenga una puntuación
nutricional superior.

El scoring usa cuatro componentes normalizados y produce un valor de 0 a 100:

| Objetivo | Componentes y peso máximo |
| --- | --- |
| Aumentar masa muscular | proteína 40, energía 20, carbohidratos 25, grasas 15 |
| Perder grasa | calorías 35, proteína 30, carbohidratos 20, grasas 15 |
| Mantener peso | energía 30, proteína 25, carbohidratos 25, grasas 20 |

Las etiquetas se asignan así:

| Puntuación | Adecuación |
| ---: | --- |
| 75 a 100 | Muy adecuada |
| 55 a 74.99 | Adecuada |
| Menor que 55 | Complementaria |

### 5. Validación Robusta y Pruebas Automatizadas

El endpoint valida el cuerpo antes de ejecutar el motor:

| Entrada inválida | Comportamiento |
| --- | --- |
| JSON malformado | HTTP 400 |
| Cuerpo que no es un objeto JSON | HTTP 400 |
| Objetivo nulo, desconocido o de tipo incorrecto | HTTP 400 |
| Tipo de comida nulo, desconocido o de tipo incorrecto | HTTP 400 |
| `ingredientes` ausente o no es una lista | HTTP 400 |
| Lista de ingredientes vacía | HTTP 400 |
| Elementos que no son texto | HTTP 400 |
| Identificadores desconocidos | HTTP 400 con detalle |
| Ingredientes duplicados | Se normalizan sin inflar los totales |

La suite `tests/test_lab1.py` comprueba:

- Esquema y consistencia de 27 ingredientes, 32 recetas y 32 reglas.
- Correspondencia entre condiciones de reglas y metadatos de recetas.
- Ausencia de ingredientes o conclusiones desconocidas.
- Exclusión de coincidencias exactamente iguales al 50 %.
- Orden descendente por confianza.
- Desempate mediante puntuación nutricional.
- Filtro por tipo de comida.
- Rankings distintos entre objetivos.
- Casos válidos e inválidos de la API.
- Presencia de la segunda categoría en la interfaz.
- Compatibilidad del alias `/api/recomendar`.
- Estado y metadatos reportados por `/health`.

## Arquitectura del Proyecto

| Archivo | Responsabilidad |
| --- | --- |
| `info.json` | Fuente única de catálogos, ingredientes, recetas y reglas |
| `lab1.py` | Carga, normalización, inferencia, scoring, explicación y API |
| `templates/index.html` | Formulario y estructura semántica de la interfaz |
| `static/app.js` | Captura de hechos, consumo de API y presentación |
| `static/styles.css` | Estados visuales, métricas y resultados |
| `tests/test_lab1.py` | Pruebas unitarias y de integración con Flask |

Flujo entre componentes:

```text
Usuario
  │
  ▼
index.html + app.js
  │  POST /api/recommend
  ▼
validar_payload()
  │
  ▼
crear_hechos()
  │
  ▼
motor_inferencia()
  ├─ filtra por tipo_comida
  ├─ calcula P por cada regla
  └─ conserva únicamente P > 50 %
  │
  ▼
calcular_nutricion() + evaluar_objetivo()
  │
  ▼
ordenar por P, scoring y nombre
  │
  ▼
construir_explicacion()
  │
  ▼
Respuesta JSON y tarjetas de resultados
```

## API JSON

### Endpoint Canónico

```http
POST /api/recommend
Content-Type: application/json
```

`POST /api/recomendar` se conserva como alias compatible, pero toda nueva
integración debe utilizar `/api/recommend`.

### Payload

Los tres campos son obligatorios:

```json
{
  "objetivo": "perder_grasa",
  "tipo_comida": "almuerzo",
  "ingredientes": ["pollo", "arroz"]
}
```

Valores válidos:

| Campo | Valores |
| --- | --- |
| `objetivo` | `aumentar_masa_muscular`, `perder_grasa`, `mantener_peso` |
| `tipo_comida` | `desayuno`, `almuerzo`, `cena`, `snack`, `todos` |
| `ingredientes` | IDs existentes en `info.json` |

Ejemplo con PowerShell:

```powershell
$body = @{
  objetivo = "perder_grasa"
  tipo_comida = "almuerzo"
  ingredientes = @("pollo", "arroz")
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:5001/api/recommend" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Esquema de Respuesta Exitosa

| Campo | Contenido |
| --- | --- |
| `hechos` | Memoria de trabajo normalizada |
| `objetivo` | ID, nombre y criterio nutricional |
| `tipo_comida` | ID y nombre del filtro aplicado |
| `umbral_coincidencia` | Valor 50.0; el operador aplicado es `>` |
| `ingredientes` | Ingredientes disponibles con metadatos completos |
| `recetas` | Recomendaciones ordenadas |
| `totales` | Cantidad de ingredientes, recetas y reglas activadas |

Cada elemento de `recetas` contiene:

| Campo | Contenido |
| --- | --- |
| `id`, `nombre`, `descripcion` | Identidad de la receta |
| `tipo_comida` | Categoría de la receta |
| `dificultad`, `tiempo_preparacion_min` | Metadatos de preparación |
| `ingredientes` | Requerimientos con nutrición por porción |
| `nutricion` | Totales de calorías, proteínas, carbohidratos y grasas |
| `adecuacion` | Etiqueta derivada del scoring |
| `puntuacion_objetivo` | Scoring total de 0 a 100 |
| `componentes_puntuacion` | Desglose de la puntuación |
| `coincidencia` | Porcentaje, cantidades, disponibles y faltantes |
| `regla_activada` | ID y tipo de la regla |
| `explicacion` | Justificación trazable de la recomendación |

Fragmento real de respuesta para `pollo + arroz`:

```json
{
  "hechos": {
    "objetivo_id": "perder_grasa",
    "tipo_comida_id": "almuerzo",
    "ingredientes_disponibles": ["pollo", "arroz"]
  },
  "objetivo": {
    "id": "perder_grasa",
    "nombre": "Perder grasa",
    "criterio": "Favorece control calórico, proteína suficiente y cantidades moderadas de carbohidratos y grasas."
  },
  "tipo_comida": {
    "id": "almuerzo",
    "nombre": "Almuerzo"
  },
  "umbral_coincidencia": 50.0,
  "recetas": [
    {
      "id": "pollo_a_la_plancha",
      "puntuacion_objetivo": 64.4,
      "coincidencia": {
        "porcentaje": 100.0,
        "cantidad_disponible": 1,
        "cantidad_requerida": 1,
        "ingredientes_disponibles": [
          {"id": "pollo", "nombre": "Pollo"}
        ],
        "ingredientes_faltantes": []
      },
      "regla_activada": {
        "id": "R004",
        "tipo_comida": "almuerzo"
      }
    },
    {
      "id": "bowl_de_pollo",
      "puntuacion_objetivo": 89.94,
      "coincidencia": {
        "porcentaje": 66.67,
        "cantidad_disponible": 2,
        "cantidad_requerida": 3,
        "ingredientes_disponibles": [
          {"id": "pollo", "nombre": "Pollo"},
          {"id": "arroz", "nombre": "Arroz integral"}
        ],
        "ingredientes_faltantes": [
          {"id": "brocoli", "nombre": "Brócoli"}
        ]
      },
      "regla_activada": {
        "id": "R010",
        "tipo_comida": "almuerzo"
      }
    }
  ],
  "totales": {
    "recetas": 2,
    "ingredientes": 2,
    "reglas_activadas": 2
  }
}
```

Aunque el bowl obtiene mayor scoring, aparece después porque 66.67 % es menor
que 100 %. Esto demuestra la prioridad del criterio de confianza.

### Respuesta de Error

```json
{
  "error": "Solicitud inválida.",
  "detalles": [
    "Debes proporcionar al menos un ingrediente."
  ]
}
```

Los errores de entrada devuelven HTTP 400 y una lista `detalles` apta para
presentarse al usuario.

### Estado del Servicio

```http
GET /health
```

```json
{
  "status": "ok",
  "version": "2.0.0",
  "evaluacion": "Parcial 1 v 2.0.0 · Sistemas Expertos",
  "ingredientes": 27,
  "recetas": 32,
  "reglas": 32
}
```

## Guía de Defensa del Sistema Experto

### Arquitectura del Motor de Inferencia

FitExpert utiliza reglas de producción transparentes y deterministas. Los hechos
iniciales ingresan a la memoria de trabajo y se evalúan hacia adelante contra
las condiciones de cada regla.

El ciclo de inferencia es:

1. Construir y normalizar la memoria de trabajo.
2. Seleccionar las reglas compatibles con `tipo_comida`.
3. Comparar el subconjunto disponible con los ingredientes de cada regla.
4. Calcular el factor de confianza $P$.
5. Activar únicamente reglas con $P > 50\%$.
6. Convertir cada conclusión en una receta candidata.
7. Calcular nutrición y scoring según el objetivo.
8. Ordenar y generar una explicación.

Las conclusiones son recetas terminales; no son premisas de otras reglas. Por
esa razón, una pasada completa sobre la base de reglas alcanza el punto de
terminación y no se necesita reinyectar conclusiones para nuevos ciclos.

Complejidad aproximada:

$$
O(n \times m)
$$

donde $n$ es el número de reglas evaluadas y $m$ el promedio de ingredientes
por regla. Con 32 reglas, el costo es pequeño y predecible.

### Flujo de Ejecución Paso a Paso

#### 1. Captura de Hechos Iniciales

El frontend envía ingredientes, objetivo y tipo de comida. `validar_payload()`
rechaza valores incorrectos y `crear_hechos()` elimina duplicados.

#### 2. Evaluación de Reglas de Producción

`motor_inferencia()` recorre las reglas. Cuando el tipo solicitado no es
`todos`, omite de inmediato las reglas de otras categorías.

#### 3. Cálculo de Confianza

`calcular_coincidencia()` obtiene la intersección, los faltantes y $P$. Una
regla con 50 % exacto no se activa.

#### 4. Ponderación Nutricional

`calcular_nutricion()` suma los cuatro valores nutricionales.
`evaluar_objetivo()` aplica pesos distintos para masa muscular, pérdida de
grasa o mantenimiento.

#### 5. Ordenamiento y Filtrado

Primero se aplica $P > 50\%$. Después se ordena por confianza descendente y,
solo en empate, por scoring descendente.

#### 6. Módulo de Explicación

`construir_explicacion()` informa la regla activada, la fracción coincidente,
el porcentaje, el scoring y los ingredientes que faltan. La recomendación es
auditable y no funciona como una caja negra.

### Casos de Prueba para Demostración en Vivo

#### Caso 1: prioridad de confianza sobre scoring

```json
{
  "objetivo": "perder_grasa",
  "tipo_comida": "almuerzo",
  "ingredientes": ["pollo", "arroz"]
}
```

Salida esperada:

| Orden | Receta | Confianza | Scoring | Faltante |
| ---: | --- | ---: | ---: | --- |
| 1 | Pollo a la plancha | 100 % | 64.40 | Ninguno |
| 2 | Bowl de pollo | 66.67 % | 89.94 | Brócoli |

Punto de defensa: el pollo aparece primero por tener mayor confianza, aunque el
bowl tiene mayor scoring.

#### Caso 2: segunda categoría y recomendación parcial

```json
{
  "objetivo": "mantener_peso",
  "tipo_comida": "cena",
  "ingredientes": ["pollo", "brocoli", "quinoa"]
}
```

Salida esperada:

| Orden | Receta | Confianza | Scoring | Faltante |
| ---: | --- | ---: | ---: | --- |
| 1 | Pollo con brócoli | 100 % | 42.46 | Ninguno |
| 2 | Bowl de pollo y quinoa | 75 % | 70.22 | Zanahoria |

Punto de defensa: solo aparecen reglas clasificadas como cena. Las reglas de
almuerzo con ingredientes similares quedan fuera antes de calcular el ranking.

#### Caso 3: demostración del umbral estricto

```json
{
  "objetivo": "mantener_peso",
  "tipo_comida": "snack",
  "ingredientes": ["manzana"]
}
```

Salida esperada:

```json
{
  "recetas": [],
  "totales": {
    "recetas": 0,
    "ingredientes": 1,
    "reglas_activadas": 0
  }
}
```

Punto de defensa: `manzana_con_almendras` coincide en 1 de 2 ingredientes,
equivalente a 50 %. Se descarta porque el requisito es $P > 50\%$, no
$P \ge 50\%$.

### Preguntas Frecuentes de la Cátedra

#### ¿Por qué se eligieron reglas de producción?

Porque el conocimiento del dominio puede expresarse como condiciones y
conclusiones legibles. Cada recomendación conserva trazabilidad hasta una regla
concreta y puede explicarse sin interpretar parámetros ocultos.

#### ¿Es realmente una probabilidad?

Es un factor de confianza basado en cobertura de requisitos. Está acotado entre
0 y 100 %, pero no representa frecuencia estadística ni fue aprendido a partir
de datos históricos.

#### ¿Por qué se considera evaluación hacia adelante?

El motor parte de hechos conocidos y avanza hacia conclusiones. Las conclusiones
son terminales, por lo que no existe una segunda capa de reglas que requiera
realimentación. Si se incorporaran conclusiones intermedias, el motor debería
iterar hasta no producir hechos nuevos.

#### ¿Qué diferencia existe entre objetivo y tipo de comida?

`tipo_comida` es un filtro de reglas. El objetivo es una función de evaluación
nutricional. Separarlos evita confundir elegibilidad categórica con calidad de
la recomendación.

#### ¿Por qué una receta incompleta puede recomendarse?

El parcial exige coincidencia porcentual. Una receta que supera 50 % es una
alternativa viable; el módulo de explicación muestra exactamente qué falta para
completarla.

#### ¿Cómo se garantiza la consistencia de los datos?

`info.json` es la única fuente de verdad. Las pruebas verifican que cada regla
apunte a una receta existente, que sus condiciones coincidan con la receta y
que todos los ingredientes estén registrados.

#### ¿Cómo escala la base de conocimiento?

Actualmente el motor evalúa cada regla compatible, con costo (O(n \times m)).
Para cientos o miles de reglas se puede indexar por `tipo_comida`, ingrediente
principal o estructuras RETE, sin cambiar el contrato de la API.

#### ¿Cómo se agrega una nueva receta?

Se registra el ingrediente si no existe, se agrega la receta normalizada y se
crea una regla cuya conclusión apunte al ID de la receta. Luego se ejecuta la
suite para validar referencias y estructura.

#### ¿Cómo se evita que un solo nutriente domine el ranking?

El scoring limita el peso máximo de cada componente. La proteína tiene como
máximo 40 puntos en masa muscular, mientras que los demás objetivos distribuyen
el peso de forma aún más equilibrada.

#### ¿Qué ocurre si la API recibe datos incorrectos?

La inferencia no se ejecuta. `validar_payload()` recopila errores y responde
HTTP 400 con detalles; así se evitan excepciones 500 por entradas controlables.

## Instalación, Ejecución y Pruebas

### Requisitos

- Python 3.10 o superior.
- pip.
- Navegador web.

### Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Ejecución

```powershell
python lab1.py
```

Abrir:

```text
http://127.0.0.1:5001/
```

Configuración opcional:

```powershell
$env:PORT = "8000"
$env:URL_PREFIX = "/parcial1-se"
$env:FLASK_DEBUG = "1"
python lab1.py
```

`FLASK_DEBUG` está desactivado por defecto y solo debe habilitarse durante
desarrollo local.

### Pruebas Automatizadas

```powershell
python -m unittest discover -s tests -v
```

Resultado esperado:

```text
Ran 13 tests
OK
```

## Recorrido Recomendado Durante la Defensa

| Orden | Pantalla o archivo | Qué demostrar |
| ---: | --- | --- |
| 1 | Interfaz web | Título, versión, objetivos, tipo de comida e ingredientes |
| 2 | `info.json` | Esquema normalizado y totales de la base |
| 3 | `lab1.py:calcular_coincidencia` | Fórmula y faltantes |
| 4 | `lab1.py:motor_inferencia` | Filtro categórico y umbral estricto |
| 5 | `lab1.py:evaluar_objetivo` | Scoring diferenciado |
| 6 | `lab1.py:recomendar_recetas` | Orden y desempate |
| 7 | `lab1.py:construir_explicacion` | Trazabilidad |
| 8 | Casos en vivo | Confianza, segunda categoría y 50 % excluido |
| 9 | `tests/test_lab1.py` | Evidencia automatizada |

Resumen oral:

> FitExpert 2.0.0 es un sistema basado en conocimiento con 27 ingredientes, 32
> recetas y 32 reglas normalizadas. Recibe ingredientes, objetivo nutricional y
> tipo de comida; calcula la cobertura de cada regla, conserva únicamente
> coincidencias mayores al 50 %, puntúa nutricionalmente las recetas y las
> ordena por confianza y scoring. Cada conclusión incluye la regla activada y
> los ingredientes faltantes, por lo que el razonamiento es trazable.

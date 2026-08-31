# FitExpert

FitExpert es un sistema basado en conocimiento desarrollado con Python y Flask.
Recomienda recetas a partir de tres grupos de hechos:

- Objetivo nutricional.
- Tipo de comida.
- Ingredientes disponibles.

El motor evalúa reglas de producción, calcula la coincidencia entre los
ingredientes disponibles y los requeridos, descarta resultados con una
coincidencia menor o igual al 50 % y evalúa nutricionalmente cada receta.

## Requisitos

- Python 3.10 o superior.
- pip.
- Navegador web.

## Instalación local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Ejecución

```powershell
python lab1.py
```

La aplicación queda disponible en:

```text
http://127.0.0.1:5001/
```

El puerto se puede cambiar con la variable `PORT`:

```powershell
$env:PORT = "8000"
python lab1.py
```

Para servir la aplicación detrás de un proxy que elimina un prefijo público:

```powershell
$env:URL_PREFIX = "/lab1-se"
python lab1.py
```

El modo de depuración está desactivado por defecto. Para habilitarlo únicamente
durante desarrollo local:

```powershell
$env:FLASK_DEBUG = "1"
python lab1.py
```

## Arquitectura

| Archivo | Responsabilidad |
| --- | --- |
| `info.json` | Fuente única de la base de conocimiento normalizada |
| `lab1.py` | Carga de conocimiento, inferencia, scoring, API y Flask |
| `templates/index.html` | Formulario y estructura de la interfaz |
| `static/app.js` | Consumo de la API y representación de resultados |
| `static/styles.css` | Presentación visual y estados de resultados |
| `tests/test_lab1.py` | Pruebas de consistencia, inferencia y validación |

El archivo `info.json` contiene:

- Catálogos de objetivos y tipos de comida.
- Ingredientes con ID, nombre, categoría, porción y nutrición.
- Recetas con metadatos uniformes.
- Reglas con `id`, `condiciones` y `conclusion`.

Al iniciar, `lab1.py` carga esta información y construye índices por ID. De
esta forma no existen dos bases de conocimiento independientes que puedan
desincronizarse.

## API

### Recomendación

```text
POST /api/recomendar
Content-Type: application/json
```

Todos los campos son obligatorios:

```json
{
  "objetivo": "perder_grasa",
  "tipo_comida": "almuerzo",
  "ingredientes": ["pollo", "arroz"]
}
```

Valores admitidos para `objetivo`:

- `aumentar_masa_muscular`
- `perder_grasa`
- `mantener_peso`

Valores admitidos para `tipo_comida`:

- `todos`
- `desayuno`
- `almuerzo`
- `cena`
- `snack`

### Estado del servicio

```text
GET /health
```

Respuesta:

```json
{
  "ingredientes": 27,
  "recetas": 32,
  "reglas": 32,
  "status": "ok",
  "version": "2.0.0"
}
```

## Actualizaciones y Modificaciones - Evaluación Parcial

### 1. Normalización y extensión de la base de conocimiento

La versión 2.0 normaliza todos los elementos:

- **27 ingredientes** con IDs en `snake_case`, nombre, categoría, porción y
  valores de calorías, proteínas, carbohidratos y grasas.
- **32 recetas** con ID, nombre, descripción, ingredientes, tipo de comida,
  dificultad y tiempo de preparación.
- **32 reglas de producción** identificadas desde `R001` hasta `R032`.
- **3 objetivos nutricionales** con un criterio de evaluación explícito.

Se agregaron ingredientes como salmón, quinoa, tofu, lentejas, garbanzos,
manzana, almendras, leche descremada, pepino y semillas de chía. También se
incorporaron recetas de desayuno, almuerzo, cena y snack.

Una regla normalizada tiene la siguiente estructura:

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

### 2. Segunda categoría: tipo de comida

Además del objetivo nutricional, el motor recibe `tipo_comida`. Las categorías
son desayuno, almuerzo, cena y snack. El valor `todos` permite consultar todas
las categorías.

Cada regla declara su tipo de comida. Si el usuario selecciona una categoría
específica, el motor solo evalúa las reglas pertenecientes a esa categoría.
Después calcula el scoring de cada receta usando el objetivo nutricional. Así,
la inferencia combina ambas dimensiones:

```text
objetivo nutricional + tipo de comida + ingredientes disponibles
```

### 3. Probabilidad o porcentaje de coincidencia

La confianza representa la proporción de ingredientes requeridos que el usuario
tiene disponibles:

```text
P = (ingredientes coincidentes / ingredientes requeridos) * 100
```

Ejemplo: si una receta requiere pollo, arroz y brócoli, pero el usuario tiene
pollo y arroz:

```text
P = (2 / 3) * 100 = 66.67 %
```

La regla supera el umbral y puede recomendarse. El filtro es estricto:

```text
P > 50 %
```

Una coincidencia exacta de 50 % no se incluye. La respuesta también informa los
ingredientes faltantes para completar las recetas parciales.

### 4. Ordenamiento descendente

Las recomendaciones se ordenan usando estas prioridades:

1. Mayor porcentaje de coincidencia.
2. En caso de empate, mayor puntuación para el objetivo nutricional.
3. Si persiste el empate, nombre de receta en orden alfabético.

El scoring nutricional produce un valor de 0 a 100 y combina cuatro componentes.
Ningún macronutriente puede aportar por sí solo más del 40 % de la puntuación:

- Aumentar masa muscular: proteína, energía, carbohidratos y grasas.
- Perder grasa: control calórico, proteína, carbohidratos y grasas moderadas.
- Mantener peso: cercanía a una comida balanceada en los cuatro valores.

### 5. Ejemplos de consulta y respuesta

Consulta con PowerShell:

```powershell
$body = @{
  objetivo = "perder_grasa"
  tipo_comida = "almuerzo"
  ingredientes = @("pollo", "arroz")
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:5001/api/recomendar" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

La respuesta contiene primero el pollo a la plancha con 100 % de coincidencia y
después el bowl de pollo con 66.67 %. Este fragmento resume los campos
principales:

```json
{
  "objetivo": {
    "id": "perder_grasa",
    "nombre": "Perder grasa"
  },
  "tipo_comida": {
    "id": "almuerzo",
    "nombre": "Almuerzo"
  },
  "umbral_coincidencia": 50.0,
  "recetas": [
    {
      "id": "pollo_a_la_plancha",
      "coincidencia": {
        "porcentaje": 100.0,
        "cantidad_disponible": 1,
        "cantidad_requerida": 1,
        "ingredientes_faltantes": []
      }
    },
    {
      "id": "bowl_de_pollo",
      "coincidencia": {
        "porcentaje": 66.67,
        "cantidad_disponible": 2,
        "cantidad_requerida": 3,
        "ingredientes_faltantes": [
          {"id": "brocoli", "nombre": "Brócoli"}
        ]
      }
    }
  ],
  "totales": {
    "ingredientes": 2,
    "recetas": 2,
    "reglas_activadas": 2
  }
}
```

Una solicitud inválida devuelve HTTP 400:

```json
{
  "error": "Solicitud inválida.",
  "detalles": [
    "Debes proporcionar al menos un ingrediente."
  ]
}
```

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas verifican:

- La consistencia entre ingredientes, recetas y reglas.
- El umbral estricto mayor al 50 %.
- El ordenamiento y desempate.
- El filtro por tipo de comida.
- La diferencia de scoring entre objetivos.
- La validación de JSON, valores nulos, listas vacías y tipos incorrectos.

## Guía breve para la defensa

1. Mostrar `info.json` para explicar la base de conocimiento normalizada.
2. Mostrar `motor_inferencia()` y `calcular_coincidencia()` en `lab1.py`.
3. Explicar que una regla se activa únicamente cuando supera el 50 %.
4. Mostrar `evaluar_objetivo()` y sus componentes ponderados.
5. Ejecutar una consulta con una receta completa y otra parcialmente coincidente.
6. Cambiar el tipo de comida para demostrar la segunda categoría.

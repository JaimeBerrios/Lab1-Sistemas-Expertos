# Parcial 1 v 2.0.0 · Sistemas Expertos

## Guion de Defensa en Vivo de FitExpert

Este documento es el guion cronológico para proyectar, explicar y demostrar
FitExpert frente al docente.

**Duración sugerida:** 8 a 10 minutos.

**Objetivo:** demostrar que FitExpert es un sistema basado en conocimiento
normalizado, con reglas de producción, segunda categoría, factor de certeza,
umbral estricto, scoring nutricional, explicación y validación automatizada.

> Las referencias corresponden exactamente a la versión v2.0.0. Activar los
> números de línea del editor antes de comenzar.

## Preparación Antes de Proyectar

1. Abrir el repositorio en el editor.
2. Preparar las pestañas **templates/index.html**, **info.json**, **lab1.py** y
   **tests/test_lab1.py**.
3. Iniciar la aplicación:

~~~powershell
python lab1.py
~~~

4. Abrir http://127.0.0.1:5001/.
5. Comprobar las pruebas:

~~~powershell
python -m unittest discover -s tests -v
~~~

Resultado esperado:

~~~text
Ran 13 tests
OK
~~~

## Mapa Rápido de Evidencias

| Requerimiento | Archivo | Líneas |
| --- | --- | ---: |
| Versión y metadatos | **info.json** | 3-14 |
| Header v2.0.0 | **templates/index.html** | 26 |
| Tipos de comida | **info.json** | 35-41 |
| 27 ingredientes | **info.json** | 43-71 |
| 32 recetas | **info.json** | 72-105 |
| 32 reglas | **info.json** | 106-139 |
| Hechos iniciales | **lab1.py** | 91-97 |
| Fórmula de coincidencia | **lab1.py** | 100-119 |
| Motor, categoría y umbral | **lab1.py** | 122-146 |
| Cuatro macros por receta | **lab1.py** | 150-162 |
| Scoring | **lab1.py** | 170-213 |
| Explicación | **lab1.py** | 216-232 |
| Faltantes y regla activada | **lab1.py** | 248-287 |
| Ordenamiento | **lab1.py** | 290-300 |
| Validación | **lab1.py** | 327-358 |
| Suite automatizada | **tests/test_lab1.py** | 1-223 |

---

## Acto 1: Introducción y Versión del Proyecto

### Qué mostrar en pantalla

1. Navegador: página principal de FitExpert.
2. **templates/index.html**, línea **26**.
3. **info.json**, líneas **3-14**.

### Qué señalar

- El header “Parcial 1 v 2.0.0 · Sistemas Expertos”.
- Nombre, versión, tipo de inferencia, umbral y ordenamiento.

### Qué decir

> Buenos días. Nuestro proyecto se llama FitExpert y corresponde al Parcial 1,
> versión 2.0.0, de Sistemas Expertos. Recomienda recetas utilizando hechos
> iniciales, reglas de producción y un factor de certeza explicable.
>
> info.json contiene la base de conocimiento; lab1.py implementa el motor y la
> API Flask; index.html, styles.css y app.js forman la interfaz; y
> tests/test_lab1.py verifica la consistencia y el comportamiento.
>
> La entrada combina ingredientes, objetivo nutricional y tipo de comida. La
> salida contiene recetas con más del 50 por ciento, ordenadas por certeza y
> scoring nutricional.

### Transición

> Primero mostraremos cómo se normalizó y extendió el conocimiento.

---

## Acto 2: Normalización y Extensión de la Base de Conocimiento

### Qué mostrar en pantalla

| Paso | Archivo | Líneas | Evidencia |
| ---: | --- | ---: | --- |
| 1 | **info.json** | 43-71 | 27 ingredientes |
| 2 | **info.json** | 44-70 | Cuatro atributos nutricionales |
| 3 | **info.json** | 72-105 | 32 recetas |
| 4 | **info.json** | 106-139 | 32 reglas R001 a R032 |
| 5 | **lab1.py** | 150-162 | Cálculo de macros |

### Acción

1. Abrir **info.json** en la línea 43.
2. Mostrar el ingrediente huevo en la línea 44.
3. Mostrar el final del arreglo, línea 70.
4. Mostrar recetas, líneas 72-105.
5. Mostrar reglas, líneas 106-139.
6. Cambiar a **lab1.py**, líneas 150-162.

### Qué decir

> Abrimos info.json para validar que los hechos y reglas están normalizados bajo
> un esquema homogéneo.
>
> Entre las líneas 43 y 71 hay 27 ingredientes. Cada registro utiliza un ID en
> snake_case, nombre, categoría, porción, calorías, proteínas, carbohidratos y
> grasas.
>
> Entre las líneas 72 y 105 están las 32 recetas. Cada una declara ID,
> descripción, ingredientes, tipo, dificultad y tiempo. Entre las líneas 106 y
> 139 están las 32 reglas, con condiciones y conclusión separadas.
>
> Los macros no se duplican dentro de cada receta. Las recetas referencian IDs y
> calcular_nutricion, líneas 150-162 de lab1.py, suma los cuatro valores. Esto
> evita inconsistencias en datos derivados.

### Explicación técnica

1. **Fuente única:** **info.json** contiene el conocimiento.
2. **Integridad referencial:** recetas y reglas usan IDs.
3. **Desacoplamiento:** agregar conocimiento no cambia el motor.

### Si preguntan por los totales

> Son 27 ingredientes, 32 recetas, 32 reglas, 3 objetivos y 5 valores de tipo.

### Transición

> Con la base normalizada, veremos cómo los hechos alimentan el motor.

---

## Acto 3: Motor de Inferencia y Segunda Categoría tipo_comida

### Qué mostrar en pantalla

| Archivo | Líneas | Evidencia |
| --- | ---: | --- |
| **info.json** | 35-41 | todos, desayuno, almuerzo, cena y snack |
| **lab1.py** | 91-97 | Construcción de hechos |
| **lab1.py** | 122-130 | Recorrido y filtro |
| **lab1.py** | 132-146 | Coincidencia y activación |

### Acción

1. Mostrar **info.json**, líneas 35-41.
2. Cambiar a **lab1.py**, líneas 91-97.
3. Señalar objetivo_id, tipo_comida_id e ingredientes_disponibles.
4. Mostrar motor_inferencia, líneas 122-146.
5. Detenerse en las líneas 129-130.

### Qué decir

> Pasamos al núcleo del motor, donde se captura la segunda dimensión solicitada.
>
> crear_hechos construye la memoria de trabajo con objetivo, tipo e
> ingredientes, y elimina duplicados.
>
> Los tipos son desayuno, almuerzo, cena, snack y todos. En las líneas 122 a 146
> el motor recorre las reglas. Las líneas 129 y 130 descartan una regla si no
> pertenece al tipo solicitado. Con todos se evalúan todas las categorías.

### Precisión conceptual

| Dimensión | Responsabilidad |
| --- | --- |
| tipo_comida | Filtra reglas |
| Objetivo | Define scoring de desempate |
| Ingredientes | Determinan coincidencia |

### Si preguntan por encadenamiento

> El proceso avanza de hechos a conclusiones. Las recetas son terminales y no
> son premisas de otras reglas; una pasada alcanza el punto de terminación.

### Transición

> Después del filtro categórico, el motor calcula cuánto conoce de cada regla.

---

## Acto 4: Algoritmo de Certeza y Filtro Estricto Mayor al 50%

### Qué mostrar en pantalla

| Archivo | Líneas | Evidencia |
| --- | ---: | --- |
| **lab1.py** | 100-119 | Coincidentes, faltantes y porcentaje |
| **lab1.py** | 132-136 | Umbral y descarte |

### Fórmula

$$
P =
\frac{
  |\text{Ingredientes Disponibles} \cap \text{Ingredientes Requeridos}|
}{
  |\text{Ingredientes Requeridos}|
}
\times 100
$$

### Acción

1. Abrir **lab1.py**, línea 100.
2. Señalar el conjunto de disponibles, línea 101.
3. Señalar coincidentes y faltantes, líneas 102-107.
4. Señalar la operación, líneas 108-112.
5. Mostrar las líneas 132-136.

### Qué decir

> Aquí se calcula la confianza con teoría de conjuntos.
>
> Los disponibles se convierten en conjunto. Luego obtenemos coincidentes y
> faltantes. El porcentaje es la cantidad coincidente dividida entre la cantidad
> requerida, multiplicada por cien.
>
> En las líneas 135 y 136, si el porcentaje es menor o igual a 50 se ejecuta
> continue y la regla se descarta. Solo se activan reglas con más de 50 por
> ciento.

### Ejemplo oral

> Pollo y arroz contra una regla de pollo, arroz y brócoli produce dos de tres:
> 66.67 por ciento. La regla se conserva y brócoli aparece como faltante.

### Aclaración

> Es certeza determinista por cobertura, no probabilidad estadística aprendida.

### Transición

> Las reglas válidas se evalúan según el objetivo y luego se ordenan.

---

## Acto 5: Ordenamiento Descendente y Scoring Nutricional

### Qué mostrar en pantalla

| Archivo | Líneas | Evidencia |
| --- | ---: | --- |
| **lab1.py** | 170-213 | Fórmulas por objetivo |
| **lab1.py** | 290-300 | Ordenamiento compuesto |

### Acción

1. Mostrar evaluar_objetivo, líneas 170-213.
2. Señalar masa muscular, perder grasa y mantenimiento.
3. Mostrar recomendar_recetas, líneas 290-300.
4. Detenerse en las líneas 294-299.

### Qué decir

> El scoring cambia por objetivo. Masa muscular pondera proteína, energía,
> carbohidratos y grasas. Perder grasa prioriza control calórico y proteína.
> Mantener peso mide cercanía a una comida equilibrada.
>
> En las líneas 294 a 300 está el ordenamiento. El signo negativo produce orden
> descendente. La primera clave es el porcentaje; la segunda es el scoring; y el
> nombre es un tercer criterio estable.

### Regla para memorizar

~~~text
1.º Mayor certeza
2.º Mayor scoring, solo si la certeza empata
3.º Nombre alfabético, solo si ambos empatan
~~~

### Transición

> Finalmente, el sistema no solo concluye: justifica la recomendación.

---

## Acto 6: Explicación y Manejo de Errores

### Qué mostrar en pantalla

| Archivo | Líneas | Evidencia |
| --- | ---: | --- |
| **lab1.py** | 216-232 | Explicación natural |
| **lab1.py** | 248-287 | Faltantes y regla activada |
| **lab1.py** | 327-358 | Validación |
| **tests/test_lab1.py** | 1-223 | 13 pruebas |

### Acción

1. Mostrar construir_explicacion, líneas 216-232.
2. Señalar ingredientes_faltantes, líneas 226-231.
3. Mostrar la respuesta, líneas 248-287.
4. Señalar regla_activada, líneas 280-286.
5. Mostrar validar_payload, líneas 327-358.
6. Proyectar la terminal con las pruebas.

### Qué decir

> El sistema es transparente: explica por qué se activó cada regla e informa
> qué ingredientes faltan.
>
> construir_explicacion genera una frase con regla, fracción coincidente,
> porcentaje y scoring. La respuesta contiene nutrición, porcentaje,
> disponibles, faltantes y regla activada. La interfaz lo presenta en un panel
> desplegable.
>
> validar_payload rechaza JSON incorrecto, nulos, listas vacías, tipos inválidos
> e ingredientes desconocidos. La suite ejecuta 13 pruebas de consistencia,
> umbral, ordenamiento, categorías, API e interfaz.

### Comando para proyectar

~~~powershell
python -m unittest discover -s tests -v
~~~

### Transición

> Ahora comprobaremos los requerimientos con tres casos preparados.

---

## Acto 7: Demostración en Vivo

### Instrucciones

1. Volver al navegador.
2. Usar **Limpiar** entre casos.
3. Confirmar objetivo y tipo.
4. Leer primero el porcentaje y luego abrir la explicación.

### Resumen de Casos

| Caso | Objetivo | Tipo | Ingredientes | Salida esperada |
| ---: | --- | --- | --- | --- |
| 1 | Aumentar masa muscular | Desayuno | Chía, Yogur griego, Banana | Pudín de chía, 100 %, scoring 62.55 |
| 2 | Perder grasa | Almuerzo | Pollo, Arroz integral | Pollo 100 %; Bowl 66.67 % |
| 3 | Mantener peso | Snack | Manzana | 0 recetas; 50 % o menos se descarta |

### Caso 1: Coincidencia Completa

#### Acción

1. Presionar **Cargar caso demo**, o seleccionar:
   - Objetivo: **Aumentar masa muscular**.
   - Tipo: **Desayuno**.
   - Ingredientes: **Semillas de chía**, **Yogur griego**, **Banana**.
2. Presionar **Ejecutar sistema experto**.
3. Abrir “¿Por qué el sistema experto recomienda esto?”.

#### Resultado exacto

| Receta | Certeza | Scoring | Faltantes | Regla |
| --- | ---: | ---: | --- | --- |
| Pudín de chía | 100 % | 62.55 | Ninguno | R032 |

#### Qué decir

> Tres de tres ingredientes equivalen a 100 por ciento. La receta está completa
> y la regla R032 queda trazada.

#### Descartes

Las demás reglas de desayuno comparten como máximo un ingrediente. Pancakes usa
solo banana de tres requeridos: 33.33 %.

### Caso 2: Coincidencia Parcial Mayor al 50%

#### Acción

1. Presionar **Limpiar**.
2. Objetivo: **Perder grasa**.
3. Tipo: **Almuerzo**.
4. Ingredientes: **Pollo** y **Arroz integral**.
5. Ejecutar.

#### Resultado exacto

| Orden | Receta | Certeza | Scoring | Faltantes | Regla |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | Pollo a la plancha | 100 % | 64.40 | Ninguno | R004 |
| 2 | Bowl de pollo | 66.67 % | 89.94 | Brócoli | R010 |

#### Qué decir

> Pollo aparece primero por su certeza de 100 por ciento. El bowl tiene dos de
> tres ingredientes, 66.67 por ciento, e informa que falta brócoli.
>
> Aunque el bowl tiene mayor scoring, no desplaza al primer resultado porque la
> certeza es la clave primaria.

#### Descartes

- Bowl fitness: 2 de 4 = 50 %, descartado.
- Bowl completo: 2 de 5 = 40 %, descartado.
- Bowl mexicano: 2 de 6 = 33.33 %, descartado.
- Otras categorías: descartadas por tipo_comida.

### Caso 3: Umbral Estricto Menor o Igual al 50%

#### Acción

1. Presionar **Limpiar**.
2. Objetivo: **Mantener peso**.
3. Tipo: **Snack**.
4. Ingrediente: **Manzana**.
5. Ejecutar.

#### Resultado exacto

~~~text
0 recetas
Ninguna receta superó el umbral estricto de coincidencia mayor al 50%.
~~~

#### Qué decir

> Manzana con almendras coincide en uno de dos ingredientes, exactamente 50 por
> ciento. Como se exige un valor mayor, se descarta. El parfait coincide en uno
> de cuatro, 25 por ciento, y también se descarta.

### Cierre de la demostración

> Los casos prueban coincidencia completa, recomendación parcial con faltantes y
> descarte estricto. También prueban la segunda categoría, el orden y la
> explicación.

---

## Acto 8: Preguntas Frecuentes y Justificaciones

### ¿Por qué reglas de producción?

> Porque el conocimiento se expresa con condiciones y conclusiones legibles.
> Cada recomendación se rastrea hasta una regla concreta.

### ¿Es una probabilidad estadística?

> No. Es certeza determinista por cobertura. No proviene de aprendizaje
> automático ni de frecuencias históricas.

### ¿Cómo se garantiza la consistencia?

> info.json es la única fuente de verdad. Las pruebas validan referencias entre
> reglas, recetas e ingredientes.

### ¿Por qué no guardar macros totales en cada receta?

> Serían datos derivados duplicados. La receta referencia ingredientes y
> calcular_nutricion suma los cuatro valores.

### ¿Cómo escala?

> La complejidad es O(n × m), con n reglas y m ingredientes promedio. Para una
> base mayor se puede indexar por tipo o ingrediente, o utilizar RETE.

### ¿Cómo se agrega una receta?

> Se registran ingredientes nuevos, se crea la receta con IDs válidos y una
> regla que concluya su ID. Después se ejecutan las pruebas.

### ¿Por qué recomendar recetas incompletas?

> Si supera 50 por ciento es una opción viable y el sistema indica exactamente
> qué falta.

### ¿Qué hace cada dimensión?

> El tipo filtra reglas, la certeza mide cobertura y el objetivo calcula scoring
> para desempatar.

### ¿Cómo se evita que un nutriente domine?

> Cada objetivo distribuye 100 puntos entre cuatro componentes. La proteína
> nunca aporta más de 40 puntos.

### ¿Qué pasa con una entrada inválida?

> El motor no se ejecuta. La API responde HTTP 400 con detalles antes de inferir.

---

## Cierre Oral

### Qué mostrar

Volver a la interfaz con el Caso 2 y la explicación abierta.

### Qué decir

> FitExpert v2.0.0 cumple el parcial con 27 ingredientes, 32 recetas y 32 reglas;
> segunda categoría; certeza con umbral mayor al 50 por ciento; scoring;
> ordenamiento; explicación trazable y validación automatizada.
>
> La interfaz permite observar la conclusión y el proceso que la produjo. Con
> esto finalizamos la demostración.

---

## Apéndice: API

~~~http
POST /api/recommend
Content-Type: application/json
~~~

~~~json
{
  "objetivo": "perder_grasa",
  "tipo_comida": "almuerzo",
  "ingredientes": ["pollo", "arroz"]
}
~~~

Consulta:

~~~powershell
$body = @{ objetivo = "perder_grasa"; tipo_comida = "almuerzo"; ingredientes = @("pollo", "arroz") } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5001/api/recommend" -Method Post -ContentType "application/json" -Body $body
~~~

POST /api/recomendar permanece como alias.

~~~http
GET /health
~~~

~~~json
{
  "status": "ok",
  "version": "2.0.0",
  "evaluacion": "Parcial 1 v 2.0.0 · Sistemas Expertos",
  "ingredientes": 27,
  "recetas": 32,
  "reglas": 32
}
~~~

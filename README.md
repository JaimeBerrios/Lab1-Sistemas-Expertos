# FitExpert

Sistema experto de recetas nutricionales desarrollado con Flask.

La aplicacion permite seleccionar un objetivo fisico y los ingredientes disponibles. Luego ejecuta reglas de inferencia hacia adelante para recomendar recetas compatibles, ordenar los resultados segun el objetivo, calcular calorias/proteinas aproximadas y explicar que regla fue activada.

## Requisitos

Debes tener instalado:

- Python 3.10 o superior
- pip
- Un navegador web

Opcional pero recomendado:

- Git
- Un entorno virtual de Python

## Instalacion local

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activacion del entorno virtual, ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Ejecutar el programa

Con el entorno virtual activado:

```powershell
python lab1.py
```

Abre esta direccion en el navegador:

```text
http://127.0.0.1:5001/
```

## Salir del entorno virtual

Cuando termines de trabajar, puedes salir del entorno virtual con:

```powershell
deactivate
```

## Probar la API

El sistema tambien expone un endpoint JSON:

```text
POST http://127.0.0.1:5001/api/recomendar
```

Ejemplo con PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5001/api/recomendar" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"objetivo":"mantener_peso","ingredientes":["pollo","arroz","brocoli"]}'
```

## Configuracion opcional

Por defecto se ejecuta en el puerto `5001`. Puedes cambiarlo con la variable `PORT`:

```powershell
$env:PORT = "8000"
python lab1.py
```

Para publicarlo detras de un proxy con prefijo, usa `URL_PREFIX`:

```powershell
$env:URL_PREFIX = "/lab1-se"
python lab1.py
```

## Guia visual para la defensa del proyecto

Durante la defensa se recomienda alternar entre la aplicacion abierta en el
navegador y el archivo `lab1.py`. El siguiente orden permite explicar con
claridad la descripcion del proyecto, la base de conocimiento y el motor de
inferencia.

| Momento de la explicacion | Archivo o pantalla | Elemento que se debe mostrar |
| --- | --- | --- |
| Descripcion del proyecto | Aplicacion en el navegador | Pagina principal de FitExpert |
| Base de conocimiento | `lab1.py` | Diccionario `INGREDIENTES` |
| Base de conocimiento | `lab1.py` | Lista `REGLAS` |
| Base de conocimiento | `lab1.py` | Diccionario `RECETAS` |
| Motor de inferencia | `lab1.py` | Funcion `motor_inferencia()` |
| Procesamiento de resultados | `lab1.py` | Funciones `calcular_nutricion()` y `evaluar_objetivo()` |
| Demostracion | Aplicacion en el navegador | Seleccion de parametros y resultados |

### 1. Descripcion del proyecto

Mostrar la aplicacion en el navegador en:

```text
http://127.0.0.1:5001/
```

Durante esta parte se deben senalar el selector del objetivo fisico, la lista
de ingredientes, el boton para ejecutar el sistema y el area de resultados.

**Explicacion sugerida:**

> FitExpert es un sistema experto que recomienda recetas nutricionales. El
> usuario selecciona su objetivo fisico y los ingredientes que tiene
> disponibles. El sistema determina que recetas puede preparar, calcula sus
> calorias y proteinas y las ordena segun el objetivo seleccionado.

### 2. Base de conocimiento: ingredientes

Abrir `lab1.py` y mostrar la seccion `INGREDIENTES`, ubicada debajo del
comentario `BASE DE CONOCIMIENTOS`.

```python
INGREDIENTES = {
    "huevo": {"calorias": 78, "proteinas": 6},
    "avena": {"calorias": 150, "proteinas": 5},
    "pollo": {"calorias": 165, "proteinas": 31},
}
```

**Explicacion sugerida:**

> Esta es una parte de la base de conocimiento. Aqui se almacena la
> informacion nutricional aproximada de cada ingrediente, especificamente sus
> calorias y proteinas por porcion.

### 3. Base de conocimiento: reglas

En `lab1.py`, mostrar la lista `REGLAS`. No es necesario explicar las 20 reglas
individualmente; basta con presentar dos o tres ejemplos.

```python
{
    "if": ["pollo", "arroz", "brocoli"],
    "then": ["bowl_de_pollo"]
}
```

**Explicacion sugerida:**

> Las reglas representan el conocimiento del experto y tienen una estructura
> SI-ENTONCES. En este ejemplo, si el usuario tiene pollo, arroz y brocoli,
> entonces el sistema puede recomendar un bowl de pollo.

### 4. Base de conocimiento: recetas

Continuar en `lab1.py` y mostrar el diccionario `RECETAS`.

**Explicacion sugerida:**

> En esta seccion se encuentra la informacion completa de las recetas: su
> nombre, descripcion e ingredientes. El identificador de cada receta conecta
> la conclusion de una regla con los datos que posteriormente se muestran al
> usuario.

La base de conocimiento puede resumirse como **lo que el sistema sabe**:
ingredientes, valores nutricionales, recetas y reglas.

### 5. Motor de inferencia

Mostrar la funcion `motor_inferencia()` de `lab1.py`, especialmente la
condicion que comprueba los ingredientes:

```python
for indice, regla in enumerate(REGLAS, start=1):
    condiciones = regla["if"]
    resultado = regla["then"][0]

    if all(ingrediente in ingredientes_usuario for ingrediente in condiciones):
```

**Explicacion sugerida:**

> El motor utiliza encadenamiento hacia adelante. Comienza con los ingredientes
> seleccionados por el usuario, que funcionan como hechos iniciales. Despues
> recorre todas las reglas y utiliza `all` para comprobar que todos los
> ingredientes requeridos por una regla esten disponibles. Si la condicion se
> cumple, la regla se activa y se obtiene la receta correspondiente.

Luego se puede mostrar el lugar donde se registra la regla activada:

```python
reglas_activadas.append(
    {
        "regla": indice,
        "condiciones": condiciones,
        "receta_id": resultado,
    }
)
```

El motor de inferencia puede resumirse como **la manera en que el sistema usa
lo que sabe para obtener una conclusion**.

### 6. Calculo nutricional y evaluacion del objetivo

Mostrar primero la funcion `calcular_nutricion()`.

> Esta funcion suma las calorias y proteinas de los ingredientes utilizados en
> cada receta encontrada.

Despues, mostrar la funcion `evaluar_objetivo()` y senalar sus tres casos:

```python
if objetivo == "aumentar_masa_muscular":
    # Prioriza el aporte de proteinas.
elif objetivo == "perder_grasa":
    # Considera el control de calorias y las proteinas.
else:
    # Busca una opcion balanceada para mantener el peso.
```

> Esta funcion asigna una puntuacion y un nivel de adecuacion a cada receta.
> Gracias a esa puntuacion, las recomendaciones se presentan desde la mas
> apropiada hasta la menos apropiada para el objetivo elegido.

### 7. Demostracion final

Regresar a la aplicacion en el navegador y utilizar, por ejemplo, los
siguientes datos:

```text
Objetivo: Aumentar masa muscular
Ingredientes: Pollo, arroz, brocoli, tomate y aguacate
```

Despues de ejecutar el sistema, se deben senalar en los resultados:

- El nombre y la descripcion de la receta.
- Las calorias y proteinas aproximadas.
- El nivel de adecuacion para el objetivo.
- El numero de la regla activada.
- La explicacion generada por el sistema.

**Explicacion sugerida:**

> Los ingredientes seleccionados se convierten en los hechos iniciales. El
> motor revisa la base de conocimiento, activa las reglas que cumplen todas sus
> condiciones y presenta las recetas encontradas. Finalmente, las ordena de
> acuerdo con su puntuacion para el objetivo fisico seleccionado.

### Recorrido recomendado

```text
Navegador: pagina principal
    -> lab1.py: INGREDIENTES
    -> lab1.py: REGLAS
    -> lab1.py: RECETAS
    -> lab1.py: motor_inferencia()
    -> lab1.py: calcular_nutricion()
    -> lab1.py: evaluar_objetivo()
    -> Navegador: demostracion y resultados
```

### Resumen para memorizar

> FitExpert es un sistema experto de recetas nutricionales. Su base de
> conocimiento contiene ingredientes, datos nutricionales, recetas y 20 reglas
> de tipo SI-ENTONCES. Su motor de inferencia utiliza encadenamiento hacia
> adelante: toma los ingredientes como hechos, revisa cuales reglas se cumplen
> y genera las recetas correspondientes. Despues calcula las calorias y
> proteinas, evalua cada receta segun el objetivo fisico y ordena los
> resultados.

## Guion para el video de presentacion

El video se divide entre tres integrantes. No es necesario realizar una
conclusion grupal; el tercer integrante puede cerrar la presentacion despues de
la demostracion.

### Integrante 1: presentacion del proyecto

**Contenido que debe mostrar:** pagina principal de la aplicacion.

**Guion sugerido:**

> Buenos dias. Nuestro proyecto se llama FitExpert y es un sistema experto de
> recetas nutricionales. Su objetivo es recomendar platillos de acuerdo con los
> ingredientes disponibles y el objetivo fisico del usuario, que puede ser
> aumentar masa muscular, perder grasa o mantener el peso.
>
> Para utilizarlo, el usuario selecciona su objetivo y marca los ingredientes
> que tiene disponibles. La aplicacion fue desarrollada con Python y Flask para
> la logica del sistema, y con HTML, CSS y JavaScript para la interfaz web.

### Integrante 2: funcionamiento del sistema experto

**Contenido que debe mostrar:** las secciones `INGREDIENTES`, `REGLAS` y las
funciones del motor de inferencia en `lab1.py`.

**Guion sugerido:**

> El sistema cuenta con una base de conocimientos que contiene la informacion
> aproximada de calorias y proteinas de cada ingrediente, ademas de un conjunto
> de reglas que relacionan ingredientes con recetas.
>
> Por ejemplo, una regla establece que si el usuario tiene pollo, arroz y
> brocoli, entonces se puede recomendar un bowl de pollo.
>
> El motor utiliza encadenamiento hacia adelante. Esto significa que parte de
> los ingredientes seleccionados por el usuario y revisa todas las reglas. Una
> regla se activa cuando todos sus ingredientes se encuentran entre los
> seleccionados.
>
> Para cada receta encontrada, el sistema calcula las calorias y proteinas. A
> continuacion, asigna una puntuacion segun el objetivo fisico y ordena las
> recomendaciones desde la mas adecuada hasta la menos adecuada. Tambien
> presenta una explicacion de la regla que fue activada.

### Integrante 3: demostracion de la aplicacion

**Contenido que debe mostrar:** ejecucion de la aplicacion y resultados en el
navegador.

**Guion sugerido:**

> Ahora realizaremos una demostracion. Primero seleccionamos el objetivo
> aumentar masa muscular. Despues marcamos ingredientes como pollo, arroz,
> brocoli, tomate y aguacate, y presionamos el boton para ejecutar el sistema
> experto.
>
> La aplicacion muestra las recetas que pueden prepararse con esos ingredientes.
> En cada resultado podemos observar el nombre y la descripcion de la receta,
> sus calorias, la cantidad aproximada de proteina, su nivel de adecuacion y el
> numero de la regla activada.
>
> Los resultados aparecen ordenados de acuerdo con el objetivo seleccionado. En
> este caso se priorizan las recetas con mayor aporte de proteina porque el
> objetivo es aumentar masa muscular.
>
> Si cambiamos el objetivo a perder grasa, el sistema utiliza otro criterio de
> puntuacion y prioriza el control de calorias junto con una cantidad adecuada
> de proteina.
>
> De esta manera, FitExpert utiliza reglas de inferencia y datos nutricionales
> para recomendar recetas compatibles con los ingredientes y el objetivo fisico
> seleccionado. Con esto finalizamos la demostracion del funcionamiento de la
> aplicacion.

### Duracion sugerida

| Tiempo | Responsable | Contenido |
| --- | --- | --- |
| 0:00-1:00 | Integrante 1 | Presentacion, objetivo y tecnologias |
| 1:00-2:30 | Integrante 2 | Base de conocimientos y motor de inferencia |
| 2:30-4:30 | Integrante 3 | Demostracion, resultados y cierre |

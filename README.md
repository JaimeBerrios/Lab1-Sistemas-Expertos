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

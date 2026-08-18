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

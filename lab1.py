import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

URL_PREFIX = os.environ.get("URL_PREFIX", "").rstrip("/")
app.config["APPLICATION_ROOT"] = URL_PREFIX or "/"


class PrefixMiddleware:
    """Expone a Flask el prefijo publico eliminado por el proxy inverso."""

    def __init__(self, application, prefix):
        self.application = application
        self.prefix = prefix

    def __call__(self, environ, start_response):
        forwarded_prefix = environ.get("HTTP_X_FORWARDED_PREFIX")
        prefix = (forwarded_prefix or self.prefix).rstrip("/")
        if prefix:
            environ["SCRIPT_NAME"] = prefix
        return self.application(environ, start_response)


app.wsgi_app = PrefixMiddleware(app.wsgi_app, URL_PREFIX)


# BASE DE CONOCIMIENTO NORMALIZADA
# info.json es la fuente unica de ingredientes, recetas, reglas y catalogos.
BASE_CONOCIMIENTO_PATH = Path(__file__).with_name("info.json")
with BASE_CONOCIMIENTO_PATH.open(encoding="utf-8") as archivo:
    BASE_CONOCIMIENTO = json.load(archivo)

SISTEMA = BASE_CONOCIMIENTO["sistema_experto"]
INGREDIENTES = {
    ingrediente["id"]: ingrediente for ingrediente in BASE_CONOCIMIENTO["ingredientes"]
}
RECETAS = {receta["id"]: receta for receta in BASE_CONOCIMIENTO["recetas"]}
REGLAS = BASE_CONOCIMIENTO["reglas_produccion"]
OBJETIVOS_CONFIG = {
    objetivo["id"]: objetivo for objetivo in BASE_CONOCIMIENTO["catalogos"]["objetivos"]
}
TIPOS_COMIDA_CONFIG = {
    tipo["id"]: tipo for tipo in BASE_CONOCIMIENTO["catalogos"]["tipos_comida"]
}
OBJETIVOS = {
    identificador: datos["nombre"] for identificador, datos in OBJETIVOS_CONFIG.items()
}
TIPOS_COMIDA = {
    identificador: datos["nombre"] for identificador, datos in TIPOS_COMIDA_CONFIG.items()
}
UMBRAL_COINCIDENCIA = float(SISTEMA["inferencia"]["umbral_coincidencia"])

GRUPOS_INGREDIENTES = [
    {
        "id": "proteinas",
        "nombre": "Proteínas",
        "icono": "bi-egg-fried",
        "categorias": {"proteina_animal", "proteina_vegetal", "legumbre", "lacteo"},
    },
    {
        "id": "carbohidratos",
        "nombre": "Carbohidratos",
        "icono": "bi-lightning-charge",
        "categorias": {"cereal", "tuberculo"},
    },
    {
        "id": "vegetales_frutas",
        "nombre": "Vegetales y frutas",
        "icono": "bi-flower1",
        "categorias": {"vegetal", "fruta"},
    },
    {
        "id": "grasas_otros",
        "nombre": "Grasas y otros",
        "icono": "bi-droplet-half",
        "categorias": {"grasa_saludable", "semilla"},
    },
]


def formato_ingrediente(ingrediente_id):
    ingrediente = INGREDIENTES.get(ingrediente_id)
    return ingrediente["nombre"] if ingrediente else ingrediente_id.replace("_", " ").title()


def crear_hechos(objetivo, tipo_comida, ingredientes):
    """Construye la memoria de trabajo con hechos normalizados y sin duplicados."""
    return {
        "objetivo_id": objetivo,
        "tipo_comida_id": tipo_comida,
        "ingredientes_disponibles": list(dict.fromkeys(ingredientes)),
    }


def calcular_coincidencia(ingredientes_disponibles, ingredientes_requeridos):
    disponibles = set(ingredientes_disponibles)
    coincidencias = [
        ingrediente for ingrediente in ingredientes_requeridos if ingrediente in disponibles
    ]
    faltantes = [
        ingrediente for ingrediente in ingredientes_requeridos if ingrediente not in disponibles
    ]
    porcentaje = (
        len(coincidencias) / len(ingredientes_requeridos) * 100
        if ingredientes_requeridos
        else 0
    )
    return {
        "porcentaje": round(porcentaje, 2),
        "cantidad_disponible": len(coincidencias),
        "cantidad_requerida": len(ingredientes_requeridos),
        "ingredientes_disponibles": coincidencias,
        "ingredientes_faltantes": faltantes,
    }


def motor_inferencia(hechos):
    """Evalua reglas por tipo de comida y conserva coincidencias mayores al 50 %."""
    reglas_activadas = []
    tipo_solicitado = hechos["tipo_comida_id"]

    for regla in REGLAS:
        condiciones = regla["condiciones"]
        if tipo_solicitado != "todos" and condiciones["tipo_comida"] != tipo_solicitado:
            continue

        coincidencia = calcular_coincidencia(
            hechos["ingredientes_disponibles"], condiciones["ingredientes"]
        )
        if coincidencia["porcentaje"] <= UMBRAL_COINCIDENCIA:
            continue

        reglas_activadas.append(
            {
                "regla_id": regla["id"],
                "receta_id": regla["conclusion"]["receta_id"],
                "condiciones": condiciones,
                "coincidencia": coincidencia,
            }
        )

    return reglas_activadas


def calcular_nutricion(ingredientes):
    totales = {
        "calorias": 0,
        "proteinas": 0,
        "carbohidratos": 0,
        "grasas": 0,
    }
    for ingrediente_id in ingredientes:
        nutricion = INGREDIENTES[ingrediente_id]["nutricion"]
        for nutriente in totales:
            totales[nutriente] += nutricion[nutriente]

    return {nutriente: round(valor, 1) for nutriente, valor in totales.items()}


def puntuacion_cercania(valor, objetivo, tolerancia):
    """Devuelve una cercania normalizada entre 0 y 1."""
    return max(0.0, 1 - abs(valor - objetivo) / tolerancia)


def evaluar_objetivo(objetivo, nutricion):
    calorias = nutricion["calorias"]
    proteinas = nutricion["proteinas"]
    carbohidratos = nutricion["carbohidratos"]
    grasas = nutricion["grasas"]

    if objetivo == "aumentar_masa_muscular":
        componentes = {
            "proteinas": min(proteinas / 40, 1) * 40,
            "energia": puntuacion_cercania(calorias, 500, 420) * 20,
            "carbohidratos": puntuacion_cercania(carbohidratos, 55, 55) * 25,
            "grasas": puntuacion_cercania(grasas, 15, 20) * 15,
        }
    elif objetivo == "perder_grasa":
        componentes = {
            "calorias": puntuacion_cercania(calorias, 300, 350) * 35,
            "proteinas": min(proteinas / 35, 1) * 30,
            "carbohidratos": puntuacion_cercania(carbohidratos, 30, 45) * 20,
            "grasas": puntuacion_cercania(grasas, 10, 18) * 15,
        }
    else:
        componentes = {
            "energia": puntuacion_cercania(calorias, 400, 350) * 30,
            "proteinas": puntuacion_cercania(proteinas, 25, 25) * 25,
            "carbohidratos": puntuacion_cercania(carbohidratos, 45, 45) * 25,
            "grasas": puntuacion_cercania(grasas, 15, 20) * 20,
        }

    puntuacion = round(sum(componentes.values()), 2)
    if puntuacion >= 75:
        etiqueta = "Muy adecuada"
    elif puntuacion >= 55:
        etiqueta = "Adecuada"
    else:
        etiqueta = "Complementaria"

    return {
        "puntuacion": puntuacion,
        "etiqueta": etiqueta,
        "componentes": {
            clave: round(valor, 2) for clave, valor in componentes.items()
        },
        "razon": OBJETIVOS_CONFIG[objetivo]["criterio"],
    }


def construir_explicacion(activacion, receta, objetivo, evaluacion):
    coincidencia = activacion["coincidencia"]
    explicacion = (
        f"La regla {activacion['regla_id']} coincide en "
        f"{coincidencia['cantidad_disponible']} de "
        f"{coincidencia['cantidad_requerida']} ingredientes "
        f"({coincidencia['porcentaje']:.2f} %). "
        f"Para {OBJETIVOS[objetivo].lower()}, {receta['nombre']} obtiene "
        f"{evaluacion['puntuacion']:.2f} puntos nutricionales."
    )
    if coincidencia["ingredientes_faltantes"]:
        faltantes = ", ".join(
            formato_ingrediente(item)
            for item in coincidencia["ingredientes_faltantes"]
        )
        explicacion += f" Para completar la receta faltan: {faltantes}."
    return explicacion


def serializar_ingrediente(ingrediente_id):
    ingrediente = INGREDIENTES[ingrediente_id]
    return {
        "id": ingrediente["id"],
        "nombre": ingrediente["nombre"],
        "categoria": ingrediente["categoria"],
        "porcion": ingrediente["porcion"],
        "nutricion": ingrediente["nutricion"],
    }


def construir_receta(activacion, objetivo):
    receta = RECETAS[activacion["receta_id"]]
    nutricion = calcular_nutricion(receta["ingredientes"])
    evaluacion = evaluar_objetivo(objetivo, nutricion)
    coincidencia = activacion["coincidencia"]

    return {
        "id": receta["id"],
        "nombre": receta["nombre"],
        "descripcion": receta["descripcion"],
        "tipo_comida": {
            "id": receta["tipo_comida"],
            "nombre": TIPOS_COMIDA[receta["tipo_comida"]],
        },
        "dificultad": receta["dificultad"],
        "tiempo_preparacion_min": receta["tiempo_preparacion_min"],
        "ingredientes": [
            serializar_ingrediente(item) for item in receta["ingredientes"]
        ],
        "nutricion": nutricion,
        "adecuacion": evaluacion["etiqueta"],
        "puntuacion_objetivo": evaluacion["puntuacion"],
        "componentes_puntuacion": evaluacion["componentes"],
        "coincidencia": {
            **coincidencia,
            "ingredientes_disponibles": [
                {"id": item, "nombre": formato_ingrediente(item)}
                for item in coincidencia["ingredientes_disponibles"]
            ],
            "ingredientes_faltantes": [
                {"id": item, "nombre": formato_ingrediente(item)}
                for item in coincidencia["ingredientes_faltantes"]
            ],
        },
        "regla_activada": {
            "id": activacion["regla_id"],
            "tipo_comida": activacion["condiciones"]["tipo_comida"],
        },
        "explicacion": construir_explicacion(
            activacion, receta, objetivo, evaluacion
        ),
    }


def recomendar_recetas(objetivo, tipo_comida, ingredientes_usuario):
    hechos = crear_hechos(objetivo, tipo_comida, ingredientes_usuario)
    activaciones = motor_inferencia(hechos)
    recetas = [construir_receta(activacion, objetivo) for activacion in activaciones]
    recetas.sort(
        key=lambda receta: (
            -receta["coincidencia"]["porcentaje"],
            -receta["puntuacion_objetivo"],
            receta["nombre"],
        )
    )

    return {
        "hechos": hechos,
        "objetivo": {
            "id": objetivo,
            "nombre": OBJETIVOS[objetivo],
            "criterio": OBJETIVOS_CONFIG[objetivo]["criterio"],
        },
        "tipo_comida": {
            "id": tipo_comida,
            "nombre": TIPOS_COMIDA[tipo_comida],
        },
        "umbral_coincidencia": UMBRAL_COINCIDENCIA,
        "ingredientes": [
            serializar_ingrediente(item)
            for item in hechos["ingredientes_disponibles"]
        ],
        "recetas": recetas,
        "totales": {
            "recetas": len(recetas),
            "ingredientes": len(hechos["ingredientes_disponibles"]),
            "reglas_activadas": len(activaciones),
        },
    }


def validar_payload(data):
    errores = []
    if not isinstance(data, dict):
        return None, ["El cuerpo debe ser un objeto JSON."]

    objetivo = data.get("objetivo")
    tipo_comida = data.get("tipo_comida")
    ingredientes = data.get("ingredientes")

    if not isinstance(objetivo, str) or objetivo not in OBJETIVOS:
        errores.append("El objetivo nutricional no es válido.")
    if not isinstance(tipo_comida, str) or tipo_comida not in TIPOS_COMIDA:
        errores.append("El tipo de comida no es válido.")
    if not isinstance(ingredientes, list):
        errores.append("El campo ingredientes debe ser una lista.")
    elif not ingredientes:
        errores.append("Debes proporcionar al menos un ingrediente.")
    elif any(not isinstance(item, str) for item in ingredientes):
        errores.append("Todos los ingredientes deben ser identificadores de texto.")
    else:
        ingredientes = list(
            dict.fromkeys(item.strip().lower() for item in ingredientes)
        )
        desconocidos = [item for item in ingredientes if item not in INGREDIENTES]
        if desconocidos:
            errores.append(
                "Ingredientes desconocidos: " + ", ".join(sorted(desconocidos)) + "."
            )

    if errores:
        return None, errores
    return crear_hechos(objetivo, tipo_comida, ingredientes), []


@app.get("/")
def index():
    ingredientes = [serializar_ingrediente(item) for item in INGREDIENTES]
    grupos_ingredientes = [
        {
            **grupo,
            "ingredientes": [
                ingrediente
                for ingrediente in ingredientes
                if ingrediente["categoria"] in grupo["categorias"]
            ],
        }
        for grupo in GRUPOS_INGREDIENTES
    ]
    return render_template(
        "index.html",
        objetivos=OBJETIVOS,
        tipos_comida=TIPOS_COMIDA,
        ingredientes=ingredientes,
        grupos_ingredientes=grupos_ingredientes,
        recetas_count=len(RECETAS),
        reglas_count=len(REGLAS),
    )


@app.post("/api/recommend")
def api_recommend():
    data = request.get_json(silent=True)
    hechos, errores = validar_payload(data)
    if errores:
        return jsonify({"error": "Solicitud inválida.", "detalles": errores}), 400

    resultado = recomendar_recetas(
        hechos["objetivo_id"],
        hechos["tipo_comida_id"],
        hechos["ingredientes_disponibles"],
    )
    return jsonify(resultado)


@app.post("/api/recomendar")
def api_recomendar():
    """Alias conservado para clientes de FitExpert 1.x y 2.0 inicial."""
    return api_recommend()


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "version": SISTEMA["version"],
            "evaluacion": SISTEMA["evaluacion"],
            "ingredientes": len(INGREDIENTES),
            "recetas": len(RECETAS),
            "reglas": len(REGLAS),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="127.0.0.1", port=port)

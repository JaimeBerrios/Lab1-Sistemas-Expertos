import os

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# En local la aplicacion se sirve desde "/". Si se publica detras de un proxy
# inverso, se puede definir URL_PREFIX, por ejemplo: /lab1-se.
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


# 1. BASE DE CONOCIMIENTOS
# Información nutricional aproximada por porción.
INGREDIENTES = {
    "huevo": {"calorias": 78, "proteinas": 6},
    "avena": {"calorias": 150, "proteinas": 5},
    "pollo": {"calorias": 165, "proteinas": 31},
    "espinaca": {"calorias": 23, "proteinas": 3},
    "tomate": {"calorias": 18, "proteinas": 1},
    "atun": {"calorias": 132, "proteinas": 29},
    "brocoli": {"calorias": 35, "proteinas": 2.4},
    "yogur_griego": {"calorias": 100, "proteinas": 10},
    "arroz": {"calorias": 130, "proteinas": 2.7},
    "banana": {"calorias": 105, "proteinas": 1.3},
    "lechuga": {"calorias": 15, "proteinas": 1},
    "aguacate": {"calorias": 160, "proteinas": 2},
    "pan_integral": {"calorias": 80, "proteinas": 4},
    "zanahoria": {"calorias": 41, "proteinas": 0.9},
    "camote": {"calorias": 112, "proteinas": 2},
    "frijoles": {"calorias": 127, "proteinas": 9},
    "maiz": {"calorias": 96, "proteinas": 3.4},
}

NOMBRES_INGREDIENTES = {
    "atun": "Atún",
    "brocoli": "Brócoli",
    "maiz": "Maíz",
    "yogur_griego": "Yogur griego",
    "pan_integral": "Pan integral",
}


# 2. REGLAS DEL SISTEMA EXPERTO
REGLAS = [
    {"if": ["huevo"], "then": ["huevo_hervido"]},
    {"if": ["huevo"], "then": ["huevo_pochado"]},
    {"if": ["avena"], "then": ["avena_cocida"]},
    {"if": ["pollo"], "then": ["pollo_a_la_plancha"]},
    {"if": ["huevo", "espinaca"], "then": ["huevo_con_espinaca"]},
    {"if": ["atun", "huevo"], "then": ["ensalada_de_atun_y_huevo"]},
    {"if": ["pollo", "brocoli"], "then": ["pollo_con_brocoli"]},
    {"if": ["yogur_griego", "avena"], "then": ["yogur_con_avena"]},
    {"if": ["huevo", "espinaca", "tomate"], "then": ["omelette_fitness"]},
    {"if": ["pollo", "arroz", "brocoli"], "then": ["bowl_de_pollo"]},
    {"if": ["avena", "huevo", "banana"], "then": ["pancakes_fitness"]},
    {"if": ["pollo", "lechuga", "tomate"], "then": ["ensalada_proteica"]},
    {"if": ["pollo", "arroz", "brocoli", "tomate"], "then": ["bowl_fitness_de_pollo"]},
    {"if": ["atun", "arroz", "aguacate", "tomate"], "then": ["bowl_de_atun_con_aguacate"]},
    {"if": ["pollo", "lechuga", "tomate", "aguacate"], "then": ["ensalada_de_pollo"]},
    {"if": ["pan_integral", "huevo", "aguacate", "tomate"], "then": ["tostada_proteica"]},
    {
        "if": ["pollo", "arroz", "brocoli", "zanahoria", "aguacate"],
        "then": ["bowl_completo_de_pollo"],
    },
    {
        "if": ["pollo", "camote", "brocoli", "zanahoria", "aguacate"],
        "then": ["plato_fitness_de_pollo"],
    },
    {
        "if": ["pollo", "arroz", "frijoles", "tomate", "maiz", "aguacate"],
        "then": ["bowl_mexicano_de_pollo"],
    },
    {
        "if": ["atun", "huevo", "arroz", "tomate", "aguacate", "espinaca"],
        "then": ["bowl_de_atun_y_huevo"],
    },
]


# 3. INFORMACIÓN DE LAS RECETAS
RECETAS = {
    "huevo_hervido": {
        "nombre": "Huevo hervido",
        "descripcion": "Huevo cocido en agua.",
        "ingredientes": ["huevo"],
    },
    "huevo_pochado": {
        "nombre": "Huevo pochado",
        "descripcion": "Huevo cocinado en agua caliente.",
        "ingredientes": ["huevo"],
    },
    "avena_cocida": {
        "nombre": "Avena cocida",
        "descripcion": "Avena preparada con agua o leche.",
        "ingredientes": ["avena"],
    },
    "pollo_a_la_plancha": {
        "nombre": "Pollo a la plancha",
        "descripcion": "Pechuga de pollo preparada a la plancha.",
        "ingredientes": ["pollo"],
    },
    "huevo_con_espinaca": {
        "nombre": "Huevo con espinaca",
        "descripcion": "Huevo acompañado de espinaca.",
        "ingredientes": ["huevo", "espinaca"],
    },
    "ensalada_de_atun_y_huevo": {
        "nombre": "Ensalada de atún y huevo",
        "descripcion": "Ensalada rica en proteínas.",
        "ingredientes": ["atun", "huevo"],
    },
    "pollo_con_brocoli": {
        "nombre": "Pollo con brócoli",
        "descripcion": "Pollo acompañado de brócoli.",
        "ingredientes": ["pollo", "brocoli"],
    },
    "yogur_con_avena": {
        "nombre": "Yogur con avena",
        "descripcion": "Yogur griego acompañado de avena.",
        "ingredientes": ["yogur_griego", "avena"],
    },
    "omelette_fitness": {
        "nombre": "Omelette fitness",
        "descripcion": "Omelette de huevo, espinaca y tomate.",
        "ingredientes": ["huevo", "espinaca", "tomate"],
    },
    "bowl_de_pollo": {
        "nombre": "Bowl de pollo",
        "descripcion": "Pollo acompañado de arroz y brócoli.",
        "ingredientes": ["pollo", "arroz", "brocoli"],
    },
    "pancakes_fitness": {
        "nombre": "Pancakes fitness",
        "descripcion": "Pancakes preparados con avena, huevo y banana.",
        "ingredientes": ["avena", "huevo", "banana"],
    },
    "ensalada_proteica": {
        "nombre": "Ensalada proteica",
        "descripcion": "Ensalada de pollo, lechuga y tomate.",
        "ingredientes": ["pollo", "lechuga", "tomate"],
    },
    "bowl_fitness_de_pollo": {
        "nombre": "Bowl fitness de pollo",
        "descripcion": "Bowl de pollo, arroz, brócoli y tomate.",
        "ingredientes": ["pollo", "arroz", "brocoli", "tomate"],
    },
    "bowl_de_atun_con_aguacate": {
        "nombre": "Bowl de atún con aguacate",
        "descripcion": "Atún acompañado de arroz, tomate y aguacate.",
        "ingredientes": ["atun", "arroz", "aguacate", "tomate"],
    },
    "ensalada_de_pollo": {
        "nombre": "Ensalada de pollo",
        "descripcion": "Ensalada fresca de pollo y vegetales.",
        "ingredientes": ["pollo", "lechuga", "tomate", "aguacate"],
    },
    "tostada_proteica": {
        "nombre": "Tostada proteica",
        "descripcion": "Pan integral con huevo, aguacate y tomate.",
        "ingredientes": ["pan_integral", "huevo", "aguacate", "tomate"],
    },
    "bowl_completo_de_pollo": {
        "nombre": "Bowl completo de pollo",
        "descripcion": "Bowl completo con pollo, arroz y vegetales.",
        "ingredientes": ["pollo", "arroz", "brocoli", "zanahoria", "aguacate"],
    },
    "plato_fitness_de_pollo": {
        "nombre": "Plato fitness de pollo",
        "descripcion": "Pollo acompañado de camote y vegetales.",
        "ingredientes": ["pollo", "camote", "brocoli", "zanahoria", "aguacate"],
    },
    "bowl_mexicano_de_pollo": {
        "nombre": "Bowl mexicano de pollo",
        "descripcion": "Bowl con pollo, arroz, frijoles, tomate, maíz y aguacate.",
        "ingredientes": ["pollo", "arroz", "frijoles", "tomate", "maiz", "aguacate"],
    },
    "bowl_de_atun_y_huevo": {
        "nombre": "Bowl de atún y huevo",
        "descripcion": "Bowl de alto contenido proteico.",
        "ingredientes": ["atun", "huevo", "arroz", "tomate", "aguacate", "espinaca"],
    },
}


OBJETIVOS = {
    "aumentar_masa_muscular": "Aumentar masa muscular",
    "perder_grasa": "Perder grasa",
    "mantener_peso": "Mantener peso",
}

CRITERIOS_OBJETIVO = {
    "aumentar_masa_muscular": {
        "nombre": "Alto aporte de proteína",
        "descripcion": "Prioriza recetas con mayor cantidad de proteína para favorecer la recuperación y el desarrollo muscular.",
    },
    "perder_grasa": {
        "nombre": "Control de calorías",
        "descripcion": "Prioriza recetas con menos calorías y una buena cantidad de proteína para apoyar la pérdida de grasa.",
    },
    "mantener_peso": {
        "nombre": "Balance nutricional",
        "descripcion": "Prioriza recetas equilibradas en energía y proteína para mantener el peso corporal.",
    },
}


def formato_ingrediente(ingrediente):
    return NOMBRES_INGREDIENTES.get(ingrediente, ingrediente.replace("_", " ").title())


def motor_inferencia(ingredientes_usuario):
    reglas_activadas = []
    recetas_encontradas = set()

    for indice, regla in enumerate(REGLAS, start=1):
        condiciones = regla["if"]
        resultado = regla["then"][0]

        if all(ingrediente in ingredientes_usuario for ingrediente in condiciones):
            if resultado not in recetas_encontradas:
                recetas_encontradas.add(resultado)
                reglas_activadas.append(
                    {
                        "regla": indice,
                        "condiciones": condiciones,
                        "receta_id": resultado,
                    }
                )

    return reglas_activadas


def calcular_nutricion(ingredientes):
    calorias = 0
    proteinas = 0

    for ingrediente in ingredientes:
        if ingrediente in INGREDIENTES:
            calorias += INGREDIENTES[ingrediente]["calorias"]
            proteinas += INGREDIENTES[ingrediente]["proteinas"]

    return calorias, proteinas


def evaluar_objetivo(objetivo, calorias, proteinas):
    if objetivo == "aumentar_masa_muscular":
        puntuacion = proteinas * 3 + calorias / 90
        if proteinas >= 30:
            etiqueta = "Muy adecuada"
        elif proteinas >= 15:
            etiqueta = "Adecuada"
        else:
            etiqueta = "Complementaria"
        razon = "Se prioriza por su aporte de proteína."
    elif objetivo == "perder_grasa":
        puntuacion = proteinas * 2 - calorias / 70
        if calorias <= 250 and proteinas >= 10:
            etiqueta = "Muy adecuada"
        elif calorias <= 400:
            etiqueta = "Adecuada"
        else:
            etiqueta = "Moderada"
        razon = "Se evalúa por control calórico y proteína disponible."
    else:
        distancia_balance = abs(calorias - 350)
        puntuacion = proteinas * 1.8 - distancia_balance / 80
        if 250 <= calorias <= 500 and proteinas >= 12:
            etiqueta = "Muy adecuada"
        elif calorias <= 550:
            etiqueta = "Adecuada"
        else:
            etiqueta = "Moderada"
        razon = "Se evalúa como una opción balanceada para mantener el peso."

    return {
        "puntuacion": round(puntuacion, 2),
        "etiqueta": etiqueta,
        "razon": razon,
    }


def construir_explicacion(regla_activada, receta, objetivo_nombre, evaluacion):
    ingredientes = ", ".join(
        formato_ingrediente(ingrediente) for ingrediente in regla_activada["condiciones"]
    )
    return (
        f"Regla {regla_activada['regla']} activada: como el usuario tiene "
        f"{ingredientes}, se recomienda {receta['nombre']}. "
        f"Para el objetivo '{objetivo_nombre}', la receta se clasifica como "
        f"{evaluacion['etiqueta'].lower()} porque {evaluacion['razon'].lower()}"
    )


def construir_receta(receta_id, objetivo, regla_activada):
    receta = RECETAS[receta_id]
    calorias, proteinas = calcular_nutricion(receta["ingredientes"])
    evaluacion = evaluar_objetivo(objetivo, calorias, proteinas)
    objetivo_nombre = OBJETIVOS.get(objetivo, OBJETIVOS["mantener_peso"])

    return {
        "id": receta_id,
        "nombre": receta["nombre"],
        "descripcion": receta["descripcion"],
        "ingredientes": [
            {
                "id": ingrediente,
                "nombre": formato_ingrediente(ingrediente),
                "calorias": INGREDIENTES[ingrediente]["calorias"],
                "proteinas": INGREDIENTES[ingrediente]["proteinas"],
            }
            for ingrediente in receta["ingredientes"]
        ],
        "calorias": calorias,
        "proteinas": round(proteinas, 1),
        "criterio": CRITERIOS_OBJETIVO[objetivo]["nombre"],
        "adecuacion": evaluacion["etiqueta"],
        "puntuacion": evaluacion["puntuacion"],
        "regla_activada": {
            "numero": regla_activada["regla"],
            "condiciones": [
                {"id": ingrediente, "nombre": formato_ingrediente(ingrediente)}
                for ingrediente in regla_activada["condiciones"]
            ],
            "resultado": receta_id,
        },
        "explicacion": construir_explicacion(
            regla_activada,
            receta,
            objetivo_nombre,
            evaluacion,
        ),
    }


def recomendar_recetas(objetivo, ingredientes_usuario):
    if objetivo not in OBJETIVOS:
        objetivo = "mantener_peso"

    ingredientes_validos = [
        ingrediente
        for ingrediente in ingredientes_usuario
        if ingrediente in INGREDIENTES
    ]
    reglas_activadas = motor_inferencia(ingredientes_validos)
    recetas = [
        construir_receta(regla["receta_id"], objetivo, regla)
        for regla in reglas_activadas
    ]
    recetas.sort(key=lambda receta: receta["puntuacion"], reverse=True)

    return {
        "objetivo": objetivo,
        "objetivo_nombre": OBJETIVOS.get(objetivo, OBJETIVOS["mantener_peso"]),
        "criterio_objetivo": CRITERIOS_OBJETIVO[objetivo],
        "ingredientes": [
            {"id": ingrediente, "nombre": formato_ingrediente(ingrediente)}
            for ingrediente in ingredientes_validos
        ],
        "recetas": recetas,
        "totales": {
            "recetas": len(recetas),
            "ingredientes": len(ingredientes_validos),
            "reglas_activadas": len(reglas_activadas),
        },
    }


@app.route("/")
def index():
    ingredientes = [
        {
            "id": ingrediente,
            "nombre": formato_ingrediente(ingrediente),
            "calorias": datos["calorias"],
            "proteinas": datos["proteinas"],
        }
        for ingrediente, datos in INGREDIENTES.items()
    ]
    return render_template(
        "index.html",
        objetivos=OBJETIVOS,
        ingredientes=ingredientes,
    )


@app.post("/api/recomendar")
def api_recomendar():
    data = request.get_json(silent=True) or {}
    objetivo = data.get("objetivo", "mantener_peso")
    ingredientes = data.get("ingredientes", [])

    if not isinstance(ingredientes, list):
        return jsonify({"error": "El campo ingredientes debe ser una lista."}), 400

    if objetivo not in OBJETIVOS:
        return jsonify({"error": "El objetivo físico seleccionado no es válido."}), 400

    resultado = recomendar_recetas(objetivo, ingredientes)
    return jsonify(resultado)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug, host="127.0.0.1", port=port)

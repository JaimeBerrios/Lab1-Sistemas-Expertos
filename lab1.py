# FITEXPERT
# Sistema experto de recetas nutricionales

# 1. BASE DE CONOCIMIENTOS
# Informacion nutricional aproximada por porcion
INGREDIENTES = {
    "huevo": {
        "calorias": 78,
        "proteinas": 6
    },
    "avena": {
        "calorias": 150,
        "proteinas": 5
    },
    "pollo": {
        "calorias": 165,
        "proteinas": 31
    },
    "espinaca": {
        "calorias": 23,
        "proteinas": 3
    },
    "tomate": {
        "calorias": 18,
        "proteinas": 1
    },
    "atun": {
        "calorias": 132,
        "proteinas": 29
    },
    "brocoli": {
        "calorias": 35,
        "proteinas": 2.4
    },
    "yogur_griego": {
        "calorias": 100,
        "proteinas": 10
    },
    "arroz": {
        "calorias": 130,
        "proteinas": 2.7
    },
    "banana": {
        "calorias": 105,
        "proteinas": 1.3
    },
    "lechuga": {
        "calorias": 15,
        "proteinas": 1
    },
    "aguacate": {
        "calorias": 160,
        "proteinas": 2
    },
    "pan_integral": {
        "calorias": 80,
        "proteinas": 4
    },
    "zanahoria": {
        "calorias": 41,
        "proteinas": 0.9
    },
    "camote": {
        "calorias": 112,
        "proteinas": 2
    },
    "frijoles": {
        "calorias": 127,
        "proteinas": 9
    },
    "maiz": {
        "calorias": 96,
        "proteinas": 3.4
    }
}

# 2. REGLAS DEL SISTEMA EXPERTO

REGLAS = [

    # Recetas simples
    {
        "if": ["huevo"],
        "then": ["huevo_hervido"]
    },

    {
        "if": ["huevo"],
        "then": ["huevo_pochado"]
    },

    {
        "if": ["avena"],
        "then": ["avena_cocida"]
    },

    {
        "if": ["pollo"],
        "then": ["pollo_a_la_plancha"]
    },

    # Recetas de 2 ingredientes

    {
        "if": ["huevo", "espinaca"],
        "then": ["huevo_con_espinaca"]
    },

    {
        "if": ["atun", "huevo"],
        "then": ["ensalada_de_atun_y_huevo"]
    },

    {
        "if": ["pollo", "brocoli"],
        "then": ["pollo_con_brocoli"]
    },

    {
        "if": ["yogur_griego", "avena"],
        "then": ["yogur_con_avena"]
    },

    # Recetas de 3 ingredientes
    {
        "if": ["huevo", "espinaca", "tomate"],
        "then": ["omelette_fitness"]
    },

    {
        "if": ["pollo", "arroz", "brocoli"],
        "then": ["bowl_de_pollo"]
    },

    {
        "if": ["avena", "huevo", "banana"],
        "then": ["pancakes_fitness"]
    },

    {
        "if": ["pollo", "lechuga", "tomate"],
        "then": ["ensalada_proteica"]
    },

    # Recetas de 4 ingredientes
    {
        "if": ["pollo", "arroz", "brocoli", "tomate"],
        "then": ["bowl_fitness_de_pollo"]
    },

    {
        "if": ["atun", "arroz", "aguacate", "tomate"],
        "then": ["bowl_de_atun_con_aguacate"]
    },

    {
        "if": ["pollo", "lechuga", "tomate", "aguacate"],
        "then": ["ensalada_de_pollo"]
    },

    {
        "if": ["pan_integral", "huevo", "aguacate", "tomate"],
        "then": ["tostada_proteica"]
    },

    # Recetas de 5 ingredientes
    {
        "if": [
            "pollo",
            "arroz",
            "brocoli",
            "zanahoria",
            "aguacate"
        ],
        "then": ["bowl_completo_de_pollo"]
    },

    {
        "if": [
            "pollo",
            "camote",
            "brocoli",
            "zanahoria",
            "aguacate"
        ],
        "then": ["plato_fitness_de_pollo"]
    },

    {
        "if": [
            "pollo",
            "arroz",
            "frijoles",
            "tomate",
            "maiz",
            "aguacate"
        ],
        "then": ["bowl_mexicano_de_pollo"]
    },

    {
        "if": [
            "atun",
            "huevo",
            "arroz",
            "tomate",
            "aguacate",
            "espinaca"
        ],
        "then": ["bowl_de_atun_y_huevo"]
    }
]

# 3. INFORMACION DE LAS RECETAS

RECETAS = {

    "huevo_hervido": {
        "nombre": "Huevo hervido",
        "descripcion": "Huevo cocido en agua.",
        "ingredientes": ["huevo"]
    },

    "huevo_pochado": {
        "nombre": "Huevo pochado",
        "descripcion": "Huevo cocinado en agua caliente.",
        "ingredientes": ["huevo"]
    },

    "avena_cocida": {
        "nombre": "Avena cocida",
        "descripcion": "Avena preparada con agua o leche.",
        "ingredientes": ["avena"]
    },

    "pollo_a_la_plancha": {
        "nombre": "Pollo a la plancha",
        "descripcion": "Pechuga de pollo preparada a la plancha.",
        "ingredientes": ["pollo"]
    },

    "huevo_con_espinaca": {
        "nombre": "Huevo con espinaca",
        "descripcion": "Huevo acompañado de espinaca.",
        "ingredientes": ["huevo", "espinaca"]
    },

    "ensalada_de_atun_y_huevo": {
        "nombre": "Ensalada de atún y huevo",
        "descripcion": "Ensalada rica en proteínas.",
        "ingredientes": ["atun", "huevo"]
    },

    "pollo_con_brocoli": {
        "nombre": "Pollo con brócoli",
        "descripcion": "Pollo acompañado de brócoli.",
        "ingredientes": ["pollo", "brocoli"]
    },

    "yogur_con_avena": {
        "nombre": "Yogur con avena",
        "descripcion": "Yogur griego acompañado de avena.",
        "ingredientes": ["yogur_griego", "avena"]
    },

    "omelette_fitness": {
        "nombre": "Omelette fitness",
        "descripcion": "Omelette de huevo, espinaca y tomate.",
        "ingredientes": ["huevo", "espinaca", "tomate"]
    },

    "bowl_de_pollo": {
        "nombre": "Bowl de pollo",
        "descripcion": "Pollo acompañado de arroz y brócoli.",
        "ingredientes": ["pollo", "arroz", "brocoli"]
    },

    "pancakes_fitness": {
        "nombre": "Pancakes fitness",
        "descripcion": "Pancakes preparados con avena, huevo y banana.",
        "ingredientes": ["avena", "huevo", "banana"]
    },

    "ensalada_proteica": {
        "nombre": "Ensalada proteica",
        "descripcion": "Ensalada de pollo, lechuga y tomate.",
        "ingredientes": ["pollo", "lechuga", "tomate"]
    },

    "bowl_fitness_de_pollo": {
        "nombre": "Bowl fitness de pollo",
        "descripcion": "Bowl de pollo, arroz, brócoli y tomate.",
        "ingredientes": ["pollo", "arroz", "brocoli", "tomate"]
    },

    "bowl_de_atun_con_aguacate": {
        "nombre": "Bowl de atún con aguacate",
        "descripcion": "Atún acompañado de arroz, tomate y aguacate.",
        "ingredientes": ["atun", "arroz", "aguacate", "tomate"]
    },

    "ensalada_de_pollo": {
        "nombre": "Ensalada de pollo",
        "descripcion": "Ensalada fresca de pollo y vegetales.",
        "ingredientes": ["pollo", "lechuga", "tomate", "aguacate"]
    },

    "tostada_proteica": {
        "nombre": "Tostada proteica",
        "descripcion": "Pan integral con huevo, aguacate y tomate.",
        "ingredientes": ["pan_integral", "huevo", "aguacate", "tomate"]
    },

    "bowl_completo_de_pollo": {
        "nombre": "Bowl completo de pollo",
        "descripcion": "Bowl completo con pollo, arroz y vegetales.",
        "ingredientes": [
            "pollo",
            "arroz",
            "brocoli",
            "zanahoria",
            "aguacate"
        ]
    },

    "plato_fitness_de_pollo": {
        "nombre": "Plato fitness de pollo",
        "descripcion": "Pollo acompañado de camote y vegetales.",
        "ingredientes": [
            "pollo",
            "camote",
            "brocoli",
            "zanahoria",
            "aguacate"
        ]
    },

    "bowl_mexicano_de_pollo": {
        "nombre": "Bowl mexicano de pollo",
        "descripcion": "Bowl con pollo, arroz, frijoles, tomate, maíz y aguacate.",
        "ingredientes": [
            "pollo",
            "arroz",
            "frijoles",
            "tomate",
            "maiz",
            "aguacate"
        ]
    },

    "bowl_de_atun_y_huevo": {
        "nombre": "Bowl de atún y huevo",
        "descripcion": "Bowl de alto contenido proteico.",
        "ingredientes": [
            "atun",
            "huevo",
            "arroz",
            "tomate",
            "aguacate",
            "espinaca"
        ]
    }
}

# 4. MOTOR DE INFERENCIA

def motor_inferencia(ingredientes_usuario):

    recetas_encontradas = []

    for regla in REGLAS:

        condiciones = regla["if"]
        resultado = regla["then"][0]

        # Verificar si el usuario posee TODOS
        # los ingredientes de la regla
        if all(ingrediente in ingredientes_usuario
               for ingrediente in condiciones):

            if resultado not in recetas_encontradas:
                recetas_encontradas.append(resultado)

    return recetas_encontradas

# 5. CALCULO NUTRICIONAL

def calcular_nutricion(ingredientes):

    calorias = 0
    proteinas = 0

    for ingrediente in ingredientes:

        if ingrediente in INGREDIENTES:

            calorias += INGREDIENTES[ingrediente]["calorias"]
            proteinas += INGREDIENTES[ingrediente]["proteinas"]

    return calorias, proteinas


# 6. CAPTURA DE DATOS

def capturar_datos():

    print("\n======================================")
    print("          FITEXPERT")
    print("======================================")

    print("\nObjetivo:")
    print("1. Aumentar masa muscular")
    print("2. Perder grasa")
    print("3. Mantener peso")

    opcion = input("\nSeleccione su objetivo: ")

    objetivos = {
        "1": "aumentar masa muscular",
        "2": "perder grasa",
        "3": "mantener peso"
    }

    objetivo = objetivos.get(opcion, "mantener peso")

    print("\nIngredientes disponibles:")

    ingredientes = list(INGREDIENTES.keys())

    for i, ingrediente in enumerate(ingredientes, 1):
        print(f"{i}. {ingrediente}")

    entrada = input(
        "\nIngrese los números de los ingredientes "
        "separados por coma: "
    )

    seleccionados = []

    try:

        numeros = entrada.split(",")

        for numero in numeros:

            indice = int(numero.strip()) - 1

            if 0 <= indice < len(ingredientes):

                seleccionados.append(ingredientes[indice])

    except ValueError:

        print("Entrada inválida.")

    return objetivo, seleccionados

# 7. PRESENTACION DE RESULTADOS

def mostrar_resultados(objetivo, ingredientes, recetas):

    print("\n======================================")
    print("          RESULTADOS")
    print("======================================")

    print(f"\nObjetivo: {objetivo}")

    print("\nIngredientes ingresados:")

    for ingrediente in ingredientes:
        print(f"  - {ingrediente}")

    if not recetas:

        print("\nNo se encontraron recetas con esos ingredientes.")
        return

    print("\nRecetas recomendadas:")

    for receta_id in recetas:

        receta = RECETAS[receta_id]

        calorias, proteinas = calcular_nutricion(
            receta["ingredientes"]
        )

        print("\n--------------------------------------")
        print(f"🍽️ {receta['nombre']}")
        print(f"Descripción: {receta['descripcion']}")

        print("Ingredientes:")

        for ingrediente in receta["ingredientes"]:
            print(f"  - {ingrediente}")

        print(f"Calorías aproximadas: {calorias} kcal")
        print(f"Proteínas aproximadas: {proteinas:.1f} g")

# 8. PROGRAMA PRINCIPAL

def main():

    objetivo, ingredientes = capturar_datos()

    recetas = motor_inferencia(ingredientes)

    mostrar_resultados(
        objetivo,
        ingredientes,
        recetas
    )


# Ejecutar sistema
if __name__ == "__main__":
    main()
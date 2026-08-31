import unittest

import lab1


class BaseConocimientoTests(unittest.TestCase):
    def test_base_normalizada_y_consistente(self):
        self.assertEqual(len(lab1.INGREDIENTES), 27)
        self.assertEqual(len(lab1.RECETAS), 32)
        self.assertEqual(len(lab1.REGLAS), 32)

        for ingrediente_id, ingrediente in lab1.INGREDIENTES.items():
            self.assertEqual(ingrediente["id"], ingrediente_id)
            self.assertEqual(
                set(ingrediente["nutricion"]),
                {"calorias", "proteinas", "carbohidratos", "grasas"},
            )

        for regla in lab1.REGLAS:
            receta = lab1.RECETAS[regla["conclusion"]["receta_id"]]
            self.assertEqual(regla["condiciones"]["ingredientes"], receta["ingredientes"])
            self.assertEqual(regla["condiciones"]["tipo_comida"], receta["tipo_comida"])
            self.assertTrue(
                all(item in lab1.INGREDIENTES for item in receta["ingredientes"])
            )


class MotorInferenciaTests(unittest.TestCase):
    def test_umbral_es_estrictamente_mayor_a_cincuenta(self):
        coincidencia = lab1.calcular_coincidencia(
            ["manzana"], ["manzana", "almendras"]
        )
        self.assertEqual(coincidencia["porcentaje"], 50)

        resultado = lab1.recomendar_recetas(
            "mantener_peso", "snack", ["manzana"]
        )
        self.assertNotIn(
            "manzana_con_almendras",
            [receta["id"] for receta in resultado["recetas"]],
        )

    def test_resultados_se_ordenan_por_coincidencia(self):
        resultado = lab1.recomendar_recetas(
            "perder_grasa", "almuerzo", ["pollo", "arroz"]
        )
        porcentajes = [
            receta["coincidencia"]["porcentaje"] for receta in resultado["recetas"]
        ]
        self.assertEqual(porcentajes, sorted(porcentajes, reverse=True))
        self.assertEqual(resultado["recetas"][0]["id"], "pollo_a_la_plancha")
        self.assertEqual(resultado["recetas"][1]["coincidencia"]["porcentaje"], 66.67)

    def test_empate_se_resuelve_por_puntuacion_nutricional(self):
        resultado = lab1.recomendar_recetas(
            "perder_grasa", "almuerzo", ["pollo", "arroz", "brocoli"]
        )
        completos = [
            receta
            for receta in resultado["recetas"]
            if receta["coincidencia"]["porcentaje"] == 100
        ]
        puntuaciones = [receta["puntuacion_objetivo"] for receta in completos]
        self.assertEqual(puntuaciones, sorted(puntuaciones, reverse=True))
        self.assertEqual(completos[0]["id"], "bowl_de_pollo")

    def test_tipo_de_comida_filtra_reglas(self):
        resultado = lab1.recomendar_recetas(
            "mantener_peso",
            "cena",
            ["pollo", "arroz", "brocoli", "zanahoria", "quinoa"],
        )
        self.assertTrue(resultado["recetas"])
        self.assertTrue(
            all(receta["tipo_comida"]["id"] == "cena" for receta in resultado["recetas"])
        )

    def test_objetivos_generan_ordenes_nutricionales_distintos(self):
        ingredientes = list(lab1.INGREDIENTES)
        ordenes = {
            objetivo: [
                receta["id"]
                for receta in lab1.recomendar_recetas(
                    objetivo, "todos", ingredientes
                )["recetas"]
            ]
            for objetivo in lab1.OBJETIVOS
        }
        self.assertGreater(len({tuple(orden) for orden in ordenes.values()}), 1)


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = lab1.app.test_client()

    def test_consulta_valida(self):
        response = self.client.post(
            "/api/recomendar",
            json={
                "objetivo": "aumentar_masa_muscular",
                "tipo_comida": "desayuno",
                "ingredientes": ["avena", "huevo", "banana"],
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["recetas"])
        self.assertTrue(
            all(
                receta["coincidencia"]["porcentaje"] > data["umbral_coincidencia"]
                for receta in data["recetas"]
            )
        )

    def test_interfaz_incluye_segunda_categoria_y_base_extendida(self):
        response = self.client.get("/")
        contenido = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="tipo_comida"', contenido)
        self.assertIn("32</strong>", contenido)
        self.assertEqual(contenido.count('name="ingredientes"'), 27)

    def test_entradas_invalidas_devuelven_400(self):
        casos = [
            None,
            ["pollo"],
            {
                "objetivo": None,
                "tipo_comida": "almuerzo",
                "ingredientes": ["pollo"],
            },
            {
                "objetivo": "mantener_peso",
                "tipo_comida": "otro",
                "ingredientes": ["pollo"],
            },
            {
                "objetivo": "mantener_peso",
                "tipo_comida": "almuerzo",
                "ingredientes": [],
            },
            {
                "objetivo": "mantener_peso",
                "tipo_comida": "almuerzo",
                "ingredientes": [{}],
            },
            {
                "objetivo": "mantener_peso",
                "tipo_comida": "almuerzo",
                "ingredientes": ["desconocido"],
            },
        ]
        for payload in casos:
            with self.subTest(payload=payload):
                response = self.client.post("/api/recomendar", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertIn("detalles", response.get_json())

    def test_json_malformado_devuelve_400(self):
        response = self.client.post(
            "/api/recomendar", data="{", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_ingredientes_duplicados_se_normalizan(self):
        response = self.client.post(
            "/api/recomendar",
            json={
                "objetivo": "mantener_peso",
                "tipo_comida": "almuerzo",
                "ingredientes": ["pollo", "pollo"],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["totales"]["ingredientes"], 1)

    def test_health_reporta_base_cargada(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "status": "ok",
                "version": "2.0.0",
                "ingredientes": 27,
                "recetas": 32,
                "reglas": 32,
            },
        )


if __name__ == "__main__":
    unittest.main()

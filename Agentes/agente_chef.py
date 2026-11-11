
from rdflib import Graph, Namespace


class AgenteChef:

    def __init__(self, ruta_rdf):

        # Espacio de nombres de la ontología
        self.EX = Namespace(
            "http://www.Salud-AbleNutricion.com/ontologia#"
        )

        # Cargar almacenamiento RDF
        self.grafo = Graph()
        self.grafo.parse(ruta_rdf, format="turtle")

        # Porcentaje mínimo de coincidencia
        self.umbral = 75

        print("Agente Chef inicializado correctamente.")
        print("Triples cargados:", len(self.grafo))


    # -------------------------------------------------
    # 1. Consultar alimentos disponibles en el inventario
    # -------------------------------------------------

    def consultar_inventario(self):

        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?alimento
        WHERE {
            ?alimento a ex:Alimento ;
                      ex:tieneDisponibilidadInventario true .
        }
        """

        resultados = self.grafo.query(consulta)

        inventario = set()

        for fila in resultados:
            inventario.add(fila.alimento)

        return inventario


    # -------------------------------------------------
    # 2. Consultar recetas y alimentos que las componen
    # -------------------------------------------------

    def consultar_recetas(self):

        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?receta ?alimento
        WHERE {
            ?receta a ex:Receta ;
                    ex:compuestaPor ?alimento .
        }
        """

        resultados = self.grafo.query(consulta)

        recetas = {}

        for fila in resultados:

            id_receta = fila.receta
            id_alimento = fila.alimento

            if id_receta not in recetas:
                nombre = str(id_receta).split("#")[-1]

                recetas[id_receta] = {
                    "nombre": nombre,
                    "alimentos": set()
                }

            recetas[id_receta]["alimentos"].add(id_alimento)

        return recetas


    # -------------------------------------------------
    # 3. Evaluar coincidencia entre inventario y recetas
    # -------------------------------------------------

    def evaluar_recetas(self, inventario, recetas):

        recomendaciones = []

        for id_receta, datos in recetas.items():

            alimentos_requeridos = datos["alimentos"]

            if not alimentos_requeridos:
                continue

            # Alimentos de la receta que están disponibles
            coincidencias = alimentos_requeridos.intersection(inventario)

            # Alimentos que hacen falta
            faltantes = alimentos_requeridos.difference(inventario)

            # Calcular porcentaje de coincidencia
            porcentaje = (
                len(coincidencias) / len(alimentos_requeridos)
            ) * 100

            # Aplicar umbral mínimo del 75 %
            if porcentaje >= self.umbral:

                recomendaciones.append({
                    "nombre": datos["nombre"],
                    "porcentaje": round(porcentaje, 2),
                    "disponibles": [
                        str(a).split("#")[-1]
                        for a in coincidencias
                    ],
                    "faltantes": [
                        str(a).split("#")[-1]
                        for a in faltantes
                    ]
                })

        # Ordenar de mayor a menor coincidencia
        recomendaciones.sort(
            key=lambda x: x["porcentaje"],
            reverse=True
        )

        return recomendaciones


    # -------------------------------------------------
    # 4. Ejecutar el agente
    # -------------------------------------------------

    def ejecutar(self):

        print("\nConsultando inventario RDF...")

        inventario = self.consultar_inventario()

        print("Alimentos disponibles:", len(inventario))

        print("\nConsultando recetas RDF...")

        recetas = self.consultar_recetas()

        print("Recetas encontradas:", len(recetas))

        print("\nEvaluando recetas...")

        recomendaciones = self.evaluar_recetas(
            inventario,
            recetas
        )

        return recomendaciones


# -------------------------------------------------
# 5. Ejecución del agente
# -------------------------------------------------

if __name__ == "__main__":

    agente = AgenteChef("almacenamientoRDF/dataset_extendido.ttl")

    resultado = agente.ejecutar()

    print("\n========== RECOMENDACIONES DEL AGENTE CHEF ==========")

    if resultado:

        for receta in resultado:

            print(f"\nReceta: {receta['nombre']}")
            print(f"Coincidencia: {receta['porcentaje']}%")

            print(
                "Alimentos disponibles:",
                receta["disponibles"]
            )

            print(
                "Alimentos faltantes:",
                receta["faltantes"]
            )

    else:

        print("No se encontraron recetas que cumplan el 75%.")

from rdflib import Graph, Namespace, URIRef


class AgenteChef:

    def __init__(self, ruta_rdf):
        self.EX = Namespace("http://www.Salud-AbleNutricion.com/ontologia#")
        self.grafo = Graph()
        self.grafo.parse(ruta_rdf, format="turtle")
        self.grafo.bind("ex", self.EX)

    def obtener_uri(self, identificador):
        if isinstance(identificador, URIRef):
            return identificador
        identificador_str = str(identificador)
        if identificador_str.startswith(
            "http://"
        ) or identificador_str.startswith("https://"):
            return URIRef(identificador_str)
        return self.EX[identificador_str]

    def consultar_inventario_usuario(self, usuario):
        usuario_uri = self.obtener_uri(usuario)
        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?alimento
        WHERE {
            ?usuario ex:tieneEnInventario ?alimento .
        }
        """
        resultados = self.grafo.query(
            consulta, initBindings={"usuario": usuario_uri}
        )
        return {fila.alimento for fila in resultados}

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
            receta_id = fila.receta
            alimento_id = fila.alimento
            if receta_id not in recetas:
                recetas[receta_id] = {
                    "uri_receta": receta_id,
                    "nombre": str(receta_id).split("#")[-1],
                    "alimentos": set(),
                }
            recetas[receta_id]["alimentos"].add(alimento_id)
        return recetas

    def buscar_siguiente_receta(
        self,
        usuario,
        umbral,
        ingredientes_a_evitar=None,
        recetas_evaluadas=None,
    ):
        """El umbral es recibido explícitamente desde el Orquestador."""
        if ingredientes_a_evitar is None:
            ingredientes_a_evitar = set()
        if recetas_evaluadas is None:
            recetas_evaluadas = set()

        evitar_uris = {self.obtener_uri(i) for i in ingredientes_a_evitar}
        inventario = self.consultar_inventario_usuario(usuario)
        todas_recetas = self.consultar_recetas()

        candidatas = []

        for id_receta, datos in todas_recetas.items():
            if id_receta in recetas_evaluadas:
                continue

            alimentos_requeridos = datos["alimentos"]

            # Descartar si incluye ingredientes prohibidos por el Nutricionista
            if alimentos_requeridos.intersection(evitar_uris):
                continue

            coincidencias = alimentos_requeridos.intersection(inventario)
            faltantes = alimentos_requeridos.difference(inventario)
            porcentaje = (len(coincidencias) / len(alimentos_requeridos)) * 100

            # Aplicación del umbral que viene del Orquestador
            if porcentaje >= umbral:
                candidatas.append(
                    {
                        "uri_receta": id_receta,
                        "nombre": datos["nombre"],
                        "porcentaje": round(porcentaje, 2),
                        "disponibles": [
                            str(a).split("#")[-1] for a in coincidencias
                        ],
                        "faltantes": [
                            str(a).split("#")[-1] for a in faltantes
                        ],
                        "alimentos_uris": alimentos_requeridos,
                    }
                )

        candidatas.sort(key=lambda x: x["porcentaje"], reverse=True)
        return candidatas[0] if candidatas else None
from rdflib import Graph, Namespace, URIRef


class AgenteNutricionista:

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

    def consultar_condiciones_usuario(self, usuario):
        usuario_uri = self.obtener_uri(usuario)
        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?condicion ?componente
        WHERE {
            ?usuario ex:padece ?condicion .
            OPTIONAL { ?condicion ex:contraindica ?componente . }
        }
        """
        resultados = self.grafo.query(
            consulta, initBindings={"usuario": usuario_uri}
        )

        condiciones = {}
        contraindicaciones = set()

        for fila in resultados:
            c = fila.condicion
            comp = fila.componente
            if c not in condiciones:
                condiciones[c] = set()
            if comp:
                contraindicaciones.add(comp)
                condiciones[c].add(comp)

        return condiciones, contraindicaciones

    def evaluar_receta(self, receta_candidata, usuario):
        usuario_uri = self.obtener_uri(usuario)
        receta_uri = self.obtener_uri(receta_candidata["uri_receta"])

        condiciones, contraindicados = self.consultar_condiciones_usuario(
            usuario_uri
        )

        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?alimento ?componente
        WHERE {
            ?receta ex:compuestaPor ?alimento .
            ?alimento ex:contiene ?componente .
        }
        """
        resultados = self.grafo.query(
            consulta, initBindings={"receta": receta_uri}
        )

        alimentos_conflictivos = set()
        motivos = []

        for fila in resultados:
            alimento = fila.alimento
            componente = fila.componente

            if componente in contraindicados:
                alimentos_conflictivos.add(alimento)
                for cond, comps in condiciones.items():
                    if componente in comps:
                        motivos.append(
                            {
                                "alimento": str(alimento).split("#")[-1],
                                "componente": str(componente).split("#")[-1],
                                "condicion": str(cond).split("#")[-1],
                            }
                        )

        if alimentos_conflictivos:
            return {
                "apta": False,
                "receta": receta_candidata["nombre"],
                "motivos": motivos,
                "ingredientes_a_evitar": alimentos_conflictivos,  # Feedback para el Chef
            }
        else:
            return {"apta": True, "receta": receta_candidata}
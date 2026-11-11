
from rdflib import Graph, Namespace, URIRef


class AgenteNutricionista:

    def __init__(self, ruta_rdf):

        # Espacio de nombres de la ontología
        self.EX = Namespace(
            "http://www.Salud-AbleNutricion.com/ontologia#"
        )

        # Cargar almacenamiento RDF
        self.grafo = Graph()
        self.grafo.parse(ruta_rdf, format="turtle")

        print("Agente Nutricionista inicializado.")
        print("Triples cargados:", len(self.grafo))


    # -------------------------------------------------
    # 1. Resolver nombres o URI de usuarios y recetas
    # -------------------------------------------------

    def obtener_uri(self, identificador):

        identificador = str(identificador)

        if identificador.startswith("http://") or identificador.startswith("https://"):
            return URIRef(identificador)

        return self.EX[identificador]


    # -------------------------------------------------
    # 2. Consultar patologías y restricciones del usuario
    # -------------------------------------------------

    def consultar_condiciones_usuario(self, usuario):

        usuario_uri = self.obtener_uri(usuario)

        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?condicion ?componente
        WHERE {
            ?usuario ex:padece ?condicion .
            ?condicion ex:contraindica ?componente .
        }
        """

        resultados = self.grafo.query(
            consulta,
            initBindings={"usuario": usuario_uri}
        )

        componentes_contraindicados = set()

        condiciones = {}

        for fila in resultados:

            condicion = fila.condicion
            componente = fila.componente

            componentes_contraindicados.add(componente)

            if condicion not in condiciones:
                condiciones[condicion] = set()

            condiciones[condicion].add(componente)

        return condiciones, componentes_contraindicados


    # -------------------------------------------------
    # 3. Consultar los componentes de una receta
    # -------------------------------------------------

    def consultar_componentes_receta(self, receta):

        receta_uri = self.obtener_uri(receta)

        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?alimento ?componente
        WHERE {
            ?receta ex:compuestaPor ?alimento .

            ?alimento ex:contiene ?componente .
        }
        """

        resultados = self.grafo.query(
            consulta,
            initBindings={"receta": receta_uri}
        )

        componentes = set()

        for fila in resultados:
            componentes.add(fila.componente)

        return componentes


    # -------------------------------------------------
    # 4. Evaluar la seguridad de las recetas
    # -------------------------------------------------

    def evaluar_recetas(self, recetas, usuario):

        condiciones, contraindicados = (
            self.consultar_condiciones_usuario(usuario)
        )

        aptas = []
        no_aptas = []

        for receta in recetas:

            # El Chef entrega diccionarios con el nombre
            # de la receta. También se aceptan nombres o URI.
            if isinstance(receta, dict):
                nombre_receta = receta["nombre"]
            else:
                nombre_receta = str(receta)

            componentes = self.consultar_componentes_receta(
                nombre_receta
            )

            # No considerar segura una receta sin información
            if not componentes:
                no_aptas.append({
                    "receta": nombre_receta,
                    "motivo": "No se encontraron componentes en el RDF."
                })
                continue

            # Identificar componentes perjudiciales
            encontrados = componentes.intersection(
                contraindicados
            )

            if encontrados:

                motivos = []

                for condicion, componentes_condicion in condiciones.items():

                    afectados = encontrados.intersection(
                        componentes_condicion
                    )

                    for componente in afectados:

                        motivos.append({
                            "condicion": str(condicion).split("#")[-1],
                            "componente": str(componente).split("#")[-1]
                        })

                no_aptas.append({
                    "receta": nombre_receta,
                    "componentes_perjudiciales": [
                        str(c).split("#")[-1]
                        for c in encontrados
                    ],
                    "motivos": motivos
                })

            else:

                aptas.append({
                    "nombre": nombre_receta,
                    "estado": "Apta"
                })

        return {
            "aptas": aptas,
            "no_aptas": no_aptas
        }


    # -------------------------------------------------
    # 5. Ejecutar el agente
    # -------------------------------------------------

    def ejecutar(self, recetas_recomendadas, usuario):

        print("\nUsuario evaluado:", usuario)

        print("\nConsultando patologías y restricciones...")

        condiciones, componentes = (
            self.consultar_condiciones_usuario(usuario)
        )

        print("Condiciones encontradas:", len(condiciones))
        print("Componentes contraindicados:", len(componentes))

        print("\nEvaluando recetas recomendadas por Chef...")

        resultado = self.evaluar_recetas(
            recetas_recomendadas,
            usuario
        )

        return resultado


# -------------------------------------------------
# 6. Ejecución independiente del agente
# -------------------------------------------------

if __name__ == "__main__":

    agente = AgenteNutricionista("almacenamientoRDF/dataset_extendido.ttl")

    # Recetas que previamente recomendó el Agente Chef
    recetas_chef = [
        "Receta_Pollo_Quinoa",
        "Receta_Pollo_Soya"
    ]

    # Usuario para quien se evaluarán las recetas
    usuario = "Usuario_Carlos"

    resultado = agente.ejecutar(
        recetas_chef,
        usuario
    )

    print("\n========== RECETAS APTAS ==========")

    for receta in resultado["aptas"]:
        print(receta["nombre"])

    print("\n========== RECETAS NO APTAS ==========")

    for receta in resultado["no_aptas"]:

        print("\nReceta:", receta["receta"])

        if "componentes_perjudiciales" in receta:
            print(
                "Componentes perjudiciales:",
                receta["componentes_perjudiciales"]
            )

            print("Motivos:")

            for motivo in receta["motivos"]:
                print(
                    f" - {motivo['componente']} "
                    f"(Contraindicado por: {motivo['condicion']})"
                )

        else:
            print("Motivo:", receta["motivo"])

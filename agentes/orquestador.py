from agente_chef import AgenteChef
from agente_nutricionista import AgenteNutricionista


class OrquestadorNutricional:

    def __init__(self, ruta_rdf, umbral_coincidencia=60):
        self.ruta_rdf = ruta_rdf
        self.umbral_coincidencia = umbral_coincidencia
        # AgenteChef ya no requiere umbral al inicializarse
        self.chef = AgenteChef(ruta_rdf)
        self.nutricionista = AgenteNutricionista(ruta_rdf)

    def ejecutar_flujo(self, usuario_target, ingredientes_disponibles=None,
                       ingredientes_excluir=None, recetas_rechazadas=None,
                       umbral_faltantes_max=4):
        """
        Ejecuta el flujo multiagente Chef -> Nutricionista.

        Args:
            usuario_target: nombre del usuario en el RDF.
            ingredientes_disponibles: lista de nombres de alimentos disponibles
                (inventario efectivo). Si es None, se consulta el RDF del usuario.
            ingredientes_excluir: lista de nombres de alimentos a evitar.
            recetas_rechazadas: lista de URIs (strings) de recetas ya rechazadas.
            umbral_faltantes_max: máximo de ingredientes faltantes tolerados.
        Returns:
            dict de la receta aceptada o None si no existe.
        """
        if ingredientes_excluir is None:
            ingredientes_excluir = []
        if recetas_rechazadas is None:
            recetas_rechazadas = []

        # Inventario efectivo: se usa el proporcionado o se consulta al RDF
        if ingredientes_disponibles is None:
            inventario = {str(self.chef.obtener_uri(i)) for i in self.chef.consultar_inventario_usuario(usuario_target)}
        else:
            inventario = {str(self.chef.obtener_uri(i)) for i in ingredientes_disponibles}

        evitar_uris = {str(self.chef.obtener_uri(i)) for i in ingredientes_excluir}
        recetas_evaluadas = {str(r) for r in recetas_rechazadas}

        intento = 1

        while True:
            print(
                f"\n================================================================="
            )
            print(
                f" INICIANDO SISTEMA MULTIAGENTE DE NUTRICIÓN PARA: {usuario_target}"
            )
            print(
                f"================================================================="
            )

            print(
                f"\n--- [Iteración {intento}] El Agente Chef busca propuesta ---"
            )
            if evitar_uris:
                print(
                    f"  Ingredientes a evitar: "
                    f"{[str(i).split('#')[-1] for i in evitar_uris]}"
                )

            # El Orquestador obtiene todas las recetas y aplica los filtros
            todas_recetas = self.chef.consultar_recetas()
            candidatas = []

            for id_receta, datos in todas_recetas.items():
                id_receta_str = str(id_receta)
                if id_receta_str in recetas_evaluadas:
                    continue

                # Convertir alimentos_requeridos a strings para comparación consistente
                alimentos_requeridos = {str(a) for a in datos["alimentos"]}

                # Descartar recetas que contengan ingredientes excluidos
                if alimentos_requeridos.intersection(evitar_uris):
                    continue

                # Inventario ya es set de strings
                coincidencias = alimentos_requeridos.intersection(inventario)
                faltantes = alimentos_requeridos.difference(inventario)

                # Debe tener al menos un ingrediente en común con lo seleccionado
                if len(coincidencias) == 0:
                    continue

                # Umbral: máximo N ingredientes faltantes
                if len(faltantes) > umbral_faltantes_max:
                    continue

                porcentaje = (len(coincidencias) / len(alimentos_requeridos)) * 100

                candidatas.append(
                    {
                        "uri_receta": id_receta_str,
                        "nombre": id_receta_str.split("#")[-1],
                        "porcentaje": round(porcentaje, 2),
                        "disponibles": [
                            str(a).split("#")[-1] for a in coincidencias
                        ],
                        "faltantes": [
                            str(a).split("#")[-1] for a in faltantes
                        ],
                        "alimentos": [
                            str(a).split("#")[-1] for a in alimentos_requeridos
                        ],
                        "alimentos_uris": [
                            str(a) for a in alimentos_requeridos
                        ],
                    }
                )

            candidatas.sort(key=lambda x: x["porcentaje"], reverse=True)

            if not candidatas:
                print(
                    f"\n[SISTEMA] No se encontraron más recetas aptas."
                )
                return None

            receta_propuesta = candidatas[0]
            recetas_evaluadas.add(receta_propuesta["uri_receta"])

            print(
                f"  -> Chef propone: '{receta_propuesta['nombre']}' "
                f"(Coincidencia: {receta_propuesta['porcentaje']}%)"
            )

            # Nutricionista evalúa la propuesta
            print(
                f"--- [Iteración {intento}] El Agente Nutricionista evalúa la propuesta ---"
            )
            dictamen = self.nutricionista.evaluar_receta(
                receta_propuesta, usuario_target
            )

            if dictamen["apta"]:
                print(
                    f"  Nutricionista aprueba la receta '{receta_propuesta['nombre']}'."
                )
                print(f"\n=================================================")
                print(f"       MENÚ FINAL ACEPTADO Y RECOMENDADO        ")
                print(f"=================================================")
                print(f"Receta Aprobada: {receta_propuesta['nombre']}")
                print(f"Coincidencia:    {receta_propuesta['porcentaje']}%")
                print(
                    f"Ingredientes Disponibles: {receta_propuesta['disponibles']}"
                )
                print(
                    f"Ingredientes Faltantes:   {receta_propuesta['faltantes']}"
                )
                return receta_propuesta
            else:
                nuevos_evitar = dictamen["ingredientes_a_evitar"]
                # nuevo_evitar viene como set de URIRef de rdflib, convertir a strings
                evitar_uris.update({str(i) for i in nuevos_evitar})

                print(
                    f"  Nutricionista RECHAZA la receta '{dictamen['receta']}'"
                )
                for m in dictamen["motivos"]:
                    print(
                        f"     Motivo: Contiene {m['alimento']} "
                        f"({m['componente']}), contraindicado por {m['condicion']}."
                    )
                print(
                    "  Reenviando al Agente Chef con lista de rechazos..."
                )

            intento += 1


# -------------------------------------------------
# PUNTO ÚNICO DE CONFIGURACIÓN DEL UMBRAL
# -------------------------------------------------
if __name__ == "__main__":
    dataset = "almacenamientoRDF/instancias_inventario_usuario.ttl"

    orquestador = OrquestadorNutricional(dataset)
    orquestador.ejecutar_flujo("Usuario_Carlos")

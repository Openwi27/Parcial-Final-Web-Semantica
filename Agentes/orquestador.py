from agente_chef import AgenteChef
from agente_nutricionista import AgenteNutricionista


class OrquestadorNutricional:

    def __init__(self, ruta_rdf, umbral_coincidencia=60):
        self.ruta_rdf = ruta_rdf
        self.umbral_coincidencia = umbral_coincidencia
        # AgenteChef ya no requiere umbral al inicializarse
        self.chef = AgenteChef(ruta_rdf)
        self.nutricionista = AgenteNutricionista(ruta_rdf)

    def ejecutar_flujo(self, usuario_target):
        print(
            f"\n================================================================="
        )
        print(
            f" INICIANDO SISTEMA MULTIAGENTE DE NUTRICIÓN PARA: {usuario_target}"
        )
        print(
            f" UMBRAL MÍNIMO DE COINCIDENCIA: {self.umbral_coincidencia}%"
        )
        print(
            f"================================================================="
        )

        ingredientes_a_evitar = set()
        recetas_evaluadas = set()
        intento = 1

        while True:
            print(
                f"\n--- [Iteración {intento}] El Agente Chef busca propuesta ---"
            )
            if ingredientes_a_evitar:
                print(
                    f"  Ingredientes a evitar recibidos del Nutricionista: "
                    f"{[str(i).split('#')[-1] for i in ingredientes_a_evitar]}"
                )

            # El Orquestador le pasa la variable umbral_coincidencia directamente al Chef
            receta_propuesta = self.chef.buscar_siguiente_receta(
                usuario=usuario_target,
                umbral=self.umbral_coincidencia,
                ingredientes_a_evitar=ingredientes_a_evitar,
                recetas_evaluadas=recetas_evaluadas,
            )

            if not receta_propuesta:
                print(
                    f"\n[SISTEMA] No se encontraron más recetas aptas que superen el {self.umbral_coincidencia}% de coincidencia."
                )
                return None

            print(
                f"  -> Chef propone: '{receta_propuesta['nombre']}' "
                f"(Coincidencia Inventario: {receta_propuesta['porcentaje']}%)"
            )
            recetas_evaluadas.add(receta_propuesta["uri_receta"])

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
                ingredientes_a_evitar.update(nuevos_evitar)

                print(
                    f"  Nutricionista RECHAZA la receta '{dictamen['receta']}'"
                )
                for m in dictamen["motivos"]:
                    print(
                        f"     Motivo: Contiene {m['alimento']} ({m['componente']}), contraindicado por {m['condicion']}."
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

    #CAMBIA EL UMBRAL ÚNICO AQUÍ (ejemplo: 50, 60, 10, etc.)
    UMBRAL_SISTEMA = 50

    orquestador = OrquestadorNutricional(
        dataset, umbral_coincidencia=UMBRAL_SISTEMA
    )
    orquestador.ejecutar_flujo("Usuario_Carlos")
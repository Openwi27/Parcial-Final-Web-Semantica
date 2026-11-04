from owlready2 import *

# Crear la ontologia del sistema de dietas
onto = get_ontology(
    "http://www.Salud-AbleNutricion.com/ontologia#"
)

with onto:

    # Clases principales
    class Persona(Thing):
        pass

    class Usuario(Persona):
        pass

    class CondicionClinica(Thing):
        pass

    class Patologia(CondicionClinica):
        pass

    class RestriccionAlimentaria(CondicionClinica):
        pass

    class EntidadGastronomica(Thing):
        pass

    class Dieta(EntidadGastronomica):
        pass

    class Receta(EntidadGastronomica):
        pass

    class Alimento(EntidadGastronomica):
        pass

    class ComponenteQuimico(Thing):
        pass

    class Nutriente(ComponenteQuimico):
        pass

    class Alergeno(ComponenteQuimico):
        pass

    # Propiedades que relacionan las clases
    class padece(ObjectProperty):
        domain = [Usuario]
        range = [CondicionClinica]

    class contraindica(ObjectProperty):
        domain = [CondicionClinica]
        range = [Alimento | Alergeno]

    class recibe(ObjectProperty):
        domain = [Usuario]
        range = [Dieta]

    class incluye(ObjectProperty):
        domain = [Dieta]
        range = [Receta]

    class compuestaPor(ObjectProperty):
        domain = [Receta]
        range = [Alimento]

    class contiene(ObjectProperty):
        domain = [Alimento]
        range = [Nutriente | Alergeno]

    # Propiedades de datos
    class tieneDisponibilidadInventario(DataProperty):
        domain = [Alimento]
        range = [bool]

    class caloriasTotales(DataProperty):
        domain = [Dieta]
        range = [int]

    class nivelSeveridad(DataProperty):
        domain = [RestriccionAlimentaria]
        range = [str]

    # Restricciones de la ontologia
    AllDisjoint([CondicionClinica, EntidadGastronomica])

    Receta.is_a.append(compuestaPor.some(Alimento))

# Guardar la ontologia en formato OWL
onto.save(
    file="ontologia.owl",
    format="rdfxml"
)

print("Ontologia creada y guardada correctamente.")
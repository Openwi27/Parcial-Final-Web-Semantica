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
    class tieneEnInventario(ObjectProperty):
        domain = [Usuario]
        range = [Alimento]

    class caloriasTotales(DataProperty):
        domain = [Dieta]
        range = [int]

    class nivelSeveridad(DataProperty):
        domain = [RestriccionAlimentaria]
        range = [str]

    # 1. Propiedad Inversa
    class esIncluidaEn(ObjectProperty):
        domain = [Receta]
        range = [Dieta]
        inverse_property = incluye

    # 2. Propiedad Transitiva (Para inferir la composición en cadena)
    class tieneComponente(ObjectProperty, TransitiveProperty):
        domain = [EntidadGastronomica]
        range = [EntidadGastronomica | ComponenteQuimico]

    # Hacemos que compuestaPor y contiene sean subpropiedades de la transitiva
    # para que la inferencia fluya desde la Receta hasta el Alérgeno
    compuestaPor.is_a.append(tieneComponente)
    contiene.is_a.append(tieneComponente)

    # 3. Clase Equivalente / Restricción Universal
    class DietaSegura(Dieta):
        # En owlready2, .only() representa owl:allValuesFrom (Restricción universal ∀)
        # Esto se ajustará posteriormente con el reasoner dependiendo de los alérgenos, 
        # pero esta es la declaración estructural de la clase inferida.
        pass
    
    # Restricciones de la ontologia
    AllDisjoint([CondicionClinica, EntidadGastronomica])

    Receta.is_a.append(compuestaPor.some(Alimento))

# Guardar la ontologia en formato OWL
onto.save(
    file="ontologia.owl",
    format="rdfxml"
)

print("Ontologia creada y guardada correctamente.")
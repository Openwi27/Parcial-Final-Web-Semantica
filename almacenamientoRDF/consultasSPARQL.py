from rdflib import Graph, Namespace

# 1. Cargar el grafo RDF
g = Graph()
# Asegúrate de cargar el archivo .ttl correcto generado en el paso de almacenamiento
g.parse("almacenamientoRDF/dataset_extendido.ttl", format="turtle")

print("=== EJECUCIÓN DE CONSULTAS SPARQL ===\n")

# ---------------------------------------------------------
# Consulta 1: Identificación de contraindicaciones médicas
# ---------------------------------------------------------
print("--- Consulta 1: Elementos Contraindicados para Carlos ---")
q1 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?elementoContraindicado
    WHERE {
        ex:Usuario_Carlos ex:padece ?condicionClinica .
        ?condicionClinica ex:contraindica ?elementoContraindicado .
    }
"""
for row in g.query(q1):
    print(f"- Debe evitar: {row.elementoContraindicado.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 2: Verificación de ingredientes disponibles
# ---------------------------------------------------------
print("\n--- Consulta 2: Alimentos Disponibles en Inventario ---")
q2 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT ?alimento
    WHERE {
        ?alimento rdf:type ex:Alimento .
        ?alimento ex:tieneDisponibilidadInventario true .
    }
"""
for row in g.query(q2):
    print(f"- Disponible: {row.alimento.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 3: Generación de alternativas seguras
# ---------------------------------------------------------
print("\n--- Consulta 3: Recetas Seguras (Filtro de Inocuidad) ---")
q3 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?receta
    WHERE {
        ?receta rdf:type ex:Receta .

        FILTER NOT EXISTS {
            ?receta ex:compuestaPor ?alimento .
            ?alimento ex:contiene ?elemento .
            ex:Usuario_Carlos ex:padece ?condicionClinica .
            ?condicionClinica ex:contraindica ?elemento .
        }
    }
"""
for row in g.query(q3):
    print(f"- Receta apta: {row.receta.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 4: Alérgenos ocultos en una receta específica
# ---------------------------------------------------------
print("\n--- Consulta 4: Alérgenos en Receta Sandwich de Maní ---")
q4 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?alergeno
    WHERE {
        ex:Receta_Sandwich_Mani ex:compuestaPor ?alimento .
        ?alimento ex:contiene ?alergeno .
        ?alergeno rdf:type ex:Alergeno .
    }
"""
for row in g.query(q4):
    print(f"- Contiene alérgeno: {row.alergeno.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 5: Ingredientes agotados
# ---------------------------------------------------------
print("\n--- Consulta 5: Ingredientes Agotados (Falta Stock) ---")
q5 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT ?alimento
    WHERE {
        ?alimento rdf:type ex:Alimento .
        ?alimento ex:tieneDisponibilidadInventario false .
    }
"""
for row in g.query(q5):
    print(f"- Agotado: {row.alimento.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 6: Búsqueda de alimentos aptos y disponibles
# ---------------------------------------------------------
print("\n--- Consulta 6: Alimentos Disponibles y Aptos para Carlos ---")
q6 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT ?alimento
    WHERE {
        ?alimento rdf:type ex:Alimento .
        ?alimento ex:tieneDisponibilidadInventario true .

        FILTER NOT EXISTS {
            ?alimento ex:contiene ?elemento .
            ex:Usuario_Carlos ex:padece ?condicionClinica .
            ?condicionClinica ex:contraindica ?elemento .
        }
    }
"""
for row in g.query(q6):
    print(f"- Ideal para Chef: {row.alimento.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 7: Filtrado de dietas por límite calórico
# ---------------------------------------------------------
print("\n--- Consulta 7: Dietas menores o iguales a 2000 calorías ---")
q7 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT ?dieta ?calorias
    WHERE {
        ?dieta rdf:type ex:Dieta .
        ?dieta ex:caloriasTotales ?calorias .
        FILTER (?calorias <= 2000)
    }
"""
for row in g.query(q7):
    print(f"- {row.dieta.split('#')[-1]} ({row.calorias} kcal)")

# ---------------------------------------------------------
# Consulta 8: Búsqueda de alimentos por aporte nutricional
# ---------------------------------------------------------
print("\n--- Consulta 8: Alimentos que contienen Vitamina C ---")
q8 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?alimento
    WHERE {
        ?alimento rdf:type ex:Alimento .
        ?alimento ex:contiene ex:Vitamina_C .
    }
"""
for row in g.query(q8):
    print(f"- Fuente de Vitamina C: {row.alimento.split('#')[-1]}")

# ---------------------------------------------------------
# Consulta 9: Extracción del perfil clínico detallado
# ---------------------------------------------------------
print("\n--- Consulta 9: Severidad de las restricciones de Carlos ---")
q9 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?condicion ?severidad
    WHERE {
        ex:Usuario_Carlos ex:padece ?condicion .
        ?condicion rdf:type ex:RestriccionAlimentaria .
        OPTIONAL { ?condicion ex:nivelSeveridad ?severidad . }
    }
"""
for row in g.query(q9):
    print(f"- Condición: {row.condicion.split('#')[-1]} | Severidad: {row.severidad}")

# ---------------------------------------------------------
# Consulta 10: Trazabilidad de dietas asignadas
# ---------------------------------------------------------
print("\n--- Consulta 10: Dietas asignadas a Carlos y sus recetas ---")
q10 = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?dieta ?receta
    WHERE {
        ex:Usuario_Carlos ex:recibe ?dieta .
        ?dieta ex:incluye ?receta .
    }
"""
for row in g.query(q10):
    print(f"- Dieta: {row.dieta.split('#')[-1]} | Receta: {row.receta.split('#')[-1]}")

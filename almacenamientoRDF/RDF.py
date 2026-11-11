from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Inicialización del Grafo y el Espacio de Nombres
g = Graph()
ex = Namespace("http://www.Salud-AbleNutricion.com/ontologia#")
g.bind("ex", ex)

# ==========================================
# 1. CONDICIONES CLÍNICAS Y CONTRAINDICACIONES
# ==========================================
# Restricciones Alimentarias (Alergias e Intolerancias)
g.add((ex.Enfermedad_Celiaca, RDF.type, ex.RestriccionAlimentaria))
g.add((ex.Enfermedad_Celiaca, ex.nivelSeveridad, Literal("Alta", datatype=XSD.string)))
g.add((ex.Enfermedad_Celiaca, ex.contraindica, ex.Gluten))

g.add((ex.Alergia_Mani, RDF.type, ex.RestriccionAlimentaria))
g.add((ex.Alergia_Mani, ex.nivelSeveridad, Literal("Critica", datatype=XSD.string)))
g.add((ex.Alergia_Mani, ex.contraindica, ex.Mani))

# Patologías (Enfermedades)
g.add((ex.Diabetes_Mellitus, RDF.type, ex.Patologia))
g.add((ex.Diabetes_Mellitus, ex.contraindica, ex.Azucar_Refinada))

g.add((ex.Hipertension, RDF.type, ex.Patologia))
g.add((ex.Hipertension, ex.contraindica, ex.Sodio))

# ==========================================
# 2. PERFILES DE USUARIO (Casos de prueba)
# ==========================================
# Carlos: Múltiples condiciones (Diabetes + Celiaquía)
g.add((ex.Usuario_Carlos, RDF.type, ex.Usuario))
g.add((ex.Usuario_Carlos, ex.padece, ex.Diabetes_Mellitus))
g.add((ex.Usuario_Carlos, ex.padece, ex.Enfermedad_Celiaca))

# Maria: Alergia severa única
g.add((ex.Usuario_Maria, RDF.type, ex.Usuario))
g.add((ex.Usuario_Maria, ex.padece, ex.Alergia_Mani))

# Juan: Condición única (Hipertensión)
g.add((ex.Usuario_Juan, RDF.type, ex.Usuario))
g.add((ex.Usuario_Juan, ex.padece, ex.Hipertension))

# ==========================================
# 3. COMPONENTES QUÍMICOS
# ==========================================
# Alérgenos
for alergeno in [ex.Gluten, ex.Azucar_Refinada, ex.Mani, ex.Sodio]:
    g.add((alergeno, RDF.type, ex.Alergeno))

# Nutrientes beneficiosos
for nutriente in [ex.Vitamina_C, ex.Fibra, ex.Proteina]:
    g.add((nutriente, RDF.type, ex.Nutriente))

# ==========================================
# 4. ALIMENTOS E INVENTARIO
# ==========================================
# Caso A: Alimentos 100% seguros y disponibles
g.add((ex.Alimento_Quinoa, RDF.type, ex.Alimento))
g.add((ex.Alimento_Quinoa, ex.contiene, ex.Fibra))
g.add((ex.Alimento_Quinoa, ex.tieneDisponibilidadInventario, Literal(True, datatype=XSD.boolean)))

g.add((ex.Alimento_Tomate, RDF.type, ex.Alimento))
g.add((ex.Alimento_Tomate, ex.contiene, ex.Vitamina_C))
g.add((ex.Alimento_Tomate, ex.tieneDisponibilidadInventario, Literal(True, datatype=XSD.boolean)))

g.add((ex.Alimento_Pollo, RDF.type, ex.Alimento))
g.add((ex.Alimento_Pollo, ex.contiene, ex.Proteina))
g.add((ex.Alimento_Pollo, ex.tieneDisponibilidadInventario, Literal(True, datatype=XSD.boolean)))

# Caso B: Alimentos riesgosos pero DISPONIBLES en inventario
g.add((ex.Alimento_Pan_Trigo, RDF.type, ex.Alimento))
g.add((ex.Alimento_Pan_Trigo, ex.contiene, ex.Gluten))
g.add((ex.Alimento_Pan_Trigo, ex.tieneDisponibilidadInventario, Literal(True, datatype=XSD.boolean)))

g.add((ex.Alimento_Salsa_Soya, RDF.type, ex.Alimento))
g.add((ex.Alimento_Salsa_Soya, ex.contiene, ex.Sodio))
g.add((ex.Alimento_Salsa_Soya, ex.contiene, ex.Gluten)) # Doble riesgo
g.add((ex.Alimento_Salsa_Soya, ex.tieneDisponibilidadInventario, Literal(True, datatype=XSD.boolean)))

# Caso C: Alimentos riesgosos y AGOTADOS
g.add((ex.Alimento_Crema_Mani, RDF.type, ex.Alimento))
g.add((ex.Alimento_Crema_Mani, ex.contiene, ex.Mani))
g.add((ex.Alimento_Crema_Mani, ex.contiene, ex.Azucar_Refinada)) # Doble riesgo
g.add((ex.Alimento_Crema_Mani, ex.tieneDisponibilidadInventario, Literal(False, datatype=XSD.boolean)))

#===============
# 5. RECETAS (Combinatoria de Inocuidad)
# ==========================================
# Receta 1: Segura para todos (Solo ingredientes aptos)
g.add((ex.Receta_Pollo_Quinoa, RDF.type, ex.Receta))
g.add((ex.Receta_Pollo_Quinoa, ex.compuestaPor, ex.Alimento_Pollo))
g.add((ex.Receta_Pollo_Quinoa, ex.compuestaPor, ex.Alimento_Quinoa))
g.add((ex.Receta_Pollo_Quinoa, ex.compuestaPor, ex.Alimento_Tomate))

# Receta 2: Riesgo cruzado (Inocua para María, Letal para Carlos y Juan)
g.add((ex.Receta_Pollo_Soya, RDF.type, ex.Receta))
g.add((ex.Receta_Pollo_Soya, ex.compuestaPor, ex.Alimento_Pollo))
g.add((ex.Receta_Pollo_Soya, ex.compuestaPor, ex.Alimento_Salsa_Soya))

# Receta 3: Riesgo por alérgeno directo (Peligrosa para María y Carlos)
g.add((ex.Receta_Sandwich_Mani, RDF.type, ex.Receta))
g.add((ex.Receta_Sandwich_Mani, ex.compuestaPor, ex.Alimento_Pan_Trigo))
g.add((ex.Receta_Sandwich_Mani, ex.compuestaPor, ex.Alimento_Crema_Mani))

# ==========================================
# 6. ASIGNACIÓN DE DIETAS A USUARIOS
# ==========================================
# Dieta Carlos (Solo puede recibir Pollo con Quinoa)
g.add((ex.Dieta_Carlos_Lunes, RDF.type, ex.Dieta))
g.add((ex.Dieta_Carlos_Lunes, ex.caloriasTotales, Literal(1500, datatype=XSD.integer)))
g.add((ex.Dieta_Carlos_Lunes, ex.incluye, ex.Receta_Pollo_Quinoa))
g.add((ex.Usuario_Carlos, ex.recibe, ex.Dieta_Carlos_Lunes))

# Dieta Juan (No puede recibir Pollo con Soya por el Sodio)
g.add((ex.Dieta_Juan_Lunes, RDF.type, ex.Dieta))
g.add((ex.Dieta_Juan_Lunes, ex.caloriasTotales, Literal(1800, datatype=XSD.integer)))
g.add((ex.Dieta_Juan_Lunes, ex.incluye, ex.Receta_Pollo_Quinoa))
g.add((ex.Usuario_Juan, ex.recibe, ex.Dieta_Juan_Lunes))

# Dieta Maria (Evalúa si el chef falla al sugerir Crema de Maní)
g.add((ex.Dieta_Maria_Lunes, RDF.type, ex.Dieta))
g.add((ex.Dieta_Maria_Lunes, ex.caloriasTotales, Literal(2000, datatype=XSD.integer)))
g.add((ex.Dieta_Maria_Lunes, ex.incluye, ex.Receta_Sandwich_Mani)) # Riesgo intencional para prueba
g.add((ex.Usuario_Maria, ex.recibe, ex.Dieta_Maria_Lunes))

# ==========================================
# 7. EXPORTACIÓN
# ==========================================
g.serialize(destination="almacenamientoRDF/dataset_extendido.ttl", format="turtle")
g.serialize(destination="almacenamientoRDF/dataset_extendido.rdf", format="xml")

print("Grafo extendido generado: dataset_extendido.ttl y .rdf")
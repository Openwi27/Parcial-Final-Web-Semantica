from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, XSD

# 1. Inicialización del Grafo y Namespace
g = Graph()
ex = Namespace("http://www.Salud-AbleNutricion.com/ontologia#")
g.bind("ex", ex)

# ==========================================
# 2. DEFINICIÓN DE COMPONENTES (ALÉRGENOS Y NUTRIENTES)
# ==========================================
alergenos = [
    "Gluten",
    "Azucar_Refinada",
    "Mani",
    "Lactosa",
    "Mariscos",
    "Huevos",
    "Sodio",
    "Soya",
    "Frutos_Secos",
]

nutrientes = [
    "Vitamina_C",
    "Fibra",
    "Proteina",
    "Omega_3",
    "Calcio",
    "Hierro",
    "Potasio",
    "Vitamina_A",
]

for alg in alergenos:
    g.add((ex[alg], RDF.type, ex.Alergeno))

for nut in nutrientes:
    g.add((ex[nut], RDF.type, ex.Nutriente))

# ==========================================
# 3. CONDICIONES CLÍNICAS Y CONTRAINDICACIONES
# ==========================================
condiciones = {
    "Enfermedad_Celiaca": ("RestriccionAlimentaria", "Alta", "Gluten"),
    "Diabetes_Mellitus_Tipo_2": ("Patologia", "Alta", "Azucar_Refinada"),
    "Alergia_Mani": ("RestriccionAlimentaria", "Critica", "Mani"),
    "Intolerancia_Lactosa": ("RestriccionAlimentaria", "Media", "Lactosa"),
    "Alergia_Mariscos": ("RestriccionAlimentaria", "Critica", "Mariscos"),
    "Hipertension_Arterial": ("Patologia", "Alta", "Sodio"),
    "Alergia_Huevo": ("RestriccionAlimentaria", "Alta", "Huevos"),
}

for cond_name, (tipo, severidad, contraindica) in condiciones.items():
    cond_uri = ex[cond_name]
    g.add((cond_uri, RDF.type, ex[tipo]))
    g.add(
        (cond_uri, ex.nivelSeveridad, Literal(severidad, datatype=XSD.string))
    )
    g.add((cond_uri, ex.contraindica, ex[contraindica]))

# ==========================================
# 4. ALIMENTOS Y COMPOSICIÓN QUÍMICA
# ==========================================
alimentos_data = {
    "Alimento_Quinoa": ["Fibra", "Proteina", "Potasio"],
    "Alimento_Tomate": ["Vitamina_C", "Potasio"],
    "Alimento_Pollo": ["Proteina"],
    "Alimento_Pan_Trigo": ["Gluten"],
    "Alimento_Crema_Mani_Dulce": ["Mani", "Azucar_Refinada"],
    "Alimento_Leche_Vaca": ["Lactosa", "Calcio"],
    "Alimento_Queso_Fresco": ["Lactosa", "Calcio", "Proteina"],
    "Alimento_Huevo": ["Huevos", "Proteina"],
    "Alimento_Camaron": ["Mariscos", "Proteina"],
    "Alimento_Arroz": ["Fibra"],
    "Alimento_Espinaca": ["Hierro", "Vitamina_C", "Fibra"],
    "Alimento_Manzana": ["Fibra", "Vitamina_C"],
    "Alimento_Banano": ["Potasio", "Fibra"],
    "Alimento_Sal": ["Sodio"],
    "Alimento_Aceite_Oliva": [],
    "Alimento_Avena": ["Fibra", "Gluten"],
    "Alimento_Salmon": ["Omega_3", "Proteina"],
    "Alimento_Mantequilla": ["Lactosa"],
    "Alimento_Azucar": ["Azucar_Refinada"],
    "Alimento_Ajo": [],
    "Alimento_Cebolla": ["Fibra"],
    "Alimento_Pimenton": ["Vitamina_C"],
    "Alimento_Papa": ["Potasio"],
    "Alimento_Zanahoria": ["Vitamina_A", "Fibra"],
    "Alimento_Carne_Res": ["Proteina", "Hierro"],
    "Alimento_Pasta_Trigo": ["Gluten"],
    "Alimento_Lentejas": ["Proteina", "Hierro", "Fibra"],
    "Alimento_Garbanzos": ["Proteina", "Fibra"],
    "Alimento_Almendras": ["Frutos_Secos", "Calcio"],
    "Alimento_Soya": ["Soya", "Proteina"],
}

for alimento_name, componentes in alimentos_data.items():
    alim_uri = ex[alimento_name]
    g.add((alim_uri, RDF.type, ex.Alimento))
    for comp in componentes:
        g.add((alim_uri, ex.contiene, ex[comp]))

# ==========================================
# 5. USUARIOS, PATOLOGÍAS E INVENTARIO
# ==========================================
usuarios_data = {
    "Usuario_Carlos": {
        "padece": ["Diabetes_Mellitus_Tipo_2", "Enfermedad_Celiaca"],
        "inventario": [
            "Alimento_Quinoa",
            "Alimento_Tomate",
            "Alimento_Pan_Trigo",
            "Alimento_Espinaca",
            "Alimento_Arroz",
            "Alimento_Ajo",
            "Alimento_Aceite_Oliva",
        ],
    },
    "Usuario_Maria": {
        "padece": ["Alergia_Mani"],
        "inventario": [
            "Alimento_Pollo",
            "Alimento_Crema_Mani_Dulce",
            "Alimento_Arroz",
            "Alimento_Ajo",
            "Alimento_Cebolla",
            "Alimento_Tomate",
            "Alimento_Pimenton",
        ],
    },
    "Usuario_Juan": {
        "padece": ["Intolerancia_Lactosa", "Hipertension_Arterial"],
        "inventario": [
            "Alimento_Leche_Vaca",
            "Alimento_Queso_Fresco",
            "Alimento_Sal",
            "Alimento_Salmon",
            "Alimento_Espinaca",
            "Alimento_Aceite_Oliva",
            "Alimento_Papa",
        ],
    },
    "Usuario_Ana": {
        "padece": ["Alergia_Mariscos", "Alergia_Huevo"],
        "inventario": [
            "Alimento_Camaron",
            "Alimento_Huevo",
            "Alimento_Pasta_Trigo",
            "Alimento_Tomate",
            "Alimento_Carne_Res",
            "Alimento_Ajo",
            "Alimento_Cebolla",
        ],
    },
    "Usuario_Luis": {
        "padece": [],  # Usuario sin restricciones sanitarias
        "inventario": [
            "Alimento_Pan_Trigo",
            "Alimento_Mantequilla",
            "Alimento_Queso_Fresco",
            "Alimento_Pollo",
            "Alimento_Papa",
            "Alimento_Zanahoria",
            "Alimento_Arroz",
            "Alimento_Azucar",
        ],
    },
    "Usuario_Sofia": {
        "padece": ["Enfermedad_Celiaca", "Alergia_Mani"],
        "inventario": [
            "Alimento_Almendras",
            "Alimento_Quinoa",
            "Alimento_Espinaca",
            "Alimento_Manzana",
            "Alimento_Pollo",
            "Alimento_Aceite_Oliva",
        ],
    },
}

for user_name, datos in usuarios_data.items():
    user_uri = ex[user_name]
    g.add((user_uri, RDF.type, ex.Usuario))

    for pat in datos["padece"]:
        g.add((user_uri, ex.padece, ex[pat]))

    for inv in datos["inventario"]:
        g.add((user_uri, ex.tieneEnInventario, ex[inv]))

# ==========================================
# 6. BANCO DE 50 RECETAS
# ==========================================
recetas_data = {
    # Recetas 1 - 10
    "Receta_Ensalada_Quinoa": ["Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Sandwich_Tomate": ["Alimento_Pan_Trigo", "Alimento_Tomate", "Alimento_Queso_Fresco"],
    "Receta_Pollo_Tomate": ["Alimento_Pollo", "Alimento_Tomate", "Alimento_Ajo"],
    "Receta_Crema_Espinaca": ["Alimento_Espinaca", "Alimento_Leche_Vaca", "Alimento_Queso_Fresco"],
    "Receta_Sopa_Lentejas": ["Alimento_Lentejas", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Arroz_Con_Pollo": ["Alimento_Arroz", "Alimento_Pollo", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Salmon_Al_Horno": ["Alimento_Salmon", "Alimento_Aceite_Oliva", "Alimento_Ajo"],
    "Receta_Camaron_Al_Ajo": ["Alimento_Camaron", "Alimento_Ajo", "Alimento_Aceite_Oliva", "Alimento_Sal"],
    "Receta_Tortilla_Huevo_Espinaca": ["Alimento_Huevo", "Alimento_Espinaca", "Alimento_Aceite_Oliva"],
    "Receta_Pasta_Bolognesa": ["Alimento_Pasta_Trigo", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],

    # Recetas 11 - 20
    "Receta_Ensalada_Manzana_Almendras": ["Alimento_Manzana", "Alimento_Almendras", "Alimento_Espinaca"],
    "Receta_Avena_Con_Banano": ["Alimento_Avena", "Alimento_Banano", "Alimento_Leche_Vaca"],
    "Receta_Batido_Proteico_Mani": ["Alimento_Crema_Mani_Dulce", "Alimento_Banano", "Alimento_Leche_Vaca"],
    "Receta_Carne_Salteada_Pimenton": ["Alimento_Carne_Res", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pure_Papa": ["Alimento_Papa", "Alimento_Mantequilla", "Alimento_Leche_Vaca", "Alimento_Sal"],
    "Receta_Hummus_Garbanzo": ["Alimento_Garbanzos", "Alimento_Ajo", "Alimento_Aceite_Oliva", "Alimento_Sal"],
    "Receta_Pollo_Al_Ajo": ["Alimento_Pollo", "Alimento_Ajo", "Alimento_Aceite_Oliva", "Alimento_Sal"],
    "Receta_Arroz_Con_Camarones": ["Alimento_Arroz", "Alimento_Camaron", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Omelet_Queso": ["Alimento_Huevo", "Alimento_Queso_Fresco", "Alimento_Mantequilla"],
    "Receta_Sopa_Zanahoria": ["Alimento_Zanahoria", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Ajo"],

    # Recetas 21 - 30
    "Receta_Ensalada_Fresca": ["Alimento_Tomate", "Alimento_Espinaca", "Alimento_Queso_Fresco", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Con_Papa": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Pasta_Con_Camarones": ["Alimento_Pasta_Trigo", "Alimento_Camaron", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Pan_Con_Crema_Mani": ["Alimento_Pan_Trigo", "Alimento_Crema_Mani_Dulce"],
    "Receta_Salmon_Con_Quinoa": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Sopa_Garbanzos": ["Alimento_Garbanzos", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Cebolla"],
    "Receta_Lentejas_Con_Arroz": ["Alimento_Lentejas", "Alimento_Arroz", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Carne_Al_Horno_Papa": ["Alimento_Carne_Res", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Tostadas_Queso": ["Alimento_Pan_Trigo", "Alimento_Queso_Fresco", "Alimento_Mantequilla"],
    "Receta_Ensalada_Quinoa_Almendras": ["Alimento_Quinoa", "Alimento_Almendras", "Alimento_Manzana", "Alimento_Espinaca"],

    # Recetas 31 - 40
    "Receta_Huevo_Frito_Arroz": ["Alimento_Huevo", "Alimento_Arroz", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Pollo_Soya": ["Alimento_Pollo", "Alimento_Soya", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Crema_Zanahoria_Ajo": ["Alimento_Zanahoria", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Pure_Papa_Carne": ["Alimento_Papa", "Alimento_Carne_Res", "Alimento_Mantequilla"],
    "Receta_Pasta_Al_Ajo": ["Alimento_Pasta_Trigo", "Alimento_Ajo", "Alimento_Aceite_Oliva", "Alimento_Queso_Fresco"],
    "Receta_Camarones_Empanizados": ["Alimento_Camaron", "Alimento_Huevo", "Alimento_Pan_Trigo", "Alimento_Aceite_Oliva"],
    "Receta_Avena_Almendras": ["Alimento_Avena", "Alimento_Almendras", "Alimento_Banano"],
    "Receta_Pollo_Empanizado": ["Alimento_Pollo", "Alimento_Huevo", "Alimento_Pan_Trigo", "Alimento_Sal"],
    "Receta_Ensalada_Espinaca_Manzana": ["Alimento_Espinaca", "Alimento_Manzana", "Alimento_Aceite_Oliva"],
    "Receta_Sopa_Pollo_Verduras": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],

    # Recetas 41 - 50
    "Receta_Tofu_Salteado": ["Alimento_Soya", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Salmon_Con_Verduras": ["Alimento_Salmon", "Alimento_Pimenton", "Alimento_Zanahoria", "Alimento_Espinaca"],
    "Receta_Tortilla_Papa": ["Alimento_Huevo", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Aceite_Oliva"],
    "Receta_Sandwich_Pollo": ["Alimento_Pan_Trigo", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Espinaca"],
    "Receta_Postre_Banano_Mani": ["Alimento_Banano", "Alimento_Crema_Mani_Dulce"],
    "Receta_Arroz_Verduras": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Lentejas_Guisadas": ["Alimento_Lentejas", "Alimento_Papa", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Ensalada_Tomate_Cebolla": ["Alimento_Tomate", "Alimento_Cebolla", "Alimento_Aceite_Oliva", "Alimento_Sal"],
    "Receta_Quesadillas_Trigo": ["Alimento_Pan_Trigo", "Alimento_Queso_Fresco"],
    "Receta_Batido_Verde": ["Alimento_Espinaca", "Alimento_Manzana", "Alimento_Banano"],
}

for receta_name, ingredientes in recetas_data.items():
    receta_uri = ex[receta_name]
    g.add((receta_uri, RDF.type, ex.Receta))
    for ing in ingredientes:
        g.add((receta_uri, ex.compuestaPor, ex[ing]))

# ==========================================
# 7. ASIGNACIÓN DE DIETAS DE EJEMPLO
# ==========================================
g.add((ex.Dieta_Miercoles_Carlos, RDF.type, ex.Dieta))
g.add((ex.Dieta_Miercoles_Carlos, ex.caloriasTotales, Literal(1800, datatype=XSD.integer)))
g.add((ex.Dieta_Miercoles_Carlos, ex.incluye, ex.Receta_Ensalada_Quinoa))
g.add((ex.Usuario_Carlos, ex.recibe, ex.Dieta_Miercoles_Carlos))

# ==========================================
# 8. EXPORTACIÓN
# ==========================================
g.serialize(destination="almacenamientoRDF/instancias_inventario_usuario.ttl", format="turtle")
g.serialize(destination="almacenamientoRDF/instancias_inventario_usuario.rdf", format="xml")

print("Base de datos RDF generada con éxito.")
print(f"Total de triples cargados: {len(g)}")
print(f"Usuarios registrados: {len(usuarios_data)}")
print(f"Recetas cargadas: {len(recetas_data)}")
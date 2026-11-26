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
    "Pescado",
    "Sesamo",
    "Mostaza",
    "Sulfitos",
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
    "Zinc",
    "Magnesio",
    "Vitamina_D",
    "Folato",
    "Grasas_Saludables",
    "Carbohidratos_Complejos",
    "Antioxidantes",
    "Vitamina_B12",
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
    "Alergia_Soya": ("RestriccionAlimentaria", "Alta", "Soya"),
    "Alergia_Frutos_Secos": ("RestriccionAlimentaria", "Critica", "Frutos_Secos"),
    "Alergia_Pescado": ("RestriccionAlimentaria", "Critica", "Pescado"),
    "Alergia_Sesamo": ("RestriccionAlimentaria", "Media", "Sesamo"),
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
    # Vegetales
    "Alimento_Quinoa": ["Proteina", "Fibra", "Hierro", "Magnesio", "Carbohidratos_Complejos"],
    "Alimento_Tomate": ["Vitamina_C", "Potasio", "Antioxidantes"],
    "Alimento_Espinaca": ["Hierro", "Vitamina_C", "Fibra", "Folato", "Vitamina_A"],
    "Alimento_Arroz": ["Carbohidratos_Complejos", "Fibra"],
    "Alimento_Ajo": ["Vitamina_C", "Antioxidantes"],
    "Alimento_Aceite_Oliva": ["Grasas_Saludables"],
    "Alimento_Zanahoria": ["Vitamina_A", "Fibra", "Antioxidantes"],
    "Alimento_Cebolla": ["Fibra", "Vitamina_C", "Antioxidantes"],
    "Alimento_Pimenton": ["Vitamina_C", "Antioxidantes"],
    "Alimento_Papa": ["Potasio", "Fibra", "Vitamina_C"],
    "Alimento_Lechuga": ["Fibra", "Folato", "Vitamina_A"],
    "Alimento_Pepino": ["Fibra", "Vitamina_C", "Potasio"],
    "Alimento_Brocoli": ["Vitamina_C", "Fibra", "Folato", "Antioxidantes"],
    "Alimento_Coliflor": ["Vitamina_C", "Fibra", "Folato"],
    "Alimento_Calabacin": ["Fibra", "Vitamina_C", "Potasio"],
    "Alimento_Berenjena": ["Fibra", "Antioxidantes"],
    "Alimento_Repollo": ["Fibra", "Vitamina_C"],
    "Alimento_Apio": ["Fibra", "Potasio", "Antioxidantes"],
    "Alimento_Puerro": ["Fibra", "Vitamina_C"],
    "Alimento_Remolacha": ["Fibra", "Folato", "Potasio", "Antioxidantes"],
    "Alimento_Chauchas": ["Fibra", "Vitamina_C", "Hierro"],
    "Alimento_Arvejas": ["Proteina", "Fibra", "Carbohidratos_Complejos"],
    "Alimento_Choclo": ["Carbohidratos_Complejos", "Fibra"],
    "Alimento_Batata": ["Vitamina_A", "Fibra", "Potasio", "Carbohidratos_Complejos"],
    "Alimento_Calabaza": ["Vitamina_A", "Fibra", "Potasio"],
    "Alimento_Champinones": ["Vitamina_D", "Fibra", "Proteina"],
    "Alimento_Palta": ["Grasas_Saludables", "Fibra", "Potasio"],
    "Alimento_Limon": ["Vitamina_C", "Antioxidantes"],
    "Alimento_Naranja": ["Vitamina_C", "Fibra", "Antioxidantes"],
    "Alimento_Manzana": ["Fibra", "Vitamina_C", "Antioxidantes"],
    "Alimento_Banano": ["Potasio", "Fibra", "Carbohidratos_Complejos"],
    "Alimento_Pera": ["Fibra", "Vitamina_C"],
    "Alimento_Frutilla": ["Vitamina_C", "Antioxidantes", "Fibra"],
    "Alimento_Arandanos": ["Antioxidantes", "Vitamina_C", "Fibra"],
    "Alimento_Uvas": ["Antioxidantes", "Vitamina_C"],
    "Alimento_Durazno": ["Vitamina_C", "Fibra"],
    "Alimento_Mango": ["Vitamina_A", "Vitamina_C", "Fibra"],
    "Alimento_Kiwi": ["Vitamina_C", "Fibra", "Antioxidantes"],
    "Alimento_Sandia": ["Potasio", "Antioxidantes"],
    # Proteinas animales
    "Alimento_Pollo": ["Proteina", "Zinc"],
    "Alimento_Carne_Res": ["Proteina", "Hierro", "Zinc", "Vitamina_B12"],
    "Alimento_Carne_Cerdo": ["Proteina", "Zinc", "Vitamina_B12"],
    "Alimento_Pavo": ["Proteina", "Zinc"],
    "Alimento_Salmon": ["Omega_3", "Proteina", "Vitamina_D", "Vitamina_B12"],
    "Alimento_Atun": ["Proteina", "Omega_3", "Vitamina_B12"],
    "Alimento_Merluza": ["Proteina", "Vitamina_B12", "Pescado"],
    "Alimento_Camaron": ["Mariscos", "Proteina"],
    "Alimento_Huevo": ["Huevos", "Proteina"],
    # Proteinas vegetales / legumbres
    "Alimento_Lentejas": ["Proteina", "Hierro", "Fibra", "Folato", "Carbohidratos_Complejos"],
    "Alimento_Garbanzos": ["Proteina", "Fibra", "Hierro", "Folato", "Carbohidratos_Complejos"],
    "Alimento_Porotos_Negros": ["Proteina", "Fibra", "Hierro", "Carbohidratos_Complejos"],
    "Alimento_Tofu": ["Soya", "Proteina", "Calcio", "Hierro"],
    "Alimento_Amaranto": ["Proteina", "Fibra", "Hierro", "Carbohidratos_Complejos"],
    "Alimento_Semillas_Chia": ["Omega_3", "Fibra", "Proteina", "Calcio"],
    "Alimento_Semillas_Lino": ["Omega_3", "Fibra", "Grasas_Saludables"],
    "Alimento_Nueces": ["Frutos_Secos", "Omega_3", "Proteina", "Grasas_Saludables"],
    "Alimento_Almendras": ["Frutos_Secos", "Calcio", "Proteina", "Grasas_Saludables"],
    "Alimento_Avellanas": ["Frutos_Secos", "Grasas_Saludables", "Fibra"],
    "Alimento_Mantequilla_Mani": ["Mani", "Proteina", "Grasas_Saludables"],
    # Lacteos
    "Alimento_Leche_Vaca": ["Lactosa", "Calcio", "Proteina", "Vitamina_D"],
    "Alimento_Leche_Almendra": ["Calcio", "Grasas_Saludables"],
    "Alimento_Leche_Soya": ["Soya", "Proteina", "Calcio"],
    "Alimento_Yogur_Natural": ["Lactosa", "Calcio", "Proteina"],
    "Alimento_Queso_Fresco": ["Lactosa", "Calcio", "Proteina"],
    "Alimento_Queso_Duro": ["Lactosa", "Calcio", "Proteina"],
    "Alimento_Mantequilla": ["Lactosa", "Grasas_Saludables"],
    "Alimento_Crema_Leche": ["Lactosa", "Grasas_Saludables"],
    "Alimento_Crema_Mani_Dulce": ["Mani", "Azucar_Refinada", "Grasas_Saludables"],
    # Cereales / granos / harinas
    "Alimento_Pan_Trigo": ["Gluten"],
    "Alimento_Pan_Integral": ["Gluten", "Fibra", "Carbohidratos_Complejos"],
    "Alimento_Pasta_Trigo": ["Gluten", "Carbohidratos_Complejos"],
    "Alimento_Pasta_Sin_Gluten": ["Carbohidratos_Complejos", "Fibra"],
    "Alimento_Avena": ["Fibra", "Gluten", "Carbohidratos_Complejos"],
    "Alimento_Avena_Sin_Gluten": ["Fibra", "Carbohidratos_Complejos"],
    "Alimento_Arroz_Integral": ["Fibra", "Carbohidratos_Complejos"],
    "Alimento_Harina_Trigo": ["Gluten", "Carbohidratos_Complejos"],
    "Alimento_Harina_Maiz": ["Carbohidratos_Complejos"],
    "Alimento_Polenta": ["Carbohidratos_Complejos", "Fibra"],
    "Alimento_Cuscus": ["Gluten", "Carbohidratos_Complejos"],
    "Alimento_Tortilla_Maiz": ["Carbohidratos_Complejos", "Fibra"],
    "Alimento_Pan_Sin_Gluten": ["Carbohidratos_Complejos", "Fibra"],
    # Otros / condimentos / salsas
    "Alimento_Sal": ["Sodio"],
    "Alimento_Azucar": ["Azucar_Refinada"],
    "Alimento_Miel": ["Azucar_Refinada", "Antioxidantes"],
    "Alimento_Vinagre": ["Antioxidantes"],
    "Alimento_Salsa_Soya": ["Soya", "Sodio"],
    "Alimento_Caldo_Verdura": ["Sodio"],
    "Alimento_Levadura": ["Proteina", "Vitamina_B12"],
    "Alimento_Cacao": ["Antioxidantes", "Magnesio", "Grasas_Saludables"],
    "Alimento_Chocolate_Negro": ["Azucar_Refinada", "Antioxidantes", "Grasas_Saludables"],
    "Alimento_Coco": ["Grasas_Saludables", "Fibra"],
    "Alimento_Tahini": ["Sesamo", "Grasas_Saludables", "Proteina"],
    "Alimento_Mostaza": ["Mostaza", "Antioxidantes"],
    "Alimento_Mayonesa": ["Grasas_Saludables", "Huevos"],
    "Alimento_Pimienta": ["Antioxidantes"],
    "Alimento_Oregano": ["Antioxidantes"],
    "Alimento_Comino": ["Antioxidantes", "Hierro"],
    "Alimento_Canela": ["Antioxidantes"],
    "Alimento_Jengibre": ["Antioxidantes", "Vitamina_C"],
    "Alimento_Laurel": ["Antioxidantes"],
    "Alimento_Perejil": ["Vitamina_C", "Hierro", "Antioxidantes"],
    "Alimento_Albahaca": ["Antioxidantes", "Vitamina_C"],
}

# Limpieza: remover compuestos inválidos (None) por si acaso
alimentos_data = {
    k: [c for c in v if c is not None]
    for k, v in alimentos_data.items()
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
            "Alimento_Pollo",
            "Alimento_Zanahoria",
            "Alimento_Cebolla",
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
            "Alimento_Espinaca",
            "Alimento_Quinoa",
            "Alimento_Aceite_Oliva",
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
            "Alimento_Pollo",
            "Alimento_Arroz",
            "Alimento_Tomate",
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
            "Alimento_Pollo",
            "Alimento_Arroz",
            "Alimento_Papa",
        ],
    },
    "Usuario_Luis": {
        "padece": [],
        "inventario": [
            "Alimento_Pan_Trigo",
            "Alimento_Mantequilla",
            "Alimento_Queso_Fresco",
            "Alimento_Pollo",
            "Alimento_Papa",
            "Alimento_Zanahoria",
            "Alimento_Arroz",
            "Alimento_Azucar",
            "Alimento_Tomate",
            "Alimento_Cebolla",
            "Alimento_Ajo",
            "Alimento_Aceite_Oliva",
            "Alimento_Huevo",
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
            "Alimento_Tomate",
            "Alimento_Arroz",
            "Alimento_Ajo",
            "Alimento_Cebolla",
        ],
    },
    "Usuario_Pedro": {
        "padece": ["Alergia_Soya", "Hipertension_Arterial"],
        "inventario": [
            "Alimento_Tofu",
            "Alimento_Salsa_Soya",
            "Alimento_Sal",
            "Alimento_Arroz",
            "Alimento_Pollo",
            "Alimento_Tomate",
            "Alimento_Cebolla",
            "Alimento_Ajo",
            "Alimento_Aceite_Oliva",
            "Alimento_Papa",
        ],
    },
    "Usuario_Laura": {
        "padece": ["Alergia_Frutos_Secos", "Intolerancia_Lactosa"],
        "inventario": [
            "Alimento_Almendras",
            "Alimento_Nueces",
            "Alimento_Leche_Vaca",
            "Alimento_Queso_Fresco",
            "Alimento_Pollo",
            "Alimento_Arroz",
            "Alimento_Tomate",
            "Alimento_Cebolla",
            "Alimento_Ajo",
            "Alimento_Aceite_Oliva",
        ],
    },
    "Usuario_Andres": {
        "padece": ["Alergia_Pescado"],
        "inventario": [
            "Alimento_Salmon",
            "Alimento_Atun",
            "Alimento_Merluza",
            "Alimento_Arroz",
            "Alimento_Tomate",
            "Alimento_Cebolla",
            "Alimento_Ajo",
            "Alimento_Aceite_Oliva",
            "Alimento_Papa",
            "Alimento_Pimenton",
        ],
    },
    "Usuario_Camila": {
        "padece": ["Diabetes_Mellitus_Tipo_2", "Alergia_Huevo"],
        "inventario": [
            "Alimento_Azucar",
            "Alimento_Miel",
            "Alimento_Huevo",
            "Alimento_Pollo",
            "Alimento_Arroz",
            "Alimento_Tomate",
            "Alimento_Cebolla",
            "Alimento_Ajo",
            "Alimento_Aceite_Oliva",
            "Alimento_Quinoa",
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
# 6. BANCO DE RECETAS (ampliado)
# ==========================================
recetas_data = {
    # --- Recetas 1 - 10 ---
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
    # --- Recetas 11 - 20 ---
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
    # --- Recetas 21 - 30 ---
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
    # --- Recetas 31 - 40 ---
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
    # --- Recetas 41 - 50 ---
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
    # --- Recetas 51 - 60 (sin gluten) ---
    "Receta_Bowl_Quinoa_Pollo": ["Alimento_Quinoa", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Arroz_Frito_Verduras": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Huevo"],
    "Receta_Sopa_Quinoa": ["Alimento_Quinoa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pollo_Con_Arroz_Integral": ["Alimento_Pollo", "Alimento_Arroz_Integral", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Ensalada_Quinoa_Espinaca": ["Alimento_Quinoa", "Alimento_Espinaca", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Tortilla_Papa_Cebolla": ["Alimento_Huevo", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Aceite_Oliva"],
    "Receta_Pure_Batata": ["Alimento_Batata", "Alimento_Mantequilla", "Alimento_Leche_Vaca", "Alimento_Sal"],
    "Receta_Polenta_Con_Pollo": ["Alimento_Polenta", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Tortilla_Maiz_Queso": ["Alimento_Tortilla_Maiz", "Alimento_Queso_Fresco", "Alimento_Pimenton"],
    "Receta_Pan_Sin_Gluten_Tomate": ["Alimento_Pan_Sin_Gluten", "Alimento_Tomate", "Alimento_Queso_Fresco"],
    # --- Recetas 61 - 70 (sin lactosa) ---
    "Receta_Pollo_Arroz_Lactosa_Free": ["Alimento_Pollo", "Alimento_Arroz", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Salmon_Quinoa_Lactosa_Free": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Ensalada_Verduras_Aceite": ["Alimento_Tomate", "Alimento_Espinaca", "Alimento_Pepino", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Con_Batata": ["Alimento_Pollo", "Alimento_Batata", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Arroz_Con_Verduras_Lactosa_Free": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Lentejas_Guisadas_Lactosa_Free": ["Alimento_Lentejas", "Alimento_Papa", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Sopa_Zanahoria_Lactosa_Free": ["Alimento_Zanahoria", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Ensalada_Quinoa_Almendras_Lactosa_Free": ["Alimento_Quinoa", "Alimento_Almendras", "Alimento_Manzana", "Alimento_Espinaca"],
    "Receta_Pasta_Sin_Gluten_Carne": ["Alimento_Pasta_Sin_Gluten", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pollo_Con_Verduras_Lactosa_Free": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    # --- Recetas 71 - 80 (bajo sodio / hipertension) ---
    "Receta_Pollo_Aceite_Oliva_Sin_Sal": ["Alimento_Pollo", "Alimento_Aceite_Oliva", "Alimento_Ajo", "Alimento_Pimenton"],
    "Receta_Salmon_Quinoa_Sin_Sal": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Ensalada_Verduras_Sin_Sal": ["Alimento_Tomate", "Alimento_Espinaca", "Alimento_Pepino", "Alimento_Aceite_Oliva"],
    "Receta_Arroz_Con_Pollo_Sin_Sal": ["Alimento_Arroz", "Alimento_Pollo", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pollo_Con_Papa_Sin_Sal": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Sopa_Pollo_Verduras_Sin_Sal": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Lentejas_Guisadas_Sin_Sal": ["Alimento_Lentejas", "Alimento_Papa", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Ensalada_Quinoa_Sin_Sal": ["Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Salmon_Con_Verduras_Sin_Sal": ["Alimento_Salmon", "Alimento_Pimenton", "Alimento_Zanahoria", "Alimento_Espinaca"],
    "Receta_Pollo_Con_Batata_Sin_Sal": ["Alimento_Pollo", "Alimento_Batata", "Alimento_Zanahoria", "Alimento_Ajo"],
    # --- Recetas 81 - 90 (sin huevo / sin mariscos) ---
    "Receta_Pollo_Arroz_Sin_Huevo": ["Alimento_Pollo", "Alimento_Arroz", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Carne_Con_Papa_Sin_Huevo": ["Alimento_Carne_Res", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pasta_Carne_Sin_Huevo": ["Alimento_Pasta_Trigo", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pollo_Con_Verduras_Sin_Huevo": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Ensalada_Quinoa_Sin_Huevo": ["Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Arroz_Con_Verduras_Sin_Mariscos": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Pollo_Tomate_Sin_Mariscos": ["Alimento_Pollo", "Alimento_Tomate", "Alimento_Ajo"],
    "Receta_Pasta_Bolognesa_Sin_Mariscos": ["Alimento_Pasta_Trigo", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Ensalada_Fresca_Sin_Mariscos": ["Alimento_Tomate", "Alimento_Espinaca", "Alimento_Queso_Fresco", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Con_Papa_Sin_Mariscos": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Ajo"],
    # --- Recetas 91 - 100 (sin soya) ---
    "Receta_Pollo_Arroz_Sin_Soya": ["Alimento_Pollo", "Alimento_Arroz", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Salmon_Quinoa_Sin_Soya": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Ensalada_Quinoa_Sin_Soya": ["Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Con_Papa_Sin_Soya": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Arroz_Con_Verduras_Sin_Soya": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Lentejas_Guisadas_Sin_Soya": ["Alimento_Lentejas", "Alimento_Papa", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Pasta_Carne_Sin_Soya": ["Alimento_Pasta_Trigo", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Ensalada_Fresca_Sin_Soya": ["Alimento_Tomate", "Alimento_Espinaca", "Alimento_Queso_Fresco", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Tomate_Sin_Soya": ["Alimento_Pollo", "Alimento_Tomate", "Alimento_Ajo"],
    "Receta_Salmon_Con_Verduras_Sin_Soya": ["Alimento_Salmon", "Alimento_Pimenton", "Alimento_Zanahoria", "Alimento_Espinaca"],
    # --- Recetas 101 - 110 (sin frutos secos) ---
    "Receta_Ensalada_Quinoa_Sin_Frutos_Secos": ["Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Espinaca_Manzana_Sin_Frutos_Secos": ["Alimento_Espinaca", "Alimento_Manzana", "Alimento_Aceite_Oliva"],
    "Receta_Avena_Banano_Sin_Frutos_Secos": ["Alimento_Avena", "Alimento_Banano", "Alimento_Leche_Vaca"],
    "Receta_Pollo_Arroz_Sin_Frutos_Secos": ["Alimento_Pollo", "Alimento_Arroz", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Salmon_Quinoa_Sin_Frutos_Secos": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Ensalada_Fresca_Sin_Frutos_Secos": ["Alimento_Tomate", "Alimento_Espinaca", "Alimento_Queso_Fresco", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Con_Papa_Sin_Frutos_Secos": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Arroz_Con_Verduras_Sin_Frutos_Secos": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Lentejas_Guisadas_Sin_Frutos_Secos": ["Alimento_Lentejas", "Alimento_Papa", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Pasta_Carne_Sin_Frutos_Secos": ["Alimento_Pasta_Trigo", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    # --- Recetas 111 - 120 (combinadas: sin gluten + sin lactosa) ---
    "Receta_Bowl_Quinoa_Pollo_Sin_Lactosa": ["Alimento_Quinoa", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Arroz_Frito_Verduras_Sin_Lactosa": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Huevo"],
    "Receta_Polenta_Con_Pollo_Sin_Lactosa": ["Alimento_Polenta", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Cebolla"],
    "Receta_Tortilla_Maiz_Queso_Sin_Lactosa": ["Alimento_Tortilla_Maiz", "Alimento_Queso_Fresco", "Alimento_Pimenton"],
    "Receta_Pan_Sin_Gluten_Tomate_Sin_Lactosa": ["Alimento_Pan_Sin_Gluten", "Alimento_Tomate", "Alimento_Queso_Fresco"],
    "Receta_Pasta_Sin_Gluten_Carne_Sin_Lactosa": ["Alimento_Pasta_Sin_Gluten", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Ensalada_Quinoa_Sin_Lactosa": ["Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Salmon_Quinoa_Sin_Lactosa": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Pollo_Con_Batata_Sin_Lactosa": ["Alimento_Pollo", "Alimento_Batata", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Arroz_Con_Verduras_Sin_Lactosa": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    # --- Recetas 121 - 130 (ensaladas variadas) ---
    "Receta_Ensalada_Tomate_Pepino": ["Alimento_Tomate", "Alimento_Pepino", "Alimento_Aceite_Oliva", "Alimento_Limon"],
    "Receta_Ensalada_Espinaca_Frutilla": ["Alimento_Espinaca", "Alimento_Frutilla", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Quinoa_Mango": ["Alimento_Quinoa", "Alimento_Mango", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Pollo_Manzana": ["Alimento_Pollo", "Alimento_Manzana", "Alimento_Espinaca", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Arroz_Verduras": ["Alimento_Arroz", "Alimento_Pepino", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Lentejas_Tomate": ["Alimento_Lentejas", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Garbanzos_Pimenton": ["Alimento_Garbanzos", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Pollo_Quinoa": ["Alimento_Pollo", "Alimento_Quinoa", "Alimento_Tomate", "Alimento_Aceite_Oliva"],
    "Receta_Ensalada_Salmon_Espinaca": ["Alimento_Salmon", "Alimento_Espinaca", "Alimento_Aceite_Oliva", "Alimento_Limon"],
    "Receta_Ensalada_Carne_Res_Tomate": ["Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Aceite_Oliva"],
    # --- Recetas 131 - 140 (sopas / cremas) ---
    "Receta_Sopa_Tomate": ["Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Crema_Brocoli": ["Alimento_Brocoli", "Alimento_Leche_Vaca", "Alimento_Queso_Fresco"],
    "Receta_Sopa_Pollo_Arroz": ["Alimento_Pollo", "Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Crema_Calabaza": ["Alimento_Calabaza", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Sopa_Lentejas_Arroz": ["Alimento_Lentejas", "Alimento_Arroz", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Crema_Espinaca_Sin_Lactosa": ["Alimento_Espinaca", "Alimento_Aceite_Oliva", "Alimento_Ajo", "Alimento_Cebolla"],
    "Receta_Sopa_Garbanzos_Arroz": ["Alimento_Garbanzos", "Alimento_Arroz", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Sopa_Pollo_Quinoa": ["Alimento_Pollo", "Alimento_Quinoa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Crema_Zanahoria_Coco": ["Alimento_Zanahoria", "Alimento_Coco", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Sopa_Verduras_Mixtas": ["Alimento_Zanahoria", "Alimento_Papa", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    # --- Recetas 141 - 150 (postres / desayunos) ---
    "Receta_Batido_Banano_Avena": ["Alimento_Banano", "Alimento_Avena", "Alimento_Leche_Vaca"],
    "Receta_Batido_Verde_Manzana": ["Alimento_Espinaca", "Alimento_Manzana", "Alimento_Banano"],
    "Receta_Panqueques_Avena": ["Alimento_Avena", "Alimento_Huevo", "Alimento_Leche_Vaca"],
    "Receta_Panqueques_Sin_Gluten": ["Alimento_Avena_Sin_Gluten", "Alimento_Huevo", "Alimento_Leche_Almendra"],
    "Receta_Yogur_Con_Frutilla": ["Alimento_Yogur_Natural", "Alimento_Frutilla"],
    "Receta_Avena_Con_Manzana": ["Alimento_Avena", "Alimento_Manzana", "Alimento_Leche_Vaca"],
    "Receta_Pudin_Chia": ["Alimento_Semillas_Chia", "Alimento_Leche_Almendra", "Alimento_Miel"],
    "Receta_Batido_Proteico_Pollo": ["Alimento_Pollo", "Alimento_Banano", "Alimento_Leche_Vaca"],
    "Receta_Tostadas_Pan_Sin_Gluten_Miel": ["Alimento_Pan_Sin_Gluten", "Alimento_Miel"],
    "Receta_Postre_Banano_Cacao": ["Alimento_Banano", "Alimento_Cacao", "Alimento_Leche_Vaca"],
    # --- Recetas 151 - 160 (salteados / salteados) ---
    "Receta_Salteado_Pollo_Verduras": ["Alimento_Pollo", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Carne_Verduras": ["Alimento_Carne_Res", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Tofu_Verduras": ["Alimento_Tofu", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Pollo_Brocoli": ["Alimento_Pollo", "Alimento_Brocoli", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Carne_Brocoli": ["Alimento_Carne_Res", "Alimento_Brocoli", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Pollo_Calabacin": ["Alimento_Pollo", "Alimento_Calabacin", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Carne_Pimenton": ["Alimento_Carne_Res", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Pollo_Chauchas": ["Alimento_Pollo", "Alimento_Chauchas", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Carne_Chauchas": ["Alimento_Carne_Res", "Alimento_Chauchas", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salteado_Pollo_Berenjena": ["Alimento_Pollo", "Alimento_Berenjena", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    # --- Recetas 161 - 170 (al horno) ---
    "Receta_Pollo_Al_Horno_Papa": ["Alimento_Pollo", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Ajo"],
    "Receta_Carne_Al_Horno_Papa_Zanahoria": ["Alimento_Carne_Res", "Alimento_Papa", "Alimento_Zanahoria", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Salmon_Al_Horno_Verduras": ["Alimento_Salmon", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Al_Horno_Batata": ["Alimento_Pollo", "Alimento_Batata", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Carne_Al_Horno_Batata": ["Alimento_Carne_Res", "Alimento_Batata", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Pollo_Al_Horno_Calabaza": ["Alimento_Pollo", "Alimento_Calabaza", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Salmon_Al_Horno_Quinoa": ["Alimento_Salmon", "Alimento_Quinoa", "Alimento_Espinaca"],
    "Receta_Pollo_Al_Horno_Tomate": ["Alimento_Pollo", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Carne_Al_Horno_Tomate": ["Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    "Receta_Pollo_Al_Horno_Pimenton": ["Alimento_Pollo", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
    # --- Recetas 171 - 180 (arroz / granos) ---
    "Receta_Arroz_Con_Pollo_Verduras": ["Alimento_Arroz", "Alimento_Pollo", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Arroz_Con_Carne": ["Alimento_Arroz", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Arroz_Con_Verduras_Mixtas": ["Alimento_Arroz", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Arvejas"],
    "Receta_Quinoa_Con_Pollo": ["Alimento_Quinoa", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Quinoa_Con_Verduras": ["Alimento_Quinoa", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla", "Alimento_Aceite_Oliva"],
    "Receta_Amaranto_Con_Pollo": ["Alimento_Amaranto", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Arroz_Integral_Con_Verduras": ["Alimento_Arroz_Integral", "Alimento_Zanahoria", "Alimento_Pimenton", "Alimento_Cebolla"],
    "Receta_Polenta_Con_Carne": ["Alimento_Polenta", "Alimento_Carne_Res", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Cuscus_Con_Pollo": ["Alimento_Cuscus", "Alimento_Pollo", "Alimento_Tomate", "Alimento_Cebolla", "Alimento_Ajo"],
    "Receta_Arroz_Con_Garbanzos": ["Alimento_Arroz", "Alimento_Garbanzos", "Alimento_Cebolla", "Alimento_Ajo", "Alimento_Aceite_Oliva"],
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
g.serialize(destination="almacenamientoRDF\instancias_inventario_usuario.ttl", format="turtle")
g.serialize(destination="almacenamientoRDF\instancias_inventario_usuario.rdf", format="xml")

print("Base de datos RDF generada con éxito.")
print(f"Total de triples cargados: {len(g)}")
print(f"Usuarios registrados: {len(usuarios_data)}")
print(f"Recetas cargadas: {len(recetas_data)}")
print(f"Alimentos registrados: {len(alimentos_data)}")

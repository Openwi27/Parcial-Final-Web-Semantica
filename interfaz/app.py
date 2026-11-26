import os
import re
import shutil
import sys
import threading

# ---------------------------------------------------------------
# Ruta a los agentes existentes (no se modifica su lógica)
# ---------------------------------------------------------------
AGENTES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agentes')
if AGENTES_DIR not in sys.path:
    sys.path.insert(0, AGENTES_DIR)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from rdflib import Graph, Literal, Namespace, URIRef, RDF
from rdflib.namespace import XSD

from orquestador import OrquestadorNutricional

app = Flask(__name__)
app.secret_key = 'clave-secreta-sistema-dietas'

# ---------------------------------------------------------------
# Rutas a los archivos de datos (se respetan los existentes)
# ---------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RDF_DIR = os.path.join(BASE_DIR, 'almacenamientoRDF')
RDF_TTL = os.path.join(RDF_DIR, 'instancias_inventario_usuario.ttl')
RDF_RDF = os.path.join(RDF_DIR, 'instancias_inventario_usuario.rdf')

EX = Namespace("http://www.Salud-AbleNutricion.com/ontologia#")
EX_STR = "http://www.Salud-AbleNutricion.com/ontologia#"

def limpiar_nombre(nombre_completo):
    """Quita prefijos RDF y formatea el nombre para mostrar al usuario."""
    nombre = str(nombre_completo)
    # Si es una URI completa, extraer la parte después de #
    if '#' in nombre:
        nombre = nombre.split('#')[-1]
    for prefijo in ["Alimento_", "Usuario_", "Receta_"]:
        if nombre.startswith(prefijo):
            nombre = nombre[len(prefijo):]
            break
    nombre = nombre.replace("_", " ")
    return " ".join(p.capitalize() for p in nombre.split() if p)


# ---------------------------------------------------------------
# Helpers de consulta sobre el grafo RDF
# ---------------------------------------------------------------
def cargar_grafo():
    g = Graph()
    g.parse(RDF_TTL, format="turtle")
    return g


# ---------------------------------------------------------------
# Escritura segura del almacén RDF
# ---------------------------------------------------------------
class ErrorRDF(Exception):
    """Error controlado al leer o escribir el almacén RDF."""


# Serializa las peticiones de escritura: evita que dos POST simultáneos
# lean y escriban el archivo a la vez (lo que corrompería el .ttl).
_RDF_LOCK = threading.Lock()


def cargar_grafo_estricto():
    """Carga el grafo existente sin tolerar fallos.

    Si el archivo no se puede leer se lanza ErrorRDF: es preferible no guardar
    nada antes que escribir un grafo vacío encima de los datos existentes.
    """
    if not os.path.exists(RDF_TTL):
        raise ErrorRDF(f'No se encontró el archivo de datos {os.path.basename(RDF_TTL)}.')

    g = Graph()
    try:
        g.parse(RDF_TTL, format="turtle")
    except Exception as exc:
        raise ErrorRDF(
            f'No se pudo leer {os.path.basename(RDF_TTL)} ({type(exc).__name__}). '
            'No se modificó ningún dato.'
        ) from exc

    if len(g) == 0:
        raise ErrorRDF(
            'El archivo de datos RDF está vacío. Se canceló la escritura para no perder información.'
        )
    return g


def guardar_grafo_atomico(g):
    """Escribe el grafo en disco de forma atómica.

    Primero se serializa a un archivo temporal y solo si eso funciona se
    reemplaza el original. Si algo falla, los archivos anteriores quedan
    intactos y además se conserva una copia .bak del estado previo.
    """
    for destino, formato in ((RDF_TTL, "turtle"), (RDF_RDF, "xml")):
        temporal = destino + ".tmp"
        try:
            g.serialize(destination=temporal, format=formato)
            if os.path.exists(destino):
                shutil.copy2(destino, destino + ".bak")
            os.replace(temporal, destino)
        except Exception as exc:
            if os.path.exists(temporal):
                try:
                    os.remove(temporal)
                except OSError:
                    pass
            raise ErrorRDF(
                f'No se pudo escribir {os.path.basename(destino)} ({type(exc).__name__}). '
                'Los datos anteriores quedaron intactos.'
            ) from exc


def normalizar_nombre(valor, prefijo=None):
    """Limpia el nombre escrito por el usuario y evita prefijos duplicados.

    Solo se permiten caracteres válidos dentro de un identificador RDF, para que
    nunca se genere una URI inválida en el archivo Turtle.
    """
    nombre = " ".join((valor or "").split())
    if prefijo and nombre.lower().startswith(prefijo.lower()):
        nombre = nombre[len(prefijo):]
    nombre = nombre.replace(" ", "_")
    nombre = re.sub(r"[^0-9A-Za-z_\-]", "", nombre)
    return nombre.strip("_")


def _etiquetas(consulta, variable):
    g = cargar_grafo()
    filas = g.query(consulta)
    etiquetas = set()
    for fila in filas:
        valor = getattr(fila, variable)
        etiquetas.add(str(valor).split("#")[-1])
    return sorted(etiquetas)


def obtener_usuarios():
    consulta = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?usuario WHERE { ?usuario a ex:Usuario . }
    """
    return _etiquetas(consulta, "usuario")


def obtener_alimentos():
    consulta = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?alimento WHERE { ?alimento a ex:Alimento . }
    """
    return _etiquetas(consulta, "alimento")


def obtener_componentes():
    consulta_nutriente = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?componente WHERE { ?componente a ex:Nutriente . }
    """
    consulta_alergeno = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?componente WHERE { ?componente a ex:Alergeno . }
    """
    return sorted(set(_etiquetas(consulta_nutriente, "componente") + _etiquetas(consulta_alergeno, "componente")))


def obtener_condiciones():
    consulta_patologia = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?condicion WHERE { ?condicion a ex:Patologia . }
    """
    consulta_restriccion = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?condicion WHERE { ?condicion a ex:RestriccionAlimentaria . }
    """
    return sorted(set(_etiquetas(consulta_patologia, "condicion") + _etiquetas(consulta_restriccion, "condicion")))


def obtener_condiciones_por_usuario():
    """Devuelve {id_usuario: [ids de condición]} para todos los usuarios del grafo."""
    consulta = """
    PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>
    SELECT ?usuario ?condicion WHERE {
        ?usuario a ex:Usuario .
        OPTIONAL { ?usuario ex:padece ?condicion . }
    }
    """
    g = cargar_grafo()
    resultado = {}
    for fila in g.query(consulta):
        usuario = str(fila.usuario).split("#")[-1]
        lista = resultado.setdefault(usuario, [])
        if fila.condicion is not None:
            lista.append(str(fila.condicion).split("#")[-1])
    return {usuario: sorted(condiciones) for usuario, condiciones in resultado.items()}


# ---------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------
@app.route('/')
def index():
    usuarios = obtener_usuarios()
    alimentos = obtener_alimentos()
    alimentos_limpios = [{"id": a, "label": limpiar_nombre(a)} for a in alimentos]
    usuarios_limpios = [{"id": u, "label": limpiar_nombre(u)} for u in usuarios]
    return render_template('index.html', usuarios=usuarios, usuarios_limpios=usuarios_limpios,
                           alimentos=alimentos, alimentos_limpios=alimentos_limpios)


@app.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.get_json(silent=True) or {}
    usuario = data.get('usuario', '').strip()
    ingredientes_disponibles = [i.strip() for i in data.get('ingredientes', []) if i.strip()]
    ingredientes_excluir = [i.strip() for i in data.get('excluir', []) if i.strip()]
    recetas_rechazadas = data.get('rechazadas', [])

    if not usuario:
        return jsonify({"error": "Debe seleccionar un perfil de usuario."}), 400
    if not ingredientes_disponibles:
        return jsonify({"error": "Debe seleccionar al menos un ingrediente."}), 400

    # Validar que el usuario exista en el RDF
    if usuario not in obtener_usuarios():
        return jsonify({"error": "El perfil de usuario seleccionado no existe en la base de datos."}), 400

    orquestador = OrquestadorNutricional(RDF_TTL)
    receta = orquestador.ejecutar_flujo(
        usuario,
        ingredientes_disponibles=ingredientes_disponibles,
        ingredientes_excluir=ingredientes_excluir,
        recetas_rechazadas=recetas_rechazadas,
        umbral_faltantes_max=4,
    )

    if receta is None:
        return jsonify({
            "error": "No se encontró una receta apta con los ingredientes seleccionados y las restricciones del usuario."
        }), 404

    return jsonify({"receta": receta})


@app.route('/validar-nombre', methods=['GET'])
def validar_nombre():
    """Valida si un nombre ya existe en la base de datos RDF."""
    tipo = request.args.get('tipo', '').strip()
    nombre = request.args.get('nombre', '').strip()

    if not tipo or not nombre:
        return jsonify({"existe": False, "mensaje": ""})

    # Anteponer prefijo según el tipo para construir el URI completo
    if tipo == 'usuario':
        nombre_completo = f"Usuario_{nombre}"
    elif tipo == 'alimento':
        nombre_completo = f"Alimento_{nombre}"
    elif tipo == 'condicion':
        nombre_completo = nombre
    else:
        nombre_completo = nombre

    g = Graph()
    g.parse(RDF_TTL, format="turtle")

    uri = URIRef(EX_STR + nombre_completo)

    # Verificar si existe alguna triple con este URI como sujeto
    existe = bool(list(g.triples((uri, None, None))))

    return jsonify({
        "existe": existe,
        "mensaje": f"El nombre '{nombre_completo}' ya está en uso." if existe else ""
    })


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    usuarios = obtener_usuarios()
    alimentos = obtener_alimentos()
    componentes = obtener_componentes()
    condiciones = obtener_condiciones()

    if request.method == 'POST':
        tipo = (request.form.get('tipo') or '').strip()

        try:
            with _RDF_LOCK:
                g = cargar_grafo_estricto()

                if tipo == 'usuario':
                    nombre = normalizar_nombre(request.form.get('nombre_usuario'), 'Usuario_')
                    if not nombre:
                        flash('El nombre de usuario es obligatorio.', 'error')
                        return redirect(url_for('agregar'))
                    nombre_completo = f"Usuario_{nombre}"
                    uri = EX[nombre_completo]
                    if bool(list(g.triples((uri, None, None)))):
                        flash(f'El usuario "{nombre_completo}" ya existe en la base de datos.', 'error')
                        return redirect(url_for('agregar'))
                    g.add((uri, RDF.type, EX.Usuario))
                    for cond in request.form.getlist('condiciones'):
                        if cond in condiciones:
                            g.add((uri, EX.padece, EX[cond]))

                elif tipo == 'alimento':
                    nombre = normalizar_nombre(request.form.get('nombre_alimento'), 'Alimento_')
                    if not nombre:
                        flash('El nombre del alimento es obligatorio.', 'error')
                        return redirect(url_for('agregar'))
                    nombre_completo = f"Alimento_{nombre}"
                    uri = EX[nombre_completo]
                    if bool(list(g.triples((uri, None, None)))):
                        flash(f'El alimento "{nombre_completo}" ya existe en la base de datos.', 'error')
                        return redirect(url_for('agregar'))
                    g.add((uri, RDF.type, EX.Alimento))
                    for comp in request.form.getlist('componentes'):
                        if comp in componentes:
                            g.add((uri, EX.contiene, EX[comp]))

                elif tipo == 'condicion':
                    nombre = normalizar_nombre(request.form.get('nombre_condicion'))
                    tipo_cond = (request.form.get('tipo_condicion') or '').strip()
                    severidad = (request.form.get('severidad') or '').strip()
                    contraindica = (request.form.get('contraindica') or '').strip()
                    if not nombre or not tipo_cond or not severidad or not contraindica:
                        flash('Todos los campos de la condición son obligatorios.', 'error')
                        return redirect(url_for('agregar'))
                    if tipo_cond not in ('Patologia', 'RestriccionAlimentaria'):
                        flash('El tipo de condición seleccionado no es válido.', 'error')
                        return redirect(url_for('agregar'))
                    if contraindica not in componentes:
                        flash('El componente contraindicado seleccionado no es válido.', 'error')
                        return redirect(url_for('agregar'))
                    uri = EX[nombre]
                    if bool(list(g.triples((uri, None, None)))):
                        flash(f'La condición "{nombre}" ya existe en la base de datos.', 'error')
                        return redirect(url_for('agregar'))
                    g.add((uri, RDF.type, EX[tipo_cond]))
                    g.add((uri, EX.nivelSeveridad, Literal(severidad, datatype=XSD.string)))
                    g.add((uri, EX.contraindica, EX[contraindica]))

                elif tipo == 'receta':
                    nombre = normalizar_nombre(request.form.get('nombre_receta'), 'Receta_')
                    if not nombre:
                        flash('El nombre de la receta es obligatorio.', 'error')
                        return redirect(url_for('agregar'))
                    ingredientes_receta = [a for a in request.form.getlist('ingredientes_receta') if a in alimentos]
                    if not ingredientes_receta:
                        flash('Debes seleccionar al menos un ingrediente para la receta.', 'error')
                        return redirect(url_for('agregar'))
                    nombre_completo = f"Receta_{nombre}"
                    uri = EX[nombre_completo]
                    if bool(list(g.triples((uri, None, None)))):
                        flash(f'La receta "{nombre_completo}" ya existe en la base de datos.', 'error')
                        return redirect(url_for('agregar'))
                    g.add((uri, RDF.type, EX.Receta))
                    for alim in ingredientes_receta:
                        g.add((uri, EX.compuestaPor, EX[alim]))

                elif tipo == 'editar_usuario':
                    usuario = (request.form.get('usuario_editar') or '').strip()
                    if usuario not in usuarios:
                        flash('Debes seleccionar un usuario válido.', 'error')
                        return redirect(url_for('agregar'))
                    uri = EX[usuario]
                    seleccionadas = [c for c in request.form.getlist('condiciones_usuario') if c in condiciones]
                    # Se reemplazan las condiciones actuales del usuario por las marcadas.
                    g.remove((uri, EX.padece, None))
                    for cond in seleccionadas:
                        g.add((uri, EX.padece, EX[cond]))
                    guardar_grafo_atomico(g)
                    flash(
                        f'Condiciones de {limpiar_nombre(usuario)} actualizadas correctamente.',
                        'success'
                    )
                    return redirect(url_for('agregar', editar=usuario))

                else:
                    flash('Debes seleccionar qué tipo de información deseas agregar.', 'error')
                    return redirect(url_for('agregar'))

                guardar_grafo_atomico(g)

        except ErrorRDF as exc:
            flash(str(exc), 'error')
            return redirect(url_for('agregar'))

        flash('La información se agregó correctamente a la base de datos RDF.', 'success')
        return redirect(url_for('agregar'))

    return render_template(
        'agregar.html',
        usuarios=usuarios,
        alimentos=alimentos,
        componentes=componentes,
        condiciones=condiciones,
        usuarios_limpios=[{"id": u, "label": limpiar_nombre(u)} for u in usuarios],
        alimentos_limpios=[{"id": a, "label": limpiar_nombre(a)} for a in alimentos],
        componentes_limpios=[{"id": c, "label": limpiar_nombre(c)} for c in componentes],
        condiciones_limpios=[{"id": c, "label": limpiar_nombre(c)} for c in condiciones],
        condiciones_por_usuario=obtener_condiciones_por_usuario(),
    )


if __name__ == '__main__':
    app.run(debug=True)

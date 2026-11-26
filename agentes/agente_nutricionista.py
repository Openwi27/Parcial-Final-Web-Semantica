from rdflib import Graph as RDFGraph
from rdflib import URIRef
from owlready2 import *

EX_STR = "http://www.Salud-AbleNutricion.com/ontologia#"


class AgenteNutricionista:

    def __init__(self, ruta_rdf):
        self.EX_STR = EX_STR
        self.ruta_rdf = ruta_rdf

        # Determinar ruta de la ontología relativa a la raíz del proyecto
        import os
        self.ruta_ontologia = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(ruta_rdf))),
            'ontologia', 'ontologia.owl'
        )

        # Cargar ontología con owlready2 para inferencia
        self.onto = get_ontology("http://www.Salud-AbleNutricion.com/ontologia#")
        try:
            self.onto.load()
        except Exception:
            self.onto = None

        # Cargar datos RDF con rdflib (para consultas de respaldo y nombres)
        self.grafo = RDFGraph()
        self.grafo.parse(ruta_rdf, format="turtle")

        # Aplicar reasoner si la ontología cargó correctamente
        self.reasoner_disponible = False
        if self.onto is not None:
            try:
                with self.onto:
                    # Agregar las instancias del RDF a la ontología para inferencia
                    self._cargar_instancias_en_onto()
                    sync_reasoner()
                    self.reasoner_disponible = True
            except Exception:
                self.reasoner_disponible = False

    def _cargar_instancias_en_onto(self):
        """Carga las instancias del RDF en la ontología owlready2."""
        for s, p, o in self.grafo:
            s_str = str(s)
            p_str = str(p)
            o_str = str(o)

            # Solo procesar triples del namespace ex
            if not s_str.startswith(self.EX_STR):
                continue

            s_name = s_str[len(self.EX_STR):]
            p_name = p_str[len(self.EX_STR):]

            # Crear o obtener entidad sujeto
            try:
                subj = self.onto[s_name]
            except Exception:
                continue

            # Crear propiedad si no existe
            try:
                pred = getattr(self.onto, p_name)
            except Exception:
                from owlready2 import ObjectProperty
                pred = ObjectProperty(p_name)
                setattr(self.onto, p_name, pred)

            # Obtener objeto
            if o_str.startswith(self.EX_STR):
                o_name = o_str[len(self.EX_STR):]
                try:
                    obj = self.onto[o_name]
                except Exception:
                    obj = o_str
            else:
                obj = o_str

            # Agregar triple
            try:
                pred[subj].append(obj)
            except Exception:
                pass

    def obtener_uri(self, identificador):
        if isinstance(identificador, URIRef):
            return identificador
        identificador_str = str(identificador)
        if identificador_str.startswith(
            "http://"
        ) or identificador_str.startswith("https://"):
            return URIRef(identificador_str)
        return URIRef(self.EX_STR + identificador_str)

    def _nombre_uri(self, uri_valor):
        """Extrae el nombre simple de una URI."""
        s = str(uri_valor)
        if s.startswith(self.EX_STR):
            return s[len(self.EX_STR):]
        return s

    def _uri_ex(self, nombre_simple):
        """Construye URI completa desde nombre simple."""
        return URIRef(self.EX_STR + nombre_simple)

    def consultar_condiciones_usuario(self, usuario_uri):
        """
        Consulta condiciones clínicas del usuario con inferencia OWL.
        Retorna (condiciones, contraindicaciones).
        """
        usuario_nombre = self._nombre_uri(usuario_uri)
        condiciones = {}
        contraindicados = set()

        if self.onto is not None and self.reasoner_disponible:
            # Usar owlready2 con inferencia
            try:
                with self.onto:
                    entidad_usuario = self.onto[usuario_nombre]

                    for condicion in entidad_usuario.padece:
                        cond_nombre = condicion.name
                        if cond_nombre not in condiciones:
                            condiciones[cond_nombre] = set()

                        # Contraindicaciones directas
                        for comp in condicion.contraindica:
                            comp_nombre = comp.name
                            contraindicados.add(comp_nombre)
                            condiciones[cond_nombre].add(comp_nombre)

                        # Contraindicaciones heredadas (ancestros)
                        for ancestro in condicion.ancestors():
                            if hasattr(ancestro, 'contraindica'):
                                for comp in ancestro.contraindica:
                                    comp_nombre = comp.name
                                    contraindicados.add(comp_nombre)
                                    condiciones[cond_nombre].add(comp_nombre)

                    # Contraindicaciones a través de subclases de las condiciones
                    for cond_nombre_2 in list(condiciones.keys()):
                        cond_entidad = self.onto[cond_nombre_2]
                        for subclase in cond_entidad.subclasses():
                            for comp in subclase.contraindica:
                                comp_nombre = comp.name
                                contraindicados.add(comp_nombre)
                                condiciones[cond_nombre_2].add(comp_nombre)

            except Exception:
                # Fallback a rdflib si falla owlready2
                return self._consultar_condiciones_rdflib(usuario_uri)

        else:
            return self._consultar_condiciones_rdflib(usuario_uri)

        return condiciones, contraindicados

    def _consultar_condiciones_rdflib(self, usuario_uri):
        """Consulta condiciones usando rdflib (método original sin inferencia)."""
        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?condicion ?componente
        WHERE {
            ?usuario ex:padece ?condicion .
            OPTIONAL { ?condicion ex:contraindica ?componente . }
        }
        """
        resultados = self.grafo.query(
            consulta, initBindings={"usuario": usuario_uri}
        )

        condiciones = {}
        contraindicaciones = set()

        for fila in resultados:
            c = fila.condicion
            comp = fila.componente
            c_nombre = self._nombre_uri(c)
            if c_nombre not in condiciones:
                condiciones[c_nombre] = set()
            if comp:
                comp_nombre = self._nombre_uri(comp)
                contraindicaciones.add(comp_nombre)
                condiciones[c_nombre].add(comp_nombre)

        return condiciones, contraindicaciones

    def evaluar_receta(self, receta_candidata, usuario):
        usuario_uri = self.obtener_uri(usuario)
        receta_uri = self.obtener_uri(receta_candidata["uri_receta"])
        receta_nombre = self._nombre_uri(receta_uri)

        condiciones, contraindicados = self.consultar_condiciones_usuario(
            usuario_uri
        )

        alimentos_conflictivos = set()
        motivos = []

        if self.onto is not None and self.reasoner_disponible:
            # Usar owlready2 con inferencia para obtener componentes de la receta
            try:
                with self.onto:
                    entidad_receta = self.onto[receta_nombre]

                    for alimento in entidad_receta.compuestaPor:
                        alimento_nombre = alimento.name

                        # Obtener componentes del alimento (con inferencia)
                        for componente in alimento.contiene:
                            comp_nombre = componente.name

                            if comp_nombre in contraindicados:
                                alimentos_conflictivos.add(alimento_nombre)
                                for cond, comps in condiciones.items():
                                    if comp_nombre in comps:
                                        motivos.append(
                                            {
                                                "alimento": alimento_nombre,
                                                "componente": comp_nombre,
                                                "condicion": cond,
                                            }
                                        )
            except Exception:
                # Fallback a rdflib
                return self._evaluar_receta_rdflib(
                    receta_candidata, usuario_uri, condiciones, contraindicados
                )
        else:
            return self._evaluar_receta_rdflib(
                receta_candidata, usuario_uri, condiciones, contraindicados
            )

        if alimentos_conflictivos:
            return {
                "apta": False,
                "receta": receta_candidata["nombre"],
                "motivos": motivos,
                "ingredientes_a_evitar": alimentos_conflictivos,
            }
        else:
            return {"apta": True, "receta": receta_candidata}

    def _evaluar_receta_rdflib(
        self, receta_candidata, usuario_uri, condiciones, contraindicados
    ):
        """Evaluar receta usando rdflib (método original)."""
        receta_uri = self.obtener_uri(receta_candidata["uri_receta"])

        consulta = """
        PREFIX ex: <http://www.Salud-AbleNutricion.com/ontologia#>

        SELECT ?alimento ?componente
        WHERE {
            ?receta ex:compuestaPor ?alimento .
            ?alimento ex:contiene ?componente .
        }
        """
        resultados = self.grafo.query(
            consulta, initBindings={"receta": receta_uri}
        )

        alimentos_conflictivos = set()
        motivos = []

        for fila in resultados:
            alimento = fila.alimento
            componente = fila.componente
            alimento_nombre = self._nombre_uri(alimento)
            comp_nombre = self._nombre_uri(componente)

            if comp_nombre in contraindicados:
                alimentos_conflictivos.add(alimento_nombre)
                for cond, comps in condiciones.items():
                    if comp_nombre in comps:
                        motivos.append(
                            {
                                "alimento": alimento_nombre,
                                "componente": comp_nombre,
                                "condicion": cond,
                            }
                        )

        if alimentos_conflictivos:
            return {
                "apta": False,
                "receta": receta_candidata["nombre"],
                "motivos": motivos,
                "ingredientes_a_evitar": alimentos_conflictivos,
            }
        else:
            return {"apta": True, "receta": receta_candidata}

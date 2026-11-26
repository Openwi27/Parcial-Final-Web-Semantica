# Sistema Multiagente de Recomendación de Dietas

Aplicación web (Flask) que integra un sistema multiagente de recomendación de dietas con una ontología (OWL) y almacenamiento de conocimiento en RDF. La interfaz permite capturar información del usuario, ejecutar el proceso de recomendación mediante el orquestador y visualizar los resultados.

## Estructura del proyecto

```
.
├── agentes/            # Agentes inteligentes y orquestador
│   ├── agente_chef.py
│   ├── agente_nutricionista.py
│   └── orquestador.py
├── almacenamientoRDF/  # Generación y archivos RDF del inventario de usuario
│   ├── RDF.py
│   ├── consultasSPARQL.py
│   └── instancias_inventario_usuario.{rdf,ttl}
├── ontologia/          # Generación y archivo de la ontología
│   ├── ontologia.py
│   └── ontologia.owl
├── interfaz/           # Aplicación web Flask
│   ├── app.py
│   ├── static/
│   └── templates/
├── AGENTS.md           # Guía de trabajo para agentes de código
└── README.md
```

## Requisitos

- Python 3.10+
- Dependencias listadas en `requirements.txt` (si aplica) o instalables manualmente.

Librerías principales utilizadas:
- Flask
- rdflib (para manipulación RDF, según imports del proyecto)
- owlready2 / similares (verificar imports)

## Instalación

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Si no existe `requirements.txt`, instalar manualmente las dependencias detectadas en los imports de `agentes/`, `almacenamientoRDF/` y `ontologia/`.

## Ejecución

```bash
cd interfaz
python app.py
```

La aplicación se iniciará en `http://127.0.0.1:5000/` por defecto.

## Notas

- Los archivos `instancias_inventario_usuario.*` son datos generados por `almacenamientoRDF/RDF.py`; se regeneran al ejecutar dicho script.
- Los archivos `.bak` y `__pycache__/` se ignoran en el repositorio.
- No modificar la ontología ni los archivos RDF sin una necesidad comprobada (ver `AGENTS.md`).

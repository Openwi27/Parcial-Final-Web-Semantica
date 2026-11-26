
# AGENTS.md — Sistema Multiagente de Recomendación de Dietas

## 1. Contexto general del proyecto

El proyecto consiste en desarrollar una interfaz gráfica web para un sistema inteligente de recomendación de dietas basado en una arquitectura multiagente.

La aplicación permitirá a los usuarios interactuar con el sistema, proporcionar información relevante para generar recomendaciones alimenticias y visualizar los resultados producidos por los agentes inteligentes.

El desarrollo de la interfaz gráfica se realizará utilizando **Python y Flask**.

El proyecto ya cuenta con componentes relacionados con la lógica multiagente, la representación del conocimiento mediante ontologías y el almacenamiento de información en RDF. Por tanto, el objetivo principal es integrar estos componentes existentes mediante una interfaz web funcional, sin duplicar ni reemplazar innecesariamente la lógica ya implementada.

### Objetivo principal

Desarrollar una aplicación web con Flask que permita interactuar con el sistema multiagente de recomendación de dietas, facilitando la entrada de información del usuario, la ejecución del proceso de recomendación y la presentación de resultados.

---

## 2. Estructura actual del proyecto

El repositorio está organizado en tres carpetas principales:

```text
proyecto/
│
├── agentes/
│   ├── [Agente 1]
│   ├── [Agente 2]
│   └── [Orquestador]
│
├── almacenamiendoRDF/
│   ├── [Script de generación RDF]
│   └── [Archivos RDF generados]
│
├── ontologia/
│   ├── [Script de generación de ontología]
│   └── [Archivo de ontología]
│
└── AGENTS.md
```

Los nombres anteriores representan las responsabilidades de los archivos, no necesariamente sus nombres reales. Antes de realizar cualquier modificación, se debe inspeccionar el repositorio para identificar los nombres, extensiones y dependencias existentes.

### 2.1. Carpeta `agentes/`

Contiene los dos agentes inteligentes del sistema y su respectivo orquestador.

Responsabilidades:
- Implementar la lógica de los agentes.
- Procesar la información necesaria para cumplir sus respectivas funciones.
- Coordinar la comunicación y ejecución de los agentes mediante el orquestador.
- Generar o gestionar los resultados del proceso de recomendación.

Instrucciones:
- Analizar cómo se ejecutan actualmente los agentes.
- Identificar los parámetros de entrada y los resultados que producen.
- Identificar cómo funciona la comunicación entre los agentes y el orquestador.
- Reutilizar el orquestador como punto de entrada para la interfaz, siempre que su arquitectura lo permita.
- No duplicar la lógica de los agentes dentro de Flask.
- No modificar el funcionamiento interno de los agentes sin una justificación técnica.

### 2.2. Carpeta `almacenamiendoRDF/`

Contiene el archivo Python encargado de generar la estructura RDF del sistema y los archivos RDF resultantes.

Responsabilidades:
- Generar representaciones de conocimiento en formato RDF.
- Gestionar los archivos RDF utilizados por el sistema.
- Proporcionar la información estructurada que necesitan los componentes del sistema.

Instrucciones:
- Identificar el script encargado de generar el RDF.
- Analizar las clases, propiedades y relaciones que se representan.
- Identificar qué archivos RDF consume el sistema multiagente.
- Determinar cómo se consultan o actualizan los datos.
- Evitar sobrescribir los archivos RDF existentes sin comprender previamente su función.
- Mantener la compatibilidad con la representación de conocimiento actual.

### 2.3. Carpeta `ontologia/`

Contiene el script Python encargado de generar la ontología y el archivo de ontología correspondiente.

Responsabilidades:
- Definir las clases y propiedades del dominio.
- Representar las relaciones semánticas entre los conceptos.
- Proporcionar la estructura conceptual sobre la que trabaja el sistema de recomendación.

Instrucciones:
- Inspeccionar el script de generación de la ontología.
- Analizar las clases, propiedades, restricciones y relaciones existentes.
- Identificar cómo se conecta la ontología con los archivos RDF.
- Mantener la consistencia semántica entre la ontología y los datos RDF.
- No crear una ontología paralela ni redefinir conceptos existentes sin justificación.

---

## 3. Tecnologías y herramientas

### Tecnologías principales

- **Python:** lenguaje principal del proyecto.
- **Flask:** framework para desarrollar la aplicación web.
- **RDF:** modelo de representación de conocimiento.
- **Ontologías:** representación formal de los conceptos y relaciones del dominio.
- **HTML:** estructura de las páginas web.
- **CSS:** estilos y presentación visual.
- **JavaScript:** interactividad de la interfaz cuando sea necesario.

### Dependencias

Antes de incorporar nuevas dependencias:
1. Inspeccionar los archivos existentes de requisitos.
2. Identificar las librerías que ya utiliza el proyecto.
3. Reutilizar las dependencias disponibles cuando sea posible.
4. Incorporar nuevas librerías únicamente cuando exista una necesidad técnica.

No asumir que se utilizan determinadas librerías RDF u ontológicas sin verificar los imports y archivos del proyecto.

---

## 4. Objetivos de desarrollo de la interfaz gráfica

La interfaz debe proporcionar un medio de interacción sencillo e intuitivo entre el usuario y el sistema multiagente.

Se deben considerar las siguientes funcionalidades:

### 4.1. Interfaz principal

- Crear una página de inicio que presente el sistema.
- Explicar brevemente el propósito del sistema de recomendación.
- Proporcionar acceso a las funcionalidades principales.
- Mantener una navegación clara y consistente.

### 4.2. Captura de información del usuario

- Diseñar formularios para recopilar la información necesaria para generar recomendaciones.
- Identificar los campos requeridos a partir de los parámetros que actualmente reciben los agentes.
- Validar los datos ingresados.
- Evitar solicitar información que el sistema no utilice.
- Presentar mensajes claros cuando existan datos incompletos o inválidos.

### 4.3. Integración con el sistema multiagente

- Conectar Flask con el orquestador existente.
- Enviar la información recopilada desde los formularios.
- Ejecutar el proceso multiagente mediante los mecanismos existentes.
- Gestionar los resultados devueltos por el orquestador.
- Manejar errores durante la ejecución sin interrumpir innecesariamente la aplicación.

### 4.4. Visualización de recomendaciones

- Presentar las recomendaciones generadas por el sistema.
- Organizar los resultados de manera comprensible.
- Diferenciar la información relevante para el usuario.
- Mostrar advertencias o restricciones alimentarias cuando el sistema las identifique.
- Evitar presentar como válida una recomendación que no haya sido generada o validada por el sistema.

Las funcionalidades definitivas deben establecerse después de analizar los resultados reales que producen los agentes.

---

## 5. Arquitectura de integración esperada

La aplicación Flask debe actuar como una capa de presentación e integración, no como un reemplazo de la arquitectura multiagente.

Flujo general esperado:

1. El usuario accede a la interfaz web.
2. Ingresa la información solicitada mediante formularios.
3. Flask recibe y valida los datos.
4. Flask transmite la información al orquestador.
5. El orquestador coordina la ejecución de los agentes.
6. Los agentes utilizan los mecanismos de conocimiento existentes, incluyendo la ontología y los datos RDF cuando corresponda.
7. El orquestador devuelve los resultados.
8. Flask procesa la respuesta y la presenta en la interfaz.

Representación conceptual:

```text
             USUARIO
                |
                v
       INTERFAZ WEB (HTML/CSS)
                |
                v
             FLASK
                |
          Validación de datos
                |
                v
           ORQUESTADOR
                |
          +-----+-----+
          |           |
          v           v
       AGENTE 1    AGENTE 2
          |           |
          +-----+-----+
                |
                v
       ONTOLOGÍA Y RDF
                |
                v
       RESULTADOS DEL SISTEMA
                |
                v
              FLASK
                |
                v
        INTERFAZ DE RESULTADOS
```

Este diagrama es una representación conceptual. El agente debe verificar el flujo real de dependencias y consultas antes de implementar la integración.

---

## 6. Organización propuesta para Flask

Se recomienda separar la interfaz web de la lógica de los agentes.

Una posible estructura de trabajo es:

```text
proyecto/
│
├── agentes/
│   ├── agente_1.py
│   ├── agente_2.py
│   └── orquestador.py
│
├── almacenamiendoRDF/
│   ├── generar_rdf.py
│   └── archivos_rdf/
│
├── ontologia/
│   ├── generar_ontologia.py
│   └── ontologia.owl
│
├── interfaz/
│   ├── app.py
│   ├── routes/
│   │   └── main.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── formulario.html
│   │   └── resultados.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── requirements.txt
└── AGENTS.md
```

Esta estructura es una propuesta, no una instrucción para reorganizar inmediatamente el repositorio.

Se debe conservar la organización actual y crear únicamente los archivos y directorios necesarios para implementar la interfaz.

---

## 7. Lineamientos de diseño de la interfaz

La interfaz debe tener un diseño moderno, limpio y fácil de utilizar.

Se establecen los siguientes criterios:

- Diseño visual consistente en todas las páginas.
- Navegación intuitiva.
- Formularios organizados por secciones.
- Jerarquía visual clara.
- Diseño adaptable a diferentes tamaños de pantalla.
- Mensajes de validación y retroalimentación comprensibles.
- Presentación ordenada de las recomendaciones.

El diseño debe estar relacionado con el dominio de nutrición, alimentación y bienestar.

Se pueden utilizar elementos visuales relacionados con alimentos, ingredientes y preparación de dietas, evitando una interfaz sobrecargada.

La experiencia de usuario debe priorizar la claridad de la información y la facilidad de interacción.

---

## 8. Reglas y restricciones de desarrollo

El agente de OpenCode debe cumplir las siguientes reglas:

### Análisis previo

- Antes de escribir código, inspeccionar la estructura completa del repositorio.
- Leer los scripts de los agentes y el orquestador.
- Comprender cómo se generan y utilizan los archivos RDF.
- Examinar la ontología y sus relaciones.
- Identificar las dependencias existentes.
- No asumir nombres de funciones, clases o parámetros sin verificarlos.

### Desarrollo

- Mantener la arquitectura existente.
- Separar la lógica de presentación de la lógica de negocio.
- Reutilizar funciones y componentes existentes.
- Evitar duplicar funcionalidades.
- Mantener el código modular y legible.
- Utilizar rutas y métodos HTTP apropiados en Flask.
- Implementar manejo de excepciones.
- Evitar dependencias innecesarias entre la interfaz y los agentes.

### Protección de componentes existentes

- No eliminar archivos existentes.
- No reemplazar los agentes por implementaciones simuladas.
- No modificar la ontología ni los archivos RDF sin una necesidad comprobada.
- No alterar el comportamiento del orquestador para facilitar artificialmente la integración.
- No sobrescribir información existente durante las pruebas.

### Comunicación con el usuario

- Explicar qué archivos se modificarán y por qué.
- Informar sobre los problemas de integración encontrados.
- Solicitar aclaraciones cuando existan decisiones arquitectónicas importantes que no puedan determinarse mediante el código.
- No afirmar que una funcionalidad está terminada sin haberla probado.

---

## 9. Metodología de trabajo esperada

El desarrollo debe realizarse progresivamente.

### Fase 1. Exploración y comprensión

- Inspeccionar el repositorio.
- Identificar las dependencias.
- Comprender el funcionamiento de los agentes.
- Analizar el orquestador.
- Comprender la relación entre RDF y ontología.
- Documentar los mecanismos de integración existentes.

No modificar código durante esta fase.

### Fase 2. Diseño de la solución

- Proponer la arquitectura de Flask.
- Definir las rutas necesarias.
- Identificar los formularios requeridos.
- Establecer cómo se comunicará Flask con el orquestador.
- Proponer la organización de las plantillas y recursos estáticos.

Presentar la propuesta antes de realizar cambios estructurales.

### Fase 3. Desarrollo de la interfaz

- Crear la aplicación Flask.
- Implementar las rutas.
- Construir las plantillas HTML.
- Desarrollar los estilos CSS.
- Incorporar JavaScript cuando sea necesario.
- Implementar validaciones de formularios.

### Fase 4. Integración multiagente

- Conectar la interfaz con el orquestador.
- Verificar los parámetros enviados.
- Comprobar la ejecución de los agentes.
- Gestionar las respuestas.
- Implementar el manejo de errores.

### Fase 5. Pruebas y validación

- Verificar que Flask inicie correctamente.
- Probar las rutas.
- Validar los formularios.
- Comprobar la comunicación con el orquestador.
- Verificar que las recomendaciones mostradas correspondan a los resultados reales.
- Comprobar que los componentes RDF y la ontología sigan funcionando correctamente.

---

## 10. Criterios de aceptación

El desarrollo se considerará funcional cuando:

1. La aplicación web pueda iniciarse correctamente mediante Flask.
2. El usuario pueda acceder a la interfaz.
3. Los formularios permitan ingresar la información necesaria.
4. Flask pueda comunicarse correctamente con el orquestador.
5. Los agentes puedan ejecutarse utilizando su implementación existente.
6. Los resultados puedan recibirse y visualizarse correctamente.
7. La aplicación gestione los errores de manera controlada.
8. La integración no afecte el funcionamiento de la ontología ni del almacenamiento RDF.

---

## 11. Instrucción general para el agente

Tu responsabilidad principal es desarrollar la interfaz gráfica web del sistema multiagente de recomendación de dietas utilizando Flask.

Debes trabajar sobre el código existente, comprender primero cómo funciona la arquitectura y posteriormente implementar la integración.

Prioriza la reutilización de los componentes existentes, la modularidad del código y la separación de responsabilidades.

No construyas una implementación alternativa de los agentes, del orquestador, de la ontología o del almacenamiento RDF.

Trabaja de manera incremental, verificando cada funcionalidad antes de continuar con la siguiente.

Cuando recibas una nueva tarea, analiza su relación con la arquitectura general y modifica únicamente los componentes necesarios.

Si encuentras inconsistencias, errores o limitaciones en el código existente, documenta los hallazgos y propone soluciones antes de realizar modificaciones que puedan afectar el funcionamiento general del sistema.

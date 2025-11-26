import streamlit as st
import pandas as pd
import numpy as np

# --- 1. CRITERIOS Y PESOS BASADOS EN EL ESTUDIO (ESCALA 1-5) ---

CUESTIONARIO_IAM = {
    "A. OBSERVACIÓN CONDUCTUAL (El Corazón del Modelo Híbrido)": {
        "P1_Conductual": {
            "pregunta": "¿El estudio utilizó **observación conductual (Y)** para medir la acción real (ej: CTR, Conversión, Frecuencia de Compra) además del autorreporte (encuesta)? (1=No, 5=Absolutamente)",
            "peso": 4.5, 
            "ayuda_humana": (
                "Peso Ponderado: 4.5 | Referencia: Nivel Conductual (Y)\n\n"
                "1. **Sirve para:** Estimar la Autenticidad de los Datos del estudio, yendo más allá de lo que el consumidor dice.\n"
                "2. **¿Por qué?:** La encuesta tradicional solo mide intenciones. Es necesario contrastar con la acción real (lo que la gente hace) para cerrar la 'Brecha Intención–Conducta'.\n"
                "3. **¿Cómo se mide?:** Analizando métricas digitales o reales como la Tasa de Conversión (Y), Frecuencia de Compra, o el comportamiento en un laboratorio de observación."
            ),
            "referencia": "Nivel Conductual (Y), Dimensión: Autenticidad de los Datos.",
            "fuente_dato": "**Buscando en:** Tablas de Resultados, Anexo de Métricas Digitales (Google Analytics, Adobe Analytics) o Reportes de CRM (Salesforce, Hubspot)."
        },
        "P2_Coincidencia_Segmento": {
            "pregunta": "¿Se aseguró que los datos observacionales ($\mathbf{Y}$) y los datos declarativos ($\mathbf{X}$) provenían del **mismo segmento de consumidores** y del **mismo periodo de tiempo** (Contraste de Fuentes)? (1=No, 5=Absolutamente)",
            "peso": 4.0,
            "ayuda_humana": (
                "Peso Ponderada: 4.0 | Referencia: Triangulación Metodológica\n\n"
                "1. **Sirve para:** Asegurar la Validez de la Triangulación Metodológica.\n"
                "2. **¿Por qué?:** Si los grupos no son los mismos, la comparación es inválida. La efectividad de la observación (Y) debe ser atribuible a la intención (X) de ese mismo grupo.\n"
                "3. **¿Cómo se mide?:** Documentando el periodo de tiempo (ej: Transversal, 2025) y los criterios de segmentación para $\mathbf{X}$ y $\mathbf{Y}$."
            ),
            "referencia": "Método Deductivo, Triangulación Metodológica.",
            "fuente_dato": "**Buscando en:** Sección de Metodología (Subsección 'Muestra' o 'Recolección de Datos'). El documento debe declarar: 'Se observó a los mismos N participantes encuestados'."
        },
        "P3_Lealtad_Observada": {
            "pregunta": "¿Se incluyeron indicadores de **Lealtad/Retención Observada** (ej: Frecuencia de Compra en 6 meses) para validar las intenciones de recompra declaradas? (1=No, 5=Absolutamente)",
            "peso": 3.0,
            "ayuda_humana": (
                "Peso Ponderada: 3.0 | Referencia: Lealtad/Retención Observada\n\n"
                "1. **Sirve para:** Evaluar la fiabilidad de las intenciones de recompra a largo plazo.\n"
                "2. **¿Por qué?:** Las intenciones de lealtad son muy susceptibles al sesgo. Contrastarlas con el historial de pedidos reales reduce el riesgo.\n"
                "3. **¿Cómo se mide?:** Mediante el análisis de datos de CRM o de ventas que muestren el número de pedidos por cliente en un periodo definido."
            ),
            "referencia": "Operacionalización: Lealtad/Retención Observada.",
            "fuente_dato": "**Buscando en:** Tablas de Datos Descriptivos, Análisis de Cohortes de Clientes (CRM) o Resultados de Retención y Valor de Vida del Cliente (CLV)."
        },
        "P4_Intencion_Historica": {
            "pregunta": "¿Se contrastaron las intenciones declaradas ($\mathbf{X}$) con un **historial de consumo previo** o acciones en el carrito de compra del participante, si el estudio fue online? (1=No, 5=Absolutamente)",
            "peso": 3.0,
            "ayuda_humana": (
                "Peso Ponderada: 3.0 | Referencia: Intención de Compra Futura (online)\n\n"
                "1. **Sirve para:** Dar contexto real a la Intención de Compra Futura.\n"
                "2. **¿Por qué?:** Un participante con historial o interés previo (carrito activo) tiene una intención más fiable que alguien sin historial. Esto reduce el ruido.\n"
                "3. **¿Cómo se mide?:** Analizando los patrones de consumo previo o las acciones de *e-commerce* de ese mismo participante (anonimizado)."
            ),
            "referencia": "Operacionalización: Intención de Compra Futura (online).",
            "fuente_dato": "**Buscando en:** Descripción de Variables (si se incluyó 'Historial de Compra' como variable de control) o el Apéndice de Recolección de Datos."
        },
        "P5_Modelo_Hibrido_Explicito": {
            "pregunta": "¿El estudio propuso y documentó explícitamente un **modelo de validación híbrido** que combina datos declarativos, observacionales y analíticos (Correlacional)? (1=No, 5=Absolutamente)",
            "peso": 4.0,
            "ayuda_humana": (
                "Peso Ponderada: 4.0 | Referencia: Modelo Híbrido de Validación\n\n"
                "1. **Sirve para:** Determinar si el estudio tiene una base metodológica robusta para la validación.\n"
                "2. **¿Por qué?:** La validación no puede ser un accidente. El estudio debe tener un plan formal (el modelo híbrido) para integrar las diferentes fuentes de datos y no solo recolectarlas.\n"
                "3. **¿Cómo se mide?:** Buscando diagramas o matrices conceptuales que muestren la interrelación de $\mathbf{X}$ (encuesta), $\mathbf{Y}$ (observación) y los sesgos ($\mathbf{M}$) en el análisis."
            ),
            "referencia": "Objetivo General, Propuesta de Wedel & Kannan (2016).",
            "fuente_dato": "**Buscando en:** Marco Teórico, Hipótesis o Sección de Modelización/Análisis. Debe haber un diagrama de flujo de las variables (X, Y, M)."
        },
    },
    
    "B. CONTROL Y MEDICIÓN DE SESGOS (Deseabilidad y Racionalización)": {
        "P6_Medicion_Sesgo": {
            "pregunta": "¿Se incluyeron **ítems indirectos** para cuantificar la **Deseabilidad Social ($\mathbf{M}$) o la Racionalización** como variable moderadora o de control? (1=No, 5=Absolutamente)",
            "peso": 4.5,
            "ayuda_humana": (
                "Peso Ponderada: 4.5 | Referencia: Hipótesis H2 (Medición de Sesgo)\n\n"
                "1. **Sirve para:** Medir la vulnerabilidad intrínseca del estudio al sesgo (el 'detector de mentiras').\n"
                "2. **¿Por qué?:** El sesgo de Deseabilidad Social distorsiona el autorreporte (ej: mentir sobre el consumo sostenible). Medir $\mathbf{M}$ es esencial para la $\mathbf{H}_2$.\n"
                "3. **¿Cómo se mide?:** Mediante el uso de preguntas 'trampa' o escalas validadas que miden la tendencia a dar respuestas socialmente aceptables."
            ),
            "referencia": "Matriz conceptual, Hipótesis $\mathbf{H}_2$, Grimm (2010).",
            "fuente_dato": "**Buscando en:** Apéndice de Cuestionario, Marco Teórico (Búsqueda de 'Escala de Deseabilidad Social' o 'Social Desirability Scale') y Tablas de Variables (M)."
        },
        "P7_Modelo_Moderador": {
            "pregunta": "¿Se usó **Regresión Lineal Múltiple** o un método para evaluar el **Efecto Moderador NEGATIVO** del sesgo ($\mathbf{M}$) sobre la relación Intención $\to$ Conducta? (1=No, 5=Absolutamente)",
            "peso": 4.0,
            "ayuda_humana": (
                "Peso Ponderada: 4.0 | Referencia: Análisis Explicativo\n\n"
                "1. **Sirve para:** Probar empíricamente si el sesgo está 'arruinando' la predicción de la conducta.\n"
                "2. **¿Por qué?:** La $\mathbf{H}_2$ es que el sesgo debilita el vínculo entre lo que dices ($\mathbf{X}$) y lo que haces ($\mathbf{Y}$). Esta prueba estadística es el corazón del análisis.\n"
                "3. **¿Cómo se mide?:** Analizando la significancia estadística del término de interacción ($\mathbf{X} \cdot \mathbf{M}$) en el modelo de regresión."
            ),
            "referencia": "Análisis Explicativo, Hipótesis $\mathbf{H}_2$.",
            "fuente_dato": "**Buscando en:** Tablas de Resultados Estadísticos (Búsqueda de 'Término de Interacción' o 'Regresión Moderada'). El modelo debe incluir $\mathbf{X} \\times \mathbf{M}$."
        },
        "P8_Validez_Externa": {
            "pregunta": "¿El análisis de sesgos permitió justificar la baja **Validez Externa** de los resultados puramente declarativos? (1=No, 5=Absolutamente)",
            "peso": 3.5,
            "ayuda_humana": (
                "Peso Ponderada: 3.5 | Referencia: Validez Externa\n\n"
                "1. **Sirve para:** Asegurar que las conclusiones del estudio son realistas y aplicables al mercado.\n"
                "2. **¿Por qué?:** Los resultados inflados por el sesgo (ej: todos dicen que aman el producto) no se mantienen en el mundo real. El estudio debe reconocer este riesgo.\n"
                "3. **¿Cómo se mide?:** Revisando las conclusiones para ver si el investigador reconoció que las intenciones declaradas no garantizan el comportamiento real."
            ),
            "referencia": "Impacto en la interpretación de resultados (Deseabilidad Social).",
            "fuente_dato": "**Buscando en:** Discusión de Resultados y Limitaciones. El investigador debe señalar que los resultados de la encuesta son más débiles que los resultados conductuales."
        },
        "P9_Post_Decision_Control": {
            "pregunta": "¿El diseño del cuestionario o la entrevista intentó **reducir la Racionalización Post-Decisión** (ej: preguntando por impulsos o emociones antes que razones)? (1=No, 5=Absolutamente)",
            "peso": 3.0,
            "ayuda_humana": (
                "Peso Ponderada: 3.0 | Referencia: Racionalización Post-Decisión\n\n"
                "1. **Sirve para:** Mitigar la tendencia humana a inventar razones lógicas *después* de actuar por impulso.\n"
                "2. **¿Por qué?:** Las decisiones son emocionales, y la justificación es posterior. La encuesta debe capturar lo emocional primero.\n"
                "3. **¿Cómo se mide?:** Verificando si las preguntas clave sobre 'motivación de compra' se enfocaron en sentimientos o impulsos antes de pedir argumentos racionales."
            ),
            "referencia": "Ariely (2008), Kahneman (2011), Matriz conceptual.",
            "fuente_dato": "**Buscando en:** El Orden de las Preguntas en el Apéndice de Cuestionario o la Descripción del Proceso de Entrevista (Sección Metodología)."
        },
        "P10_Conciencia_Limite": {
            "pregunta": "¿El estudio reconoce y discute que la intención declarada tiene un **límite epistemológico** debido a la falta de acceso consciente del consumidor a sus motivaciones reales? (1=No, 5=Absolutamente)",
            "peso": 2.5,
            "ayuda_humana": (
                "Peso Ponderada: 2.5 | Referencia: Límite de la Conciencia\n\n"
                "1. **Sirve para:** Demostrar profundidad teórica en la comprensión de la conducta del consumidor.\n"
                "2. **¿Por qué?:** La base teórica del modelo híbrido es que la conciencia no es un espejo perfecto de la acción. El estudio debe reconocer este límite.\n"
                "3. **¿Cómo se mide?:** Revisando la Introducción o el Marco Teórico en busca de referencias clave (ej: Kahneman, Zaltman) sobre la mente inconsciente."
            ),
            "referencia": "Conclusión Filosófica, Introducción (Kahneman, 2011).",
            "fuente_dato": "**Buscando en:** Introducción, Revisión de Literatura o Marco Teórico. Buscar citas a la Economía Conductual o la Psicología de la Decisión."
        },
    },

    "C. RIGOR ESTADÍSTICO Y VIABILIDAD (Validación Técnica)": {
        "P11_Alfa_Cronbach": {
            "pregunta": "¿Se documentó el $\mathbf{\\alpha}$ de Cronbach para asegurar la **consistencia interna** de las escalas ($\mathbf{X}$ y $\mathbf{M}$), cumpliendo el mínimo aceptable ($\mathbf{\\geq 0.70}$)? (1=No, 5=Absolutamente)",
            "peso": 2.0,
            "ayuda_humana": (
                "Peso Ponderada: 2.0 | Referencia: Consistencia Interna\n\n"
                "1. **Sirve para:** Asegurar la Confiabilidad y la consistencia técnica de las herramientas de medición.\n"
                "2. **¿Por qué?:** Es el estándar básico. Si las preguntas no son internamente coherentes, los resultados no sirven.\n"
                "3. **¿Cómo se mide?:** Buscando la tabla de resultados del $\mathbf{\\alpha}$ de Cronbach, donde el valor debe ser idealmente 0.70 o superior."
            ),
            "referencia": "Validación Técnica, Validez estadística.",
            "fuente_dato": "**Buscando en:** Sección 'Validez y Confiabilidad' o 'Análisis Descriptivo'. Debe haber una tabla con los valores $\mathbf{\\alpha}$."
        },
        "P12_Muestreo": {
            "pregunta": "¿El tipo de muestreo fue apropiado (ej: **No probabilístico por conveniencia** para el contraste observacional) y se justificó su delimitación? (1=No, 5=Absolutamente)",
            "peso": 1.5,
            "ayuda_humana": (
                "Peso Ponderada: 1.5 | Referencia: Muestreo\n\n"
                "1. **Sirve para:** Justificar la selección de los participantes para el contraste de datos.\n"
                "2. **¿Por qué?:** La validez del contraste depende de que los participantes de la encuesta sean los mismos cuyas acciones se observan. El muestreo debe reflejar esta necesidad.\n"
                "3. **¿Cómo se mide?:** Revisando la sección de Metodología y Muestra para ver la justificación del tipo de muestreo elegido."
            ),
            "referencia": "Muestra y Delimitaciones (Viabilidad Logística).",
            "fuente_dato": "**Buscando en:** Sección 'Metodología' o 'Muestra'. Debe indicar el tipo de muestreo y por qué se eligió."
        },
        "P13_Interaccion_Digital": {
            "pregunta": "¿El análisis incluyó métricas de **Interacción Digital** como variables descriptivas (ej: Tasa de Clics (CTR) o Duración Promedio de la Sesión)? (1=No, 5=Absolutamente)",
            "peso": 1.5,
            "ayuda_humana": (
                "Peso Ponderada: 1.5 | Referencia: Interacción Digital\n\n"
                "1. **Sirve para:** Medir el interés y la atención del consumidor en el entorno online.\n"
                "2. **¿Por qué?:** El tiempo y el clic son acciones sutiles que miden el compromiso real. No basta con la intención; la interacción demuestra el esfuerzo cognitivo.\n"
                "3. **¿Cómo se mide?:** Revisando la descripción de las variables o resultados donde se muestren promedios de CTR o segundos de sesión."
            ),
            "referencia": "Operacionalización de Variable: Interacción Digital.",
            "fuente_dato": "**Buscando en:** Tablas de Descriptivos o Variables (Búsqueda de 'CTR promedio' o 'Tiempo promedio en la tarea')."
        },
        "P14_Enfoque_Cuantitativo": {
            "pregunta": "¿El enfoque fue claramente **Cuantitativo** (análisis estadístico de datos numéricos) para medir la brecha $\mathbf{X}$ $\to$ $\mathbf{Y}$? (1=No, 5=Absolutamente)",
            "peso": 1.0,
            "ayuda_humana": (
                "Peso Ponderada: 1.0 | Referencia: Enfoque Cuantitativo\n\n"
                "1. **Sirve para:** Asegurar que el estudio buscó la medición y la predicción (propósito del modelo híbrido).\n"
                "2. **¿Por qué?:** El modelo es para medir la magnitud de la brecha y el efecto moderador del sesgo. Esto solo se logra con estadísticas.\n"
                "3. **¿Cómo se mide?:** Verificando si el objetivo principal es 'analizar la magnitud de la brecha' o 'determinar el poder predictivo' (cuantitativo)."
            ),
            "referencia": "Enfoque de investigación (Creswell & Creswell, 2018).",
            "fuente_dato": "**Buscando en:** Objetivos y Metodología. Palabras clave: 'Regresión', 'Medir', 'Cuantificar', 'Magnitud'."
        },
        "P15_Explicativo_Deductivo": {
            "pregunta": "¿El alcance fue **Explicativo** y el método **Deductivo** (justificando $\mathbf{Y}$ a partir de $\mathbf{X}$), en línea con la prueba de hipótesis? (1=No, 5=Absolutamente)",
            "peso": 1.0,
            "ayuda_humana": (
                "Peso Ponderada: 1.0 | Referencia: Alcance y Método\n\n"
                "1. **Sirve para:** Definir el propósito y la ruta lógica del estudio.\n"
                "2. **¿Por qué?:** El estudio debe *explicar* por qué la intención no se cumple (brecha) y usar la teoría (marco teórico) para probarlo con datos (deductivo).\n"
                "3. **¿Cómo se mide?:** Revisando la sección 'Alcance' y 'Método' en el documento."
            ),
            "referencia": "Alcance y Método.",
            "fuente_dato": "**Buscando en:** Sección 'Alcance' o 'Tipo de Investigación'. Debe indicar claramente el objetivo de 'Explicar la relación causal'."
        },
    },
    
    "D. ÉTICA Y RECURSOS (Transparencia)": {
        "P16_Confidencialidad": {
            "pregunta": "¿Se garantizó la **confidencialidad** y el **anonimato** total de los participantes, especialmente de los datos digitales observacionales (clics, CRM)? (1=No, 5=Absolutamente)",
            "peso": 1.0,
            "ayuda_humana": (
                "Peso Ponderada: 1.0 | Referencia: Consideraciones éticas\n\n"
                "1. **Sirve para:** Cumplir con las normativas éticas y de protección de datos.\n"
                "2. **¿Por qué?:** El uso de datos observacionales (clics, CRM) es sensible. Es obligatorio garantizar que los datos se usaron de forma anónima y agregada.\n"
                "3. **¿Cómo se mide?:** Buscando la sección 'Consideraciones éticas' y el procedimiento de manejo de datos digitales."
            ),
            "referencia": "Consideraciones éticas.",
            "fuente_dato": "**Buscando en:** Sección 'Consideraciones Éticas', 'Consentimiento Informado' o 'Manejo de Datos'."
        },
        "P17_Juicio_Expertos": {
            "pregunta": "¿El instrumento de medición fue validado mediante un **juicio de expertos** para evaluar la pertinencia y claridad de los ítems? (1=No, 5=Absolutamente)",
            "peso": 1.0,
            "ayuda_humana": (
                "Peso Ponderada: 1.0 | Referencia: Juicio de Expertos\n\n"
                "1. **Sirve para:** Aumentar la Validez de Contenido de los instrumentos de medición.\n"
                "2. **¿Por qué?:** Antes de aplicarla, la encuesta debe ser revisada por especialistas para asegurar que las preguntas (ítems) miden lo que deben medir.\n"
                "3. **¿Cómo se mide?:** Buscando evidencia de revisión por académicos o profesionales en la sección 'Validez y confiabilidad'."
            ),
            "referencia": "Validez y confiabilidad.",
            "fuente_dato": "**Buscando en:** Sección 'Validez y Confiabilidad' o 'Diseño del Instrumento'. Debe mencionar 'Evaluación por Jueces Expertos'."
        },
    }
}


# --- 2. LÓGICA DE CÁLCULO Y DIAGNÓSTICO (MODIFICADA) ---

def calcular_indice_iam(puntuaciones, r_xy, beta_m):
    """
    Calcula el Índice de Autenticidad Metodológica (IAM) y ofrece consejos de mejora.
    r_xy: Correlación Intención (X) - Conducta (Y).
    beta_m: Coeficiente Beta del término de interacción (X * M) de la Regresión Moderada.
    """
    
    puntuacion_total = 0
    peso_total_maximo = 0
    detalle_puntuacion = {}
    puntos_criticos_bajos = []
    
    # --------------------------------------------------------------------------------
    # APLICACIÓN DE PESO ADICIONAL BASADO EN CIFRAS ESTADÍSTICAS
    # --------------------------------------------------------------------------------
    # 1. Ajuste de P1 (Observación Conductual - Puntuación real de la brecha)
    # Si la correlación r(X,Y) es alta (>= 0.50), la Puntuación P1 debería ser 5. 
    # Si es baja (< 0.30), la P1 debe ser castigada si no se hizo la observación.
    # El ajuste se aplica SÓLO si el investigador respondió BAJO (1 o 2) en P1, pero la correlación es buena.
    
    p1_respuesta_original = puntuaciones.get("P1_Conductual", 1)
    ajuste_p1 = 0 
    
    # Si el investigador dice que NO observó (P1 <= 2), pero la correlación r es ALTA.
    if p1_respuesta_original <= 2 and r_xy >= 0.50:
         ajuste_p1 = 2 # Le da un pequeño bono porque el resultado 'Y' es sorprendentemente bueno, aunque la metodología 'P1' fue mala.
    elif p1_respuesta_original >= 4 and r_xy < 0.30:
         ajuste_p1 = -1 # Castiga si el investigador dijo que SÍ observó bien (P1>=4), pero la brecha es GIGANTE (r es débil).
    
    puntuaciones["P1_Conductual"] = np.clip(p1_respuesta_original + ajuste_p1, 1, 5) # Aplicar el ajuste
    
    # 2. Ajuste de P7 (Análisis Moderador - Prueba de H2)
    # Si el coeficiente Beta del término de interacción (X*M) es significativo y NEGATIVO, la H2 se confirma.
    p7_respuesta_original = puntuaciones.get("P7_Modelo_Moderador", 1)
    ajuste_p7 = 0
    
    # Si el investigador dijo que SÍ hizo la regresión (P7 >= 4) y la prueba confirma H2 (beta es negativo)
    if p7_respuesta_original >= 4 and beta_m < 0: # Asumimos que si beta es negativo, es significativo (para simplificar el input)
        ajuste_p7 = 1 # Bono por probar la hipótesis central del modelo.
    elif p7_respuesta_original >= 4 and beta_m >= 0:
        ajuste_p7 = -2 # Castigo por decir que SÍ hicieron la prueba, pero el resultado refuta la teoría.

    puntuaciones["P7_Modelo_Moderador"] = np.clip(p7_respuesta_original + ajuste_p7, 1, 5) # Aplicar el ajuste
    # --------------------------------------------------------------------------------
    
    
    for dimension, preguntas in CUESTIONARIO_IAM.items():
        for clave, detalles in preguntas.items():
            respuesta = puntuaciones.get(clave, 0)
            peso_actual = detalles["peso"]
            
            puntuacion_obtenida_criterio = respuesta * peso_actual
            puntuacion_total += puntuacion_obtenida_criterio
            
            puntuacion_maxima_criterio = 5 * peso_actual
            peso_total_maximo += puntuacion_maxima_criterio
            
            # Detección de fallos críticos (Peso >= 4.0 y Respuesta <= 2)
            if peso_actual >= 4.0 and respuesta <= 2:
                 descripcion_corta = detalles['pregunta'].split("?")[0].replace("¿El estudio utilizó", "Falta").replace("¿Se aseguró que", "Falta").replace("¿El estudio propuso y documentó", "Falta").replace("¿Se incluyeron", "Falta").replace("¿Se usó", "Falta")
                 puntos_criticos_bajos.append(f"- **{clave} (Peso {peso_actual})**: {descripcion_corta.strip()}.")
            
            # Combinar información de ayuda y fuente de datos para el tooltip
            ayuda_completa = detalles["ayuda_humana"] + "\n\n**FUENTES DE EVIDENCIA (PARA CORROBORACIÓN):**\n" + detalles["fuente_dato"]
            
            detalle_puntuacion[detalles["pregunta"]] = {
                "Respuesta (1-5)": respuesta,
                "Peso": peso_actual,
                "Puntuación Ponderada": puntuacion_obtenida_criterio,
                "Puntuación Máxima": puntuacion_maxima_criterio,
                "Ayuda Completa": ayuda_completa # Almacenar la ayuda completa para el Streamlit
            }

    iam = (puntuacion_total / peso_total_maximo) * 100
    vulnerabilidad_metodologica = 100 - iam
    
    # ... (Lógica de Diagnóstico y Consejo de Mejora se mantiene igual) ...
    # Se ajusta la lógica de diagnóstico para reflejar los nuevos inputs:
    
    consejo_mejora = ""
    
    if iam >= 85:
        nivel = "Autenticidad EXCELENTE: ¡Una Locura Metodológica!"
        interpretacion = f"¡Felicidades! Este estudio no solo cumple con los requisitos estadísticos, sino que **desmantela la Brecha Intención-Conducta**. La **Vulnerabilidad Metodológica es extremadamente baja ({vulnerabilidad_metodologica:.2f} %)**. **Correlación Intención-Conducta (r): {r_xy:.2f}**. **Efecto Moderador (β): {beta_m:.2f}**."
        consejo_mejora = "El estudio es sólido. El único paso pendiente es asegurar que la **Discusión de Resultados** destaque y cuantifique la diferencia de este IAM frente a estudios tradicionales, usando este diagnóstico como prueba de la validez de su enfoque."

    elif iam >= 65:
        nivel = "Autenticidad MUY BUENA: Cumplimiento Fuerte del Modelo Híbrido"
        interpretacion = f"El estudio ha adoptado los pilares del modelo híbrido. Hay una buena **triangulación metodológica**. La **Vulnerabilidad Metodológica ({vulnerabilidad_metodologica:.2f} %)** es moderada. **Correlación r: {r_xy:.2f}**. **Efecto Moderador β: {beta_m:.2f}**."
        
        if p7_respuesta_original < 4 or (p7_respuesta_original >= 4 and beta_m >= 0):
             consejo_mejora = "El diagnóstico es fuerte, pero revise su **Análisis Moderador (P7)**. Parece que no se corrió la Regresión Moderada para probar la $\mathbf{H}_2$, o el resultado del $\mathbf{\\beta}$ fue nulo o positivo, lo cual debilita la teoría del sesgo. Necesita correr/ajustar esa prueba."
        else:
             consejo_mejora = "El estudio es sólido, pero podría mejorar en la integración de métricas de Lealtad (P3) o Historial (P4)."
        
    elif iam >= 50:
        nivel = "Autenticidad ACEPTABLE: Implementación Parcial del Modelo Híbrido"
        interpretacion = f"El estudio está 'a medio camino'. Es probable que **no haya medido el sesgo como moderador** o que la **observación conductual sea débil**. La **Vulnerabilidad Metodológica ({vulnerabilidad_metodologica:.2f} %)** es alta. **Correlación r: {r_xy:.2f}**. **Efecto Moderador β: {beta_m:.2f}**."
        
        consejo_mejora = (
            "🚨 **¡Alerta de Corrección!** Su estudio tiene potencial, pero está en riesgo de caer en las trampas tradicionales. Revise los siguientes puntos críticos:\n\n"
            + "".join(puntos_criticos_bajos) + "\n\n"
            "**Plan de Acción Humano:** Si no puede recolectar más datos de observación (P1), su única salvación es enfocarse en **P6 (medir el sesgo)** y **P7 (analizar su efecto moderador)**. Así, demuestra que, aunque no eliminó el sesgo, al menos probó y cuantificó su vulnerabilidad."
        )

    else:
        nivel = "Autenticidad DÉBIL: Dominio del Sesgo y la Encuesta Tradicional"
        interpretacion = f"El estudio se basó casi exclusivamente en la encuesta declarativa. Es **altamente vulnerable a la Deseabilidad Social y la Racionalización**. La **Vulnerabilidad Metodológica ({vulnerabilidad_metodologica:.2f} %)** es crítica. **Correlación r: {r_xy:.2f}**. **Efecto Moderador β: {beta_m:.2f}**."
        
        consejo_mejora = (
            "🛑 **¡El Estudio Está en Riesgo!** El estudio se basa en lo que critica. **Debe corregir urgentemente los pilares**:\n\n"
            + "".join(puntos_criticos_bajos) + "\n\n"
            "**Plan de Acción Humano:**\n"
            "1. **Observación (P1):** Tiene que encontrar una métrica de acción real (CTR, tiempo en página, una compra pequeña) para contrastar la encuesta.\n"
            "2. **Medición del Sesgo (P6):** ¡Es su hipótesis principal! Incluya preguntas indirectas para detectar Deseabilidad Social.\n"
            "3. **Análisis de Ponderación (P7):** Use Regresión Moderada para probar que el sesgo **arruina** la relación Intención-Conducta."
        )

    return iam, nivel, interpretacion, consejo_mejora, detalle_puntuacion, peso_total_maximo, vulnerabilidad_metodologica

# --- 3. INTERFAZ STREAMLIT (MEJORADA CON INPUT ESTADÍSTICO) ---

def main():
    st.set_page_config(page_title="Evaluador IAM Final", layout="wide")
    
    st.title("Índice de Autenticidad Metodológica (IAM) 🤖")
    st.subheader("Evaluación Exhaustiva de Estudios de Mercado | Modelo Híbrido de Validación del Consumo")
    st.markdown("---")
    
    # Explicación Humana
    st.header("Propósito: Detector de Mentiras Metodológico")
    st.markdown("""
        Este software audita si un estudio de mercado tiene **Validez Conductual** al contrastar el **autorreporte** ($\mathbf{X}$) con la **acción real** ($\mathbf{Y}$), controlando el **sesgo cognitivo** ($\mathbf{M}$).
        
        **Instrucción de uso:** Evalúa el estudio que estás auditando y usa los resultados de sus análisis estadísticos para llenar la sección 1.
    """)
    
    st.markdown("---")
    
    # 1. MÉTRICAS OPERACIONALES Y CIFRAS DE CONTRASTE (Input Directo y Estadístico)
    st.header("1. Cifras de Contraste Requeridas (Output del Análisis Estadístico)")
    st.warning("Debe obtener estas cifras corriendo una Correlación y una Regresión Moderada en el estudio que está auditando.")
    
    col_n, col_r, col_beta = st.columns(3)
    
    with col_n:
        n_declarada = st.number_input(
            "Tamaño de la **Muestra Declarativa (N)**:", 
            min_value=1, value=150, step=10, help="Muestra de la Encuesta (X)."
        )
    
    with col_r:
        r_xy = st.number_input(
            "**Correlación $r$ (Intención $\mathbf{X} \\to$ Conducta $\mathbf{Y}$):**",
            min_value=-1.0, max_value=1.0, value=0.25, step=0.01,
            help="Mide la Brecha. Si es < 0.30, la brecha es alta. Debe buscar este valor en la sección de Resultados."
        )
    
    with col_beta:
        beta_m = st.number_input(
            "**Coeficiente $\\beta$ (Efecto Moderador $\mathbf{X} \\times \mathbf{M}$):**",
            min_value=-5.0, max_value=5.0, value=0.10, step=0.01,
            help="Mide si el sesgo (M) debilita la predicción. Si es **NEGATIVO y Significativo**, la Hipótesis H2 se confirma y el estudio es vulnerable."
        )
    
    st.markdown("---")

    # 2. CUESTIONARIO PONDERADO (1-5)
    st.header("2. Cuestionario Ponderado (Escala 1 a 5)")
    st.info("¡Sé honesto! La evaluación es crucial para la validez del estudio. **El *tooltip* de cada pregunta le indica dónde debe estar la evidencia en el estudio que está auditando.**")
    
    respuestas_usuario = {}
    ayudas_completas = {}

    # Generar los Sliders para cada pregunta
    for dimension, preguntas in CUESTIONARIO_IAM.items():
        st.markdown(f"### . {dimension}")
        
        for clave, detalles in preguntas.items():
            
            ayuda_completa = detalles["ayuda_humana"] + "\n\n**FUENTES DE EVIDENCIA (PARA CORROBORACIÓN):**\n" + detalles["fuente_dato"]
            ayudas_completas[clave] = ayuda_completa

            # Si es P1 o P7, mantenemos el valor por defecto en 1 para que el ajuste sea evidente después del cálculo
            default_value = 1
            if clave in ["P1_Conductual", "P7_Modelo_Moderador"]:
                # P1 y P7 se ajustarán automáticamente con el cálculo para reflejar la realidad estadística
                default_value = 1 
                
            respuestas_usuario[clave] = st.slider(
                label=detalles["pregunta"], 
                min_value=1, 
                max_value=5, 
                value=default_value,
                step=1,
                key=clave,
                help=ayuda_completa 
            )

    st.markdown("---")
    st.header("3. Resultado Final")
    
    if st.button("CALCULAR EL ÍNDICE DE AUTENTICIDAD METODOLÓGICA (IAM)"):
        
        # PASAR LOS NUEVOS INPUTS AL CÁLCULO
        iam, nivel, interpretacion, consejo_mejora, detalle_puntuacion_dict, peso_total_maximo, vulnerabilidad_metodologica = calcular_indice_iam(respuestas_usuario, r_xy, beta_m)
        
        for clave_pregunta, detalle in detalle_puntuacion_dict.items():
            clave_original = next(k for d, p in CUESTIONARIO_IAM.items() for k, v in p.items() if v['pregunta'] == clave_pregunta)
            detalle['Fuente de Evidencia'] = CUESTIONARIO_IAM[next(d for d, p in CUESTIONARIO_IAM.items() for k in p if k == clave_original)][clave_original]['fuente_dato']


        st.markdown("---")
        
        # --- EXPLICACIÓN DEL PORCENTAJE FINAL ---
        st.subheader("Fórmula de Normalización del IAM")
        st.latex(f"\\text{{IAM}} = \\left( \\frac{{\\text{{Puntuación Ponderada Obtenida}}}}{{\\text{{Puntuación Máxima Total}} \\left( 5 \\times \\sum \\text{{Pesos}} \\right)}} \\right) \\times 100 \\%")
        st.markdown(f"La puntuación máxima posible es de **{peso_total_maximo:.2f} puntos**. El IAM normaliza su resultado a una escala de 0 a 100%.")
        st.markdown("---")
        
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        with col_res1:
            st.metric(
                label="Índice de Autenticidad Metodológica (IAM)", 
                value=f"{iam:.2f} %",
                delta=nivel
            )
            
        with col_res2:
            st.metric(
                label="Vulnerabilidad Metodológica (Riesgo)",
                value=f"{vulnerabilidad_metodologica:.2f} %",
                delta="100% - IAM",
                delta_color="inverse"
            )
            
        with col_res3:
            st.metric(
                label="Correlación $\mathbf{r}$ ($\mathbf{X}, \mathbf{Y}$)",
                value=f"{r_xy:.2f}",
                delta="Brecha $\mathbf{X} \\to \mathbf{Y}$"
            )
            
        with col_res4:
            st.metric(
                label="Efecto Moderador $\\beta$ ($\mathbf{X} \\times \mathbf{M}$)",
                value=f"{beta_m:.2f}",
                delta="Impacto del Sesgo ($\mathbf{M}$) en la predicción"
            )

        st.subheader(f"Diagnóstico Metodológico: **{nivel}**")
        st.success(f"**Interpretación Humana:** {interpretacion}")
        
        # Consejos de Mejora
        st.markdown("---")
        st.subheader("🛠️ Plan de Mejora Humano")
        st.code(consejo_mejora, language=None)
        
        st.markdown("---")
        st.subheader("Tabla de Auditoría Ponderada")
        st.warning("Busque las puntuaciones bajas (1 o 2) en las preguntas con **Peso 4.0 o 4.5**; ahí reside el mayor riesgo de sesgo.")
        
        detalle_df = pd.DataFrame.from_dict(detalle_puntuacion_dict, orient='index')
        detalle_df = detalle_df.reset_index().rename(columns={'index': 'Criterio Evaluado'})
        
        def color_riesgo(row):
            if row['Respuesta (1-5)'] <= 2 and row['Peso'] >= 4.0:
                return ['background-color: #ffcccc'] * len(row) # Rojo claro para crítico
            elif row['Respuesta (1-5)'] <= 2 and row['Peso'] >= 3.0:
                return ['background-color: #ffffcc'] * len(row) # Amarillo claro para alto riesgo
            return [''] * len(row)

        st.dataframe(detalle_df[['Criterio Evaluado', 'Respuesta (1-5)', 'Peso', 'Puntuación Ponderada', 'Fuente de Evidencia']]
                     .style.apply(color_riesgo, axis=1), 
                     use_container_width=True)
        
if __name__ == '__main__':
    main()
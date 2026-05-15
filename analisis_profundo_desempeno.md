# 🎯 Análisis Estratégico Profundo — Desempeño y Talento

> **Examen Final — Dirección de Personas**
> Proceso seleccionado: **Desempeño y Talento**
> Base de datos: `Base_datos_CERTAMEN2_clean.xlsx`

---

## 1. Justificación de la Selección

El proceso de **Desempeño y Talento** fue seleccionado por ser el de mayor densidad relacional dentro del modelo de datos. Cuenta con **14 medidas DAX** ya definidas y permite cruces directos con al menos **12 variables** de la base:

| Variable Principal       | Variables con las que se cruza                                                 |
| ------------------------ | ------------------------------------------------------------------------------ |
| `Evaluacion_Desempeno` | Área, Nivel, Sede, Sexo, Antigüedad, Sueldo, Horas Capacitación, Engagement |
| `Evaluacion_Anterior`  | Delta de mejora/deterioro, segmentación temporal                              |
| `Potencial`            | Matriz 9-Box, planes de sucesión, retención de talento                       |
| `Engagement`           | Ausentismo, Accidentabilidad, Rotación, Satisfacción                         |
| `Ausentismo_Dias`      | Desempeño, Área, Sede, Tipo de Contrato                                      |
| `Accidentes_Laborales` | Área, Sede, Jornada, Modalidad de Trabajo                                     |

**Argumento estratégico:** El desempeño es el eje vertebral de la gestión de personas — un colaborador con bajo desempeño impacta en rotación, costos salariales, productividad y clima. Profundizar aquí permite generar recomendaciones accionables con mayor ROI organizacional.

---

## 2. Arquitectura de Filtros y Segmentaciones

### 2.1 Filtros Globales (presentes en todas las páginas)

| Filtro           | Tipo      | Valores                                                  | Propósito                        |
| ---------------- | --------- | -------------------------------------------------------- | --------------------------------- |
| **Área**  | Dropdown  | Todas las áreas de la organización                     | Comparación inter-departamental  |
| **Nivel**  | Multi-sel | Operativo, Analista, Prof. Senior, Jefatura, Gerencia... | Análisis por estrato jerárquico |
| **Sede**   | Dropdown  | Santiago, Valparaíso, Puerto Montt, etc.                | Dimensión geográfica            |
| **Estado** | Botones   | Activo / Desvinculado                                    | Incluir/excluir ex-empleados      |

### 2.2 Filtros Específicos del Análisis de Desempeño

| Filtro                       | Tipo     | Valores                         | Propósito                                   |
| ---------------------------- | -------- | ------------------------------- | -------------------------------------------- |
| **Potencial**          | Botones  | Alto / Medio / Bajo             | Segmentar por potencial de crecimiento       |
| **Rango Antigüedad**  | Lista    | <1, 1-3, 3-6, 6-10, 10+ años   | Correlacionar experiencia con rendimiento    |
| **Rango Edad**         | Lista    | 18-25, 26-35, 36-45, 46-55, 56+ | Análisis generacional                       |
| **Tipo Capacitación** | Dropdown | Interna, Externa, Mixta         | Impacto del tipo de formación en desempeño |
| **Sexo**               | Botones  | M / F / Otro                    | Equidad en evaluaciones                      |
| **Modalidad Trabajo**  | Botones  | Presencial / Híbrido / Remoto  | Impacto de modalidad en performance          |

### 2.3 Segmentaciones Calculadas (columnas DAX nuevas)

```dax
// --- Categoría de Desempeño ---
Categoria_Desempeno =
    SWITCH(
        TRUE(),
        Datos[Evaluacion_Desempeno] >= 4.5, "Excepcional",
        Datos[Evaluacion_Desempeno] >= 4.0, "Alto",
        Datos[Evaluacion_Desempeno] >= 3.0, "Adecuado",
        Datos[Evaluacion_Desempeno] >= 2.0, "En desarrollo",
        "Crítico"
    )

// --- Tendencia de Desempeño ---
Tendencia_Desempeno =
    SWITCH(
        TRUE(),
        Datos[Delta_Desempeno] > 0.5, "Mejora significativa",
        Datos[Delta_Desempeno] > 0, "Mejora leve",
        Datos[Delta_Desempeno] = 0, "Estable",
        Datos[Delta_Desempeno] > -0.5, "Deterioro leve",
        "Deterioro significativo"
    )

// --- Cuadrante 9-Box (texto) ---
Cuadrante_9Box =
    VAR _perf =
        SWITCH(
            TRUE(),
            Datos[Evaluacion_Desempeno] >= 4, "Alto",
            Datos[Evaluacion_Desempeno] >= 3, "Medio",
            "Bajo"
        )
    RETURN
        _perf & " / " & Datos[Potencial]

// --- Riesgo de Fuga (composite) ---
Riesgo_Fuga =
    SWITCH(
        TRUE(),
        Datos[Evaluacion_Desempeno] >= 4
            && Datos[Engagement] < 60, "Alto",
        Datos[Evaluacion_Desempeno] >= 3.5
            && Datos[Engagement] < 70, "Medio",
        "Bajo"
    )
```

---

## 3. KPIs Estratégicos

### 3.1 KPIs Primarios (Cards principales)

| # | KPI                     | Fórmula DAX              | Formato  | Target / Benchmark | Interpretación                        |
| - | ----------------------- | ------------------------- | -------- | ------------------ | -------------------------------------- |
| 1 | Evaluación Promedio    | `Evaluacion Promedio`   | ★ x/5.0 | ≥ 3.5             | Nivel general de rendimiento           |
| 2 | % Alto Desempeño (≥4) | `% Alto Desempeno`      | %        | ≥ 30%             | Proporción de top performers          |
| 3 | % Bajo Desempeño (<3)  | `% Bajo Desempeno`      | %        | ≤ 10%             | Proporción en zona crítica           |
| 4 | Engagement Promedio     | `Engagement Promedio`   | 0-100    | ≥ 75              | Compromiso organizacional              |
| 5 | Ausentismo Promedio     | `Ausentismo Promedio`   | días    | ≤ 5               | Proxy de satisfacción / salud laboral |
| 6 | Tasa Accidentabilidad   | `Tasa Accidentabilidad` | %        | ≤ 3%              | Seguridad laboral                      |

### 3.2 KPIs Secundarios (Análisis profundo)

| #  | KPI                   | Fórmula DAX                     | Propósito                     |
| -- | --------------------- | -------------------------------- | ------------------------------ |
| 7  | Variación Desempeño | `Variacion Desempeno Promedio` | Tendencia periodo a periodo    |
| 8  | % Mejoraron           | `% Mejoraron Desempeno`        | Evolución positiva            |
| 9  | % Empeoraron          | `% Empeoraron Desempeno`       | Señal de alerta               |
| 10 | 9-Box Stars           | `9Box Stars`                   | Talento clave a retener        |
| 11 | 9-Box Riesgo          | `9Box Riesgo`                  | Colaboradores en zona crítica |

### 3.3 KPIs Avanzados (crear para el examen)

```dax
// --- Spread de Desempeño (desviación) ---
Spread Desempeno =
    VAR _avg = AVERAGE(Datos[Evaluacion_Desempeno])
    VAR _stdev =
        SQRT(
            AVERAGEX(
                Datos,
                (Datos[Evaluacion_Desempeno] - _avg) ^ 2
            )
        )
    RETURN _stdev

// --- Ratio Engagement / Desempeño ---
Ratio Engagement Desempeno =
    DIVIDE(
        AVERAGE(Datos[Engagement]),
        AVERAGE(Datos[Evaluacion_Desempeno]) * 20,
        0
    )

// --- % Talento en Riesgo de Fuga ---
Pct Riesgo Fuga =
    DIVIDE(
        COUNTROWS(
            FILTER(Datos,
                Datos[Evaluacion_Desempeno] >= 4 &&
                Datos[Engagement] < 60
            )
        ),
        COUNTROWS(
            FILTER(Datos, Datos[Evaluacion_Desempeno] >= 4)
        ),
        0
    )

// --- Correlación Capacitación-Desempeño (gap) ---
Gap Capacitacion Desempeno =
    [Horas Cap Alto Desempeno] - [Horas Cap Bajo Desempeno]

// --- Índice de Clima Laboral Compuesto ---
Indice Clima =
    (AVERAGE(Datos[Engagement]) * 0.5)
    + ((1 - DIVIDE(AVERAGE(Datos[Ausentismo_Dias]), 30, 0)) * 100 * 0.3)
    + ((1 - [Tasa Accidentabilidad]) * 100 * 0.2)
```

---

## 4. Diseño de Páginas del Dashboard

El análisis profundo se estructura en **4 páginas** dentro de Power BI:

### 4.1 Página A — Panorama de Desempeño

**Objetivo:** Vista ejecutiva del estado actual del desempeño organizacional.

| Zona               | Visual                                     | Datos                                                          | Tipo Chart                       |
| ------------------ | ------------------------------------------ | -------------------------------------------------------------- | -------------------------------- |
| **R1**       | 6 Cards KPI                                | Eval. Promedio, % Alto, % Bajo, Engagement, Ausentismo, Accid. | Cards con condicional color      |
| **Centro-L** | Evaluación por Área                      | `Evaluacion Promedio` × `Area`                            | **Clustered Bar Chart**    |
| **Centro-R** | Distribución por Categoría de Desempeño | `Categoria_Desempeno` count                                  | **Donut Chart**            |
| **Bottom-L** | Desempeño por Nivel Jerárquico           | `Evaluacion Promedio` × `Nivel`                           | **Bar Chart** (horizontal) |
| **Bottom-R** | Desempeño por Sede                        | `Evaluacion Promedio` × `Sede`                            | **Column Chart**           |
| **Lateral**  | Slicers: Área, Nivel, Sede, Estado        | —                                                             | Slicers verticales               |

**Storytelling:** *"¿Dónde estamos hoy? ¿Qué áreas y niveles concentran el mayor y menor desempeño?"*

---

### 4.2 Página B — Evolución, Tendencias y Ranking (con Ribbon Chart)

**Objetivo:** Comparar evaluación actual vs. anterior, visualizar cómo cambiaron los rankings de cada área, e identificar patrones de mejora/deterioro.

| Zona                  | Visual                                         | Datos                                                                | Tipo Chart                               |
| --------------------- | ---------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------- |
| **R1**          | 4 Cards                                        | Δ Promedio, % Mejoraron, % Empeoraron, % Estables                   | Cards con flechas ↑↓                   |
| **Centro-Full** | 🎀**Ranking de Áreas: Antes vs. Ahora** | `Evaluacion Promedio` × `Area`, con eje de categoría = Periodo | **🎀 Ribbon Chart**                |
| **Bottom-L**    | Waterfall de Cambio                            | Delta por Área (contribución al cambio global)                     | **Waterfall Chart**                |
| **Bottom-C**    | Distribución de Tendencia                     | `Tendencia_Desempeno` count                                        | **Stacked Bar Chart** (divergente) |
| **Bottom-R**    | Scatter: Eval Anterior vs. Actual              | Ejes X/Y con `Evaluacion_Anterior` vs `Evaluacion_Desempeno`     | **Scatter Plot** + línea 45°     |

**Storytelling:** *"El Ribbon Chart revela que el Área X pasó del puesto 1 al 4 en desempeño — las cintas cruzadas muestran visualmente la magnitud del cambio. ¿Qué ocurrió allí? ¿Estamos mejorando o empeorando como organización?"*

**Insight clave del Ribbon Chart:** Las cintas que se cruzan entre los dos periodos hacen inmediatamente visible qué áreas escalaron posiciones y cuáles cayeron, sin necesidad de leer números. El ancho de la cinta representa la proporción de headcount del área.

**Insight clave del Scatter:** Los puntos sobre la línea de 45° mejoraron; los que están bajo, empeoraron. Colorear por `Area` o `Nivel` para identificar patrones.

---

### 4.3 Página C — Matriz 9-Box y Talento

**Objetivo:** Mapear talento organizacional y detectar riesgos de fuga.

| Zona               | Visual                            | Datos                                                             | Tipo Chart                              |
| ------------------ | --------------------------------- | ----------------------------------------------------------------- | --------------------------------------- |
| **R1**       | 4 Cards                           | 9-Box Stars, 9-Box Riesgo, % Potencial Alto, % Riesgo Fuga        | Cards                                   |
| **Centro**   | Matriz 9-Box                      | Eje X:`Evaluacion_Desempeno`, Eje Y: `Potencial`, Size: Count | **Scatter Plot** (con cuadrantes) |
| **Bottom-L** | Distribución por Cuadrante 9-Box | `Cuadrante_9Box` count                                          | **Treemap**                       |
| **Bottom-C** | Engagement por Cuadrante          | `Engagement` avg × `Cuadrante_9Box`                          | **Heatmap / Matrix** condicional  |
| **Bottom-R** | Riesgo de Fuga por Área          | `Riesgo_Fuga` = "Alto" count × `Area`                        | **Stacked Bar** (rojo/amarillo)   |

**Storytelling:** *"¿Quiénes son nuestras estrellas y dónde están? ¿Cuántos talentos están en riesgo de irse por bajo engagement?"*

**Configuración del 9-Box en Power BI:**

1. Scatter Plot con `Evaluacion_Desempeno` en X, codificación numérica de `Potencial` en Y
2. Agregar líneas de referencia constantes en X=3 y X=4 (separar bajo/medio/alto desempeño)
3. Agregar líneas de referencia en Y para separar bajo/medio/alto potencial
4. Colorear burbujas por `Area`
5. Tamaño de burbuja = headcount del segmento

---

### 4.4 Página D — Cruces Estratégicos

**Objetivo:** Revelar relaciones causales entre desempeño y otras variables de gestión.

| Zona               | Visual                              | Datos                                              | Tipo Chart                      |
| ------------------ | ----------------------------------- | -------------------------------------------------- | ------------------------------- |
| **R1**       | 3 Cards                             | Gap Cap-Desemp, Ratio Eng/Desemp, Índice Clima    | Cards                           |
| **Centro-L** | Capacitación vs. Desempeño        | `Horas_Capacitacion` vs `Evaluacion_Desempeno` | **Scatter + Trend Line**  |
| **Centro-R** | Engagement vs. Desempeño           | `Engagement` vs `Evaluacion_Desempeno`         | **Scatter + Trend Line**  |
| **Bottom-L** | Desempeño vs. Sueldo Base          | `Sueldo_Base` × `Categoria_Desempeno`         | **Box Plot / Violin**     |
| **Bottom-C** | Ausentismo vs. Desempeño           | `Ausentismo_Dias` avg × `Categoria_Desempeno` | **Bar Chart** (invertido) |
| **Bottom-R** | Desempeño por Modalidad de Trabajo | `Evaluacion Promedio` × `Modalidad_Trabajo`   | **Column Chart**          |

**Storytelling:** *"¿La capacitación realmente mejora el desempeño? ¿Los colaboradores mejor pagados rinden más? ¿El teletrabajo afecta la performance?"*

---

## 5. Charts Clave para la Profundización

### 5.1 Chart Estrella: Scatter 9-Box Interactivo

```
Configuración:
  - Eje X: Evaluacion_Desempeno (1-5)
  - Eje Y: Potencial codificado (Bajo=1, Medio=2, Alto=3)
  - Tamaño burbuja: Headcount del segmento
  - Color: Area
  - Tooltip: Nombre, Cargo, Engagement, Horas Cap.
  - Líneas de referencia: X=3, X=4, Y=1.5, Y=2.5
  - Cross-filter: Al hacer clic, filtra toda la página
```

### 5.2 Diverging Bar: Mejoraron vs. Empeoraron por Área

```
Configuración:
  - Eje Y: Area
  - Barras verdes (derecha): % que mejoró evaluación
  - Barras rojas (izquierda): % que empeoró
  - Ordenar por magnitud del cambio neto
  - Tooltips: n absoluto, delta promedio
```

### 5.3 Combo Chart: Desempeño + Engagement + Ausentismo

```
Configuración:
  - Eje X: Area
  - Columnas: Evaluacion Promedio (barra azul)
  - Línea 1: Engagement Promedio (línea cian)
  - Línea 2: Ausentismo Promedio (línea roja, eje secundario invertido)
  - Propósito: ver la triple correlación en un solo visual
```

### 5.4 Heatmap: Desempeño × Nivel × Área

```
Configuración:
  - Filas: Area
  - Columnas: Nivel
  - Valor: Evaluacion Promedio
  - Formato condicional: Rojo (<3.0) → Amarillo (3.0-3.9) → Verde (≥4.0)
  - Propósito: identificar "puntos calientes" de bajo desempeño
```

### 5.5 Waterfall: Contribución al Cambio de Desempeño Global

```
Configuración:
  - Categoría: Area
  - Valor: Contribución ponderada al delta de desempeño global
  - Inicio: Evaluación Anterior Promedio (global)
  - Final: Evaluación Actual Promedio (global)
  - Verde: áreas que contribuyeron positivamente
  - Rojo: áreas que arrastran el promedio hacia abajo
```

### 5.6 🎀 Ribbon Chart: Ranking de Desempeño por Área (Antes → Ahora)

El **Ribbon Chart** es la visualización estrella de la Página B. Muestra cómo cada área se posiciona en el ranking de desempeño promedio en dos periodos (evaluación anterior vs. actual), y las cintas que conectan ambos periodos revelan visualmente los cambios de posición.

#### Preparación de datos

Para alimentar el Ribbon Chart se necesita una tabla auxiliar tipo "unpivot" con dos filas por Área:

```dax
// --- Tabla auxiliar para Ribbon Chart (crear como tabla calculada) ---
Ribbon_Desempeno =
    VAR _anterior =
        ADDCOLUMNS(
            SUMMARIZE(Datos, Datos[Area]),
            "Periodo", "Anterior",
            "Eval_Promedio",
                CALCULATE(AVERAGE(Datos[Evaluacion_Anterior]))
        )
    VAR _actual =
        ADDCOLUMNS(
            SUMMARIZE(Datos, Datos[Area]),
            "Periodo", "Actual",
            "Eval_Promedio",
                CALCULATE(AVERAGE(Datos[Evaluacion_Desempeno]))
        )
    RETURN
        UNION(_anterior, _actual)
```

#### Configuración en Power BI

```
Configuración del Ribbon Chart:
  ──────────────────────────────────────────────────────────
  Visual: Ribbon Chart (nativo en Power BI)
  ──────────────────────────────────────────────────────────
  Axis (Eje X):      Ribbon_Desempeno[Periodo]
                      → Valores: "Anterior", "Actual"
                      → Orden: Anterior primero

  Legend (Leyenda):   Ribbon_Desempeno[Area]
                      → Cada área = una cinta de color distinto

  Values (Valores):   Ribbon_Desempeno[Eval_Promedio]
                      → Determina la posición (ranking) en cada periodo
  ──────────────────────────────────────────────────────────

  Formato recomendado:
  ──────────────────────────────────────────────────────────
  - Ribbons → Spacing: 5px (para que las cintas no se peguen)
  - Ribbons → Transparency: 25% (cintas semi-transparentes)
  - Data labels → ON (mostrar el valor de evaluación)
  - Title: "Evolución del Ranking de Desempeño por Área"
  - Colores: Usar la paleta corporativa del tema RRHH
  - Tooltip personalizado:
      → Área, Eval Promedio, Ranking, Delta vs periodo anterior
  ──────────────────────────────────────────────────────────

  Lectura del visual:
  ──────────────────────────────────────────────────────────
  - Cintas que SUBEN del periodo Anterior al Actual
    = áreas que mejoraron su posición relativa (positivo)

  - Cintas que BAJAN
    = áreas que perdieron posiciones (alerta)

  - Cintas que se CRUZAN con muchas otras
    = cambios dramáticos de ranking (requieren investigación)

  - Ancho de la cinta
    = proporción del headcount del área (más ancha = más gente)
  ──────────────────────────────────────────────────────────
```

#### Variante avanzada: Ribbon por Nivel Jerárquico

Para un análisis más granular, se puede crear un segundo Ribbon Chart que muestre el ranking por **Nivel** en vez de Área:

```dax
// --- Ribbon por Nivel ---
Ribbon_Desempeno_Nivel =
    VAR _anterior =
        ADDCOLUMNS(
            SUMMARIZE(Datos, Datos[Nivel]),
            "Periodo", "Anterior",
            "Eval_Promedio",
                CALCULATE(AVERAGE(Datos[Evaluacion_Anterior]))
        )
    VAR _actual =
        ADDCOLUMNS(
            SUMMARIZE(Datos, Datos[Nivel]),
            "Periodo", "Actual",
            "Eval_Promedio",
                CALCULATE(AVERAGE(Datos[Evaluacion_Desempeno]))
        )
    RETURN
        UNION(_anterior, _actual)
```

> **💡 Tip para la presentación:** El Ribbon Chart es extremadamente efectivo para storytelling porque los cruces de cintas generan un impacto visual inmediato — el evaluador puede ver *sin leer números* qué áreas subieron y cuáles cayeron. Usar esto como el "momento wow" de la presentación de 10 min.

---

## 6. Medidas DAX Adicionales para el Análisis

```dax
// --- Evaluación Promedio por Modalidad ---
Eval Promedio Modalidad =
    CALCULATE(
        AVERAGE(Datos[Evaluacion_Desempeno]),
        ALLEXCEPT(Datos, Datos[Modalidad_Trabajo])
    )

// --- Brecha de Desempeño por Género ---
Brecha Desempeno Genero =
    VAR _evalH =
        CALCULATE(AVERAGE(Datos[Evaluacion_Desempeno]), Datos[Sexo] = "M")
    VAR _evalM =
        CALCULATE(AVERAGE(Datos[Evaluacion_Desempeno]), Datos[Sexo] = "F")
    RETURN
        _evalH - _evalM

// --- % Feedback 360 Completo ---
Pct Feedback Completo =
    DIVIDE(
        COUNTROWS(FILTER(Datos, Datos[Feedback_360] = "Sí")),
        COUNTROWS(Datos),
        0
    )

// --- Desempeño Promedio con Feedback vs Sin ---
Eval Con Feedback =
    CALCULATE(
        AVERAGE(Datos[Evaluacion_Desempeno]),
        Datos[Feedback_360] = "Sí"
    )

Eval Sin Feedback =
    CALCULATE(
        AVERAGE(Datos[Evaluacion_Desempeno]),
        Datos[Feedback_360] = "No"
    )
```

---

## 7. Storytelling Visual — Guion de Presentación (10 min)

| Min  | Página | Narrativa                                                                                                                         |
| ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 0-2  | A       | "Nuestro desempeño promedio es X/5. El Y% son top performers, pero el Z% está en zona crítica."                                |
| 2-4  | B       | "El Ribbon Chart muestra que el Área X escaló del puesto 5 al 2, mientras que Q cayó 3 posiciones. El W% mejoró globalmente." |
| 4-6  | C       | "La Matriz 9-Box revela N estrellas. Alarmantemente, el P% de ellas tiene engagement bajo (<60)."                                 |
| 6-8  | D       | "Los datos muestran que más capacitación sí correlaciona con mejor desempeño. El gap es de X hrs."                            |
| 8-10 | —      | Recomendaciones estratégicas + cierre.                                                                                           |

---

## 8. Recomendaciones Estratégicas para RRHH

### Basadas en los patrones esperados del análisis:

| # | Hallazgo Probable                                        | Recomendación                                                                      | Referencia de Mercado                                     |
| - | -------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 1 | Alto desempeño + bajo engagement = riesgo de fuga       | Programa de retención diferenciado (stay interviews, bonos de retención)          | Google "gDNA" — encuestas predictivas de salida          |
| 2 | Capacitación correlaciona con mejor desempeño          | Aumentar horas mínimas de capacitación a 40 hrs/año, focalizando en bajo desemp. | LinkedIn Learning: empresas con cultura L&D retienen 50%+ |
| 3 | Dispersión de evaluaciones entre áreas                 | Calibración inter-áreas de evaluaciones (comités de calibración)                | McKinsey: calibración reduce sesgo en 35%                |
| 4 | Bajo desempeño concentrado en ciertos niveles           | Planes de desarrollo individual (PDI) con KPIs a 90 días                           | Deloitte: "Performance Management Reimagined"             |
| 5 | Brecha de desempeño por género                         | Auditoría de sesgo en evaluaciones + formación a evaluadores                      | Harvard BR: sesgo inconsciente en performance reviews     |
| 6 | Ausentismo alto en áreas de bajo desempeño             | Programa de bienestar focalizado + diagnóstico de clima por área                  | Great Place to Work: bienestar reduce ausentismo en 41%   |
| 7 | Modalidad remota con evaluaciones diferentes             | Estandarizar criterios de evaluación cross-modalidad                               | Gartner: "Hybrid Work Performance Framework"              |
| 8 | 9-Box Riesgo (bajo desemp. + bajo potencial) concentrado | Plan de desvinculación asistida o reubicación interna                             | Proceso de gestión del talento de Unilever               |

---

## 9. Checklist de Implementación

- [ ] Crear 4 nuevas columnas calculadas (Categoría Desempeño, Tendencia, Cuadrante 9-Box, Riesgo Fuga)
- [ ] Crear las 7 medidas DAX adicionales propuestas
- [ ] Construir **Página A**: Panorama (6 cards + 4 charts + slicers)
- [ ] Construir **Página B**: Evolución (4 cards + Ribbon Chart + 3 charts complementarios)
- [ ] Crear tabla calculada `Ribbon_Desempeno` para alimentar el Ribbon Chart
- [ ] Construir **Página C**: 9-Box (4 cards + scatter + treemap + heatmap + stacked bar)
- [ ] Construir **Página D**: Cruces (3 cards + 5 charts con scatter + trend lines)
- [ ] Configurar cross-filtering entre todas las páginas
- [ ] Agregar drill-through desde Página A hacia B, C y D
- [ ] Configurar tooltips personalizados en scatter plots
- [ ] Ensayar storytelling de 10 minutos con el equipo
- [ ] Validar que todos los slicers afecten correctamente los visuals

# 📊 Plan de Diseño — Dashboard Ejecutivo RRHH

## 🎨 Paleta de Colores Corporativa

| Rol | Color | Hex | Uso |
|-----|-------|-----|-----|
| **Primary** | Navy Oscuro | `#1B2A4A` | Headers, fondos de tarjetas principales |
| **Secondary** | Azul Medio | `#2E5C8A` | Barras, gráficos principales |
| **Accent 1** | Azul Claro | `#4A90D9` | Series secundarias, hover |
| **Accent 2** | Cian | `#00B4D8` | Destacados, líneas |
| **Accent 3** | Azul Hielo | `#87CEEB` | Fondos de cards, series terciarias |
| **Positivo** | Verde | `#27AE60` | KPIs positivos, mejoras |
| **Negativo** | Rojo | `#E74C3C` | Alertas, brechas, caídas |
| **Fondo** | Gris Claro | `#F0F4F8` | Fondo general del reporte |
| **Texto** | Gris Oscuro | `#2C3E50` | Títulos y etiquetas |

> **Tip:** En Power BI: **View → Themes → Customize current theme** para aplicar estos colores globalmente.

---

## 📐 Estructura de Páginas (6 páginas)

El dashboard se organiza en **6 páginas** alineadas a los 6 procesos RRHH del certamen:

| # | Página | Propósito |
|---|--------|-----------|
| 1 | **Dashboard Ejecutivo** | Vista panorámica con KPIs clave de cada pilar |
| 2 | **Análisis de Rotación** | Tasas, motivos, reemplazo, tendencias |
| 3 | **Equidad Salarial** | Brechas de género, distribución por nivel |
| 4 | **Capacitación y Desarrollo** | Cobertura, horas, correlación con desempeño |
| 5 | **Desempeño y Talento** | Evaluaciones, 9-Box, engagement |
| 6 | **Diversidad e Inclusión** | Género, nacionalidad, techo de cristal |

---

## 📄 Página 1: Dashboard Ejecutivo RRHH

### Layout

| Zona | Elemento | Medida DAX | Visual |
|------|----------|------------|--------|
| Header | Título "Dashboard Ejecutivo RRHH" | — | Texto con fondo navy |
| R1-C1 | Headcount | `Headcount` | Card |
| R1-C2 | Tasa Rotación | `Tasa Rotacion Global` | Card (% con indicador rojo) |
| R1-C3 | Brecha Salarial | `Brecha Salarial Genero` | Card (%) |
| R1-C4 | Evaluación | `Evaluacion Promedio` | Card (x/5.0) |
| R1-C5 | Engagement | `Engagement Promedio` | Card con gauge |
| R1-C6 | Cobertura Cap. | `Cobertura Capacitacion` | Card (%) |
| R2-L | Distribución por Área | `Headcount` × `Area` | Stacked bar chart |
| R2-R | Distribución por Género | `Pct Mujeres`, `Pct Hombres` | Donut chart |
| R3-L | Rotación por Motivo | `Motivo_Salida` count | Horizontal bar |
| R3-R | Sueldo por Nivel | `Sueldo Base Promedio` × `Nivel` | Combo bar+line |
| Lateral | Filtros: Área, Sede, Nivel | — | Slicers verticales |

### Slicers para esta página
- **Área** (lista)
- **Sede** (dropdown)
- **Nivel** (lista)

---

## 📄 Página 2: Análisis de Rotación

### Layout

| Zona | Elemento | Medida DAX | Visual |
|------|----------|------------|--------|
| R1-C1 | Total Desvinculados | `Total Desvinculados` | Card |
| R1-C2 | Rotación Global | `Tasa Rotacion Global` | Card (%) |
| R1-C3 | Rotación Voluntaria | `Tasa Rotacion Voluntaria` | Card (%) |
| R1-C4 | Rotación Involuntaria | `Tasa Rotacion Involuntaria` | Card (%) |
| Centro-L | Motivos de Salida | `Motivo_Salida` count | Waterfall/bar chart |
| Centro-R top | Rotación por Área | `Tasa Rotacion Area` × `Area` | Clustered bar |
| Centro-R bot | Índice de Reemplazo | `Indice Reemplazo` | Gauge (target 100%) |
| Bottom-L | Rotación Sede × Área | Heatmap matrix | Matrix con formato condicional |
| Bottom-R | Tipo de Rotación | Vol. vs Invol. | Donut chart |

### Slicers
- **Estado** (Activo / Desvinculado)
- **Sede** (dropdown)
- **Área** (dropdown)

---

## 📄 Página 3: Equidad Salarial

### Layout

| Zona | Elemento | Medida DAX | Visual |
|------|----------|------------|--------|
| R1-C1 | Sueldo Promedio | `Sueldo Base Promedio` | Card ($) |
| R1-C2 | Mediana Salarial | `Sueldo Base Mediana` | Card ($) |
| R1-C3 | Brecha de Género | `Brecha Salarial Genero` | Card (% con flecha) |
| R1-C4 | Masa Salarial | `Masa Salarial Total` | Card ($) |
| Centro-L | Sueldo por Nivel y Género | `Sueldo Base Promedio` × `Nivel` × `Sexo` | Grouped bar chart |
| Centro-R | Bono Variable por Área | `Bono Variable Promedio` × `Area` | Bar chart / Box plot |
| Bottom-L | Brecha Salarial por Nivel | `Brecha Salarial Genero` × `Nivel` | Horizontal bar (%) |
| Bottom-R | Sueldo vs Antigüedad | `Sueldo_Base` vs `Antiguedad_Anios` × `Sexo` | Scatter plot |

### Slicers
- **Área** (dropdown)
- **Nivel** (multi-select)
- **Sexo** (botones)

---

## 📄 Página 4: Capacitación y Desarrollo

### Layout

| Zona | Elemento | Medida DAX | Visual |
|------|----------|------------|--------|
| R1-C1 | Promedio Horas | `Promedio Horas Capacitacion` | Card |
| R1-C2 | Cursos Promedio | `Promedio Cursos Tomados` | Card |
| R1-C3 | Cobertura | `Cobertura Capacitacion` | Card (%) |
| R1-C4 | Sin Capacitación | `Pct Sin Capacitacion` | Card (% rojo) |
| Centro-L | Horas por Área | `Promedio Horas Capacitacion` × `Area` | Bar chart |
| Centro-R top | Tipo de Capacitación | `Tipo_Capacitacion` distribution | Donut chart |
| Centro-R bot | Alto vs Bajo Desempeño | `Horas Cap Alto Desempeno` vs `Horas Cap Bajo Desempeno` | Comparison bars |
| Bottom-L | Correlación Horas-Evaluación | `Horas_Capacitacion` vs `Evaluacion_Desempeno` | Scatter + trend line |
| Bottom-R | Cap. por Nivel | `Horas_Capacitacion` × `Nivel` × `Tipo_Capacitacion` | Stacked bar |

### Slicers
- **Área** (lista)
- **Tipo Capacitación** (lista)

---

## 📄 Página 5: Desempeño y Talento

### Layout

| Zona | Elemento | Medida DAX | Visual |
|------|----------|------------|--------|
| R1-C1 | Evaluación Promedio | `Evaluacion Promedio` | Card (★ x/5.0) |
| R1-C2 | % Alto Desempeño | `Pct Alto Desempeno` | Card (%) |
| R1-C3 | % Bajo Desempeño | `Pct Bajo Desempeno` | Card (%) |
| R1-C4 | Engagement | `Engagement Promedio` | Card |
| R1-C5 | Ausentismo | `Ausentismo Promedio` | Card (días) |
| Centro-L | Eval Actual vs Anterior | `Evaluacion Promedio` vs `Evaluacion Anterior` × `Area` | Grouped column |
| Centro-R | Matriz 9-Box | `Evaluacion_Desempeno` × `Potencial` | Scatter/Matrix coloreada |
| Bottom-L | Mejoraron vs Empeoraron | `Pct Mejoraron` vs `Pct Empeoraron` | Diverging bar (verde/rojo) |
| Bottom-C | Engagement | `Engagement Promedio` | Gauge (target: 75) |
| Bottom-R | Accidentabilidad | `Tasa Accidentabilidad` × `Area` | Bar chart |

### Slicers
- **Área** (dropdown)
- **Nivel** (dropdown)
- **Potencial** (botones)

---

## 📄 Página 6: Diversidad e Inclusión

### Layout

| Zona | Elemento | Medida DAX | Visual |
|------|----------|------------|--------|
| R1-C1 | % Mujeres | `Pct Mujeres` | Card (%) |
| R1-C2 | Índice Paridad | `Indice Paridad Genero` | Card (0-1) |
| R1-C3 | Nacionalidades | `Nacionalidades Distintas` | Card (#) |
| R1-C4 | % Extranjeros | `Pct Extranjeros` | Card (%) |
| R1-C5 | % Discapacidad | `Pct Con Discapacidad` | Card (%) |
| Centro-L | Género por Nivel | `Sexo` × `Nivel` | 100% Stacked bar |
| Centro-R top | Nacionalidades | `Nacionalidad` distribution | Treemap |
| Centro-R bot | Mujeres en Liderazgo | `Pct Mujeres Jefatura/Gerencia/Directivo` | 3 mini gauges |
| Bottom-L | Brecha por Nivel y Género | Matrix `Nivel` × métricas salariales | Table con formato condicional |
| Bottom-R | Techo de Cristal | `Techo de Cristal` index | KPI con target |

### Slicers
- **Área** (dropdown)
- **Sede** (dropdown)

---

## 🔧 Guía de Implementación en Power BI Online

### Paso 1: Crear las páginas
1. En Power BI Online → abrir el reporte del modelo `main`
2. Click `+` en la barra de pestañas para crear 6 páginas
3. Renombrar cada pestaña según la tabla de arriba

### Paso 2: Configurar el tema
1. **View → Themes → Customize current theme**
2. Configurar colores de datos:
   - Color 1: `#1B2A4A` (Navy)
   - Color 2: `#2E5C8A` (Azul medio)
   - Color 3: `#4A90D9` (Azul claro)
   - Color 4: `#00B4D8` (Cian)
   - Color 5: `#87CEEB` (Azul hielo)
   - Color 6: `#27AE60` (Verde)
   - Color 7: `#E74C3C` (Rojo)
   - Color 8: `#F39C12` (Naranja)
3. Fondo de página: `#F0F4F8`
4. Fuente: **Segoe UI** (default Power BI)

### Paso 3: Construir página por página
Para cada visual:
1. Seleccionar el tipo de visual desde el panel de visualizaciones
2. Arrastrar las medidas DAX correspondientes desde el panel Data
3. Configurar tamaño y posición según el mockup
4. Aplicar formato de colores del tema

### Paso 4: Agregar interactividad
- Configurar **cross-filtering** entre visuales
- Añadir **tooltips** personalizados en los gráficos principales
- Configurar **drill-through** de la página ejecutiva a las páginas de detalle

> **Importante:** Orden recomendado de construcción: Página 1 (Ejecutivo) → Página 2 (Rotación) → Página 3 (Equidad) → Página 5 (Desempeño) → Página 4 (Capacitación) → Página 6 (Diversidad)

---

## 📋 Checklist de Implementación

- [ ] Crear 6 pestañas/páginas en el reporte
- [ ] Aplicar tema de colores azulado
- [ ] Configurar fondo `#F0F4F8`
- [ ] **Página 1**: 6 cards + 4 charts + 3 slicers
- [ ] **Página 2**: 4 cards + 4 charts + 3 slicers
- [ ] **Página 3**: 4 cards + 4 charts + 3 slicers
- [ ] **Página 4**: 4 cards + 5 charts + 2 slicers
- [ ] **Página 5**: 5 cards + 5 charts + 3 slicers
- [ ] **Página 6**: 5 cards + 5 charts + 2 slicers
- [ ] Configurar cross-filtering
- [ ] Revisar formato de números (moneda CLP, porcentajes)
- [ ] Añadir títulos descriptivos a cada visual

---

## 📎 Archivo de Tema JSON (para importar en Power BI)

Para aplicar la paleta completa automáticamente, importa el siguiente JSON como tema personalizado en Power BI (View → Themes → Browse for themes):

```json
{
  "name": "RRHH Dashboard Azulado",
  "dataColors": [
    "#1B2A4A",
    "#2E5C8A",
    "#4A90D9",
    "#00B4D8",
    "#87CEEB",
    "#27AE60",
    "#E74C3C",
    "#F39C12"
  ],
  "background": "#F0F4F8",
  "foreground": "#2C3E50",
  "tableAccent": "#2E5C8A",
  "visualStyles": {
    "*": {
      "*": {
        "general": [{
          "responsive": true
        }],
        "title": [{
          "fontColor": {"solid": {"color": "#2C3E50"}},
          "fontSize": 12,
          "fontFamily": "Segoe UI"
        }],
        "labels": [{
          "fontColor": {"solid": {"color": "#2C3E50"}},
          "fontSize": 10,
          "fontFamily": "Segoe UI"
        }]
      }
    }
  }
}
```

Para usar: Guarda este JSON como `tema_rrhh.json` y en Power BI ve a **View → Themes → Browse for themes** → selecciona el archivo.

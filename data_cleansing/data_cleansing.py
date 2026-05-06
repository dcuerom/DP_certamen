"""
Data Cleansing — Base datos CERTAMEN2.xlsx
==========================================
Aborda las 10 prioridades detectadas en el EDA:
  1. Estandarizar Sexo (7 formatos → 3)
  2. Normalizar Area (12 valores → 6)
  3. Corregir Sueldo Total inconsistente
  4. Resolver Activos con Fecha_Salida
  5. Eliminar RUTs duplicados (conservar primera aparición)
  6. Corregir fechas invertidas (Salida < Ingreso)
  7. Convertir registros USD → CLP
  8. Corregir ausentismo negativo
  9. Imputar nulos en variables clave
 10. Homologar escala de evaluación
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ─── Configuración ───────────────────────────────────────────────
INPUT_FILE  = "Base datos CERTAMEN2.xlsx"
OUTPUT_FILE = "Base_datos_CERTAMEN2_clean.xlsx"
LOG_FILE    = "data_cleansing_log.txt"
TC_USD_CLP  = 950  # Tipo de cambio referencial USD→CLP

# ─── Carga ───────────────────────────────────────────────────────
df = pd.read_excel(INPUT_FILE, sheet_name=0)
n_original = len(df)
log_lines = []

def log(msg):
    """Imprime y acumula en log."""
    print(msg)
    log_lines.append(msg)

log(f"{'='*60}")
log(f"DATA CLEANSING — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"{'='*60}")
log(f"Archivo fuente : {INPUT_FILE}")
log(f"Registros      : {n_original}")
log(f"Columnas       : {len(df.columns)}")
log("")

# ═══════════════════════════════════════════════════════════════════
# 1. ESTANDARIZAR SEXO  (7 formatos → 3 categorías)
# ═══════════════════════════════════════════════════════════════════
log("─── 1. Estandarizar campo 'Sexo' ───")
sexo_map = {
    'M': 'M', 'F': 'F', 'Otro': 'Otro',
    'male': 'M', 'female': 'F',
    'Masculino': 'M', 'Femenino': 'F',
}
before = df['Sexo'].value_counts(dropna=False).to_dict()
df['Sexo'] = df['Sexo'].map(sexo_map)
after = df['Sexo'].value_counts(dropna=False).to_dict()
log(f"  Antes : {before}")
log(f"  Después: {after}")
# Conteo de cambios reales (excluir los que ya eran M, F, Otro)
changed = sum(v for k, v in before.items() if k not in ['M', 'F', 'Otro', np.nan, None])
log(f"  → {changed} valores remapeados")
log("")

# ═══════════════════════════════════════════════════════════════════
# 2. NORMALIZAR AREA  (12 valores → 6 categorías)
# ═══════════════════════════════════════════════════════════════════
log("─── 2. Normalizar campo 'Area' ───")
area_map = {
    'Comercial':        'Comercial',
    'Finanzas':         'Finanzas',
    'Operaciones':      'Operaciones',
    'Ops':              'Operaciones',
    'Tecnología':       'Tecnología',
    'Tecnologia':       'Tecnología',
    'TI':               'Tecnología',
    'Personas':         'Personas',
    'RRHH':             'Personas',
    'Recursos Humanos': 'Personas',
    'Administración':   'Administración',
    'Administracion':   'Administración',
}
before_area = df['Area'].value_counts(dropna=False).to_dict()
df['Area'] = df['Area'].map(area_map)
after_area = df['Area'].value_counts(dropna=False).to_dict()
log(f"  Antes : {len(before_area)} categorías")
log(f"  Después: {len(after_area)} categorías → {list(after_area.keys())}")
remapped_area = sum(v for k, v in before_area.items()
                    if k not in ['Comercial','Finanzas','Operaciones','Tecnología','Personas','Administración', np.nan, None])
log(f"  → {remapped_area} valores remapeados")
log("")

# ═══════════════════════════════════════════════════════════════════
# 3. CORREGIR SUELDO TOTAL INCONSISTENTE
# ═══════════════════════════════════════════════════════════════════
log("─── 3. Corregir Sueldo_Total_Reportado ───")

# 3a. Donde Sueldo_Base es NaN pero Sueldo_Total y Bono existen → recalcular Base
mask_base_null = df['Sueldo_Base'].isna() & df['Sueldo_Total_Reportado'].notna()
n_base_imputed = mask_base_null.sum()
df.loc[mask_base_null, 'Sueldo_Base'] = (
    df.loc[mask_base_null, 'Sueldo_Total_Reportado'] - df.loc[mask_base_null, 'Bono_Variable'].fillna(0)
)
log(f"  3a. Sueldo_Base imputado desde (Total - Bono): {n_base_imputed} registros")

# 3b. Recalcular Sueldo_Total = Sueldo_Base + Bono_Variable
df['Bono_Variable'] = df['Bono_Variable'].fillna(0)
df['Sueldo_Calc'] = df['Sueldo_Base'] + df['Bono_Variable']
diff = (df['Sueldo_Total_Reportado'] - df['Sueldo_Calc']).abs()
n_inconsistent = (diff > 1).sum()
df['Sueldo_Total_Reportado'] = df['Sueldo_Calc']
df.drop(columns=['Sueldo_Calc'], inplace=True)
log(f"  3b. Sueldo_Total recalculado (Base + Bono): {n_inconsistent} registros corregidos")
log("")

# ═══════════════════════════════════════════════════════════════════
# 4. RESOLVER ACTIVOS CON FECHA_SALIDA
# ═══════════════════════════════════════════════════════════════════
log("─── 4. Resolver Activos con Fecha_Salida ───")
mask_activo_salida = (df['Estado'] == 'Activo') & (df['Fecha_Salida'].notna())
n_activo_salida = mask_activo_salida.sum()

# Si tienen Motivo_Salida → probablemente están mal clasificados como Activos
mask_con_motivo = mask_activo_salida & df['Motivo_Salida'].notna()
n_reclasificado = mask_con_motivo.sum()
df.loc[mask_con_motivo, 'Estado'] = 'Desvinculado'
log(f"  4a. Activos con Motivo_Salida → reclasificados a Desvinculado: {n_reclasificado}")

# Si NO tienen Motivo_Salida → limpiar la Fecha_Salida (es ruido)
mask_sin_motivo = mask_activo_salida & df['Motivo_Salida'].isna()
# Actualizar máscara post-reclasificación
mask_sin_motivo = (df['Estado'] == 'Activo') & (df['Fecha_Salida'].notna()) & (df['Motivo_Salida'].isna())
n_fecha_limpia = mask_sin_motivo.sum()
df.loc[mask_sin_motivo, 'Fecha_Salida'] = pd.NaT
df.loc[mask_sin_motivo, 'Tipo_Rotacion'] = np.nan
log(f"  4b. Activos sin Motivo_Salida → Fecha_Salida limpiada: {n_fecha_limpia}")
log(f"  Total afectados: {n_activo_salida}")
log("")

# ═══════════════════════════════════════════════════════════════════
# 5. ELIMINAR RUTs DUPLICADOS  (conservar primera aparición)
# ═══════════════════════════════════════════════════════════════════
log("─── 5. Eliminar RUTs duplicados ───")
n_before = len(df)
n_rut_dup = df['RUT'].duplicated(keep='first').sum()
ruts_afectados = df.loc[df['RUT'].duplicated(keep=False), 'RUT'].nunique()
df = df.drop_duplicates(subset='RUT', keep='first').reset_index(drop=True)
n_after = len(df)
log(f"  RUTs duplicados encontrados: {ruts_afectados} RUTs con múltiples registros")
log(f"  Registros eliminados: {n_before - n_after}")
log(f"  Registros restantes: {n_after}")
log("")

# ═══════════════════════════════════════════════════════════════════
# 6. CORREGIR FECHAS INVERTIDAS  (Salida < Ingreso)
# ═══════════════════════════════════════════════════════════════════
log("─── 6. Corregir fechas invertidas ───")
mask_fechas_inv = df['Fecha_Salida'].notna() & (df['Fecha_Salida'] < df['Fecha_Ingreso'])
n_fechas_inv = mask_fechas_inv.sum()
# Swap: intercambiar las fechas
df.loc[mask_fechas_inv, ['Fecha_Ingreso', 'Fecha_Salida']] = (
    df.loc[mask_fechas_inv, ['Fecha_Salida', 'Fecha_Ingreso']].values
)
log(f"  Fechas intercambiadas (Ingreso ↔ Salida): {n_fechas_inv} registros")
log("")

# ═══════════════════════════════════════════════════════════════════
# 7. CONVERTIR REGISTROS USD → CLP
# ═══════════════════════════════════════════════════════════════════
log("─── 7. Convertir registros en USD a CLP ───")
mask_usd = df['Moneda'] == 'USD'
n_usd = mask_usd.sum()

# Revisar si los montos USD tienen magnitud similar a CLP (lo cual indicaría
# que ya están en CLP pero mal etiquetados)
usd_mean = df.loc[mask_usd, 'Sueldo_Base'].mean()
clp_mean = df.loc[df['Moneda'] == 'CLP', 'Sueldo_Base'].mean()
log(f"  Sueldo_Base promedio USD: {usd_mean:,.0f}")
log(f"  Sueldo_Base promedio CLP: {clp_mean:,.0f}")

if usd_mean > 100_000:
    # Los montos USD tienen magnitud de CLP → solo corregir la etiqueta
    log(f"  ⚠ Los montos en 'USD' tienen magnitud de CLP → se corrige solo la etiqueta Moneda")
    df.loc[mask_usd, 'Moneda'] = 'CLP'
    log(f"  → {n_usd} registros: Moneda 'USD' → 'CLP' (montos sin conversión)")
else:
    # Conversión real
    for col in ['Sueldo_Base', 'Bono_Variable', 'Sueldo_Total_Reportado']:
        df.loc[mask_usd, col] = df.loc[mask_usd, col] * TC_USD_CLP
    df.loc[mask_usd, 'Moneda'] = 'CLP'
    log(f"  → {n_usd} registros convertidos (x{TC_USD_CLP})")
log("")

# ═══════════════════════════════════════════════════════════════════
# 8. CORREGIR AUSENTISMO NEGATIVO
# ═══════════════════════════════════════════════════════════════════
log("─── 8. Corregir ausentismo negativo ───")
mask_neg_aus = df['Ausentismo_Dias'] < 0
n_neg_aus = mask_neg_aus.sum()
df.loc[mask_neg_aus, 'Ausentismo_Dias'] = df.loc[mask_neg_aus, 'Ausentismo_Dias'].abs()
log(f"  Ausentismo negativo → valor absoluto: {n_neg_aus} registros")
log("")

# ═══════════════════════════════════════════════════════════════════
# 9. IMPUTAR NULOS EN VARIABLES CLAVE
# ═══════════════════════════════════════════════════════════════════
log("─── 9. Imputar nulos en variables clave ───")

# 9a. Sueldo_Base: imputar con mediana del mismo Nivel + Area
n_null_sueldo = df['Sueldo_Base'].isna().sum()
if n_null_sueldo > 0:
    df['Sueldo_Base'] = df.groupby(['Nivel', 'Area'])['Sueldo_Base'].transform(
        lambda x: x.fillna(x.median())
    )
    # Si aún quedan NaN (combinación nivel-area sin datos), usar mediana del Nivel
    still_null = df['Sueldo_Base'].isna().sum()
    if still_null > 0:
        df['Sueldo_Base'] = df.groupby('Nivel')['Sueldo_Base'].transform(
            lambda x: x.fillna(x.median())
        )
    n_imputed_sueldo = n_null_sueldo - df['Sueldo_Base'].isna().sum()
    log(f"  9a. Sueldo_Base imputado (mediana Nivel+Área): {n_imputed_sueldo}")
    # Recalcular Sueldo_Total
    df['Sueldo_Total_Reportado'] = df['Sueldo_Base'] + df['Bono_Variable']
    log(f"      → Sueldo_Total recalculado post-imputación")

# 9b. Engagement: imputar con mediana del Área
n_null_eng = df['Engagement'].isna().sum()
df['Engagement'] = df.groupby('Area')['Engagement'].transform(
    lambda x: x.fillna(x.median())
)
n_imp_eng = n_null_eng - df['Engagement'].isna().sum()
log(f"  9b. Engagement imputado (mediana Área): {n_imp_eng}")

# 9c. Horas_Capacitacion: imputar con mediana del Nivel
n_null_hrs = df['Horas_Capacitacion'].isna().sum()
df['Horas_Capacitacion'] = df.groupby('Nivel')['Horas_Capacitacion'].transform(
    lambda x: x.fillna(x.median())
)
n_imp_hrs = n_null_hrs - df['Horas_Capacitacion'].isna().sum()
log(f"  9c. Horas_Capacitacion imputado (mediana Nivel): {n_imp_hrs}")

# 9d. Cursos_Tomados: imputar con mediana del Nivel
n_null_cursos = df['Cursos_Tomados'].isna().sum()
df['Cursos_Tomados'] = df.groupby('Nivel')['Cursos_Tomados'].transform(
    lambda x: x.fillna(x.median())
)
n_imp_cursos = n_null_cursos - df['Cursos_Tomados'].isna().sum()
log(f"  9d. Cursos_Tomados imputado (mediana Nivel): {n_imp_cursos}")

# 9e. Evaluacion_Desempeno: imputar con mediana del Nivel
n_null_eval = df['Evaluacion_Desempeno'].isna().sum()
df['Evaluacion_Desempeno'] = df.groupby('Nivel')['Evaluacion_Desempeno'].transform(
    lambda x: x.fillna(x.median())
)
n_imp_eval = n_null_eval - df['Evaluacion_Desempeno'].isna().sum()
log(f"  9e. Evaluacion_Desempeno imputado (mediana Nivel): {n_imp_eval}")

# 9f. Evaluacion_Anterior: imputar con mediana del Nivel (784 nulos — empleados nuevos)
n_null_eval_ant = df['Evaluacion_Anterior'].isna().sum()
df['Evaluacion_Anterior'] = df.groupby('Nivel')['Evaluacion_Anterior'].transform(
    lambda x: x.fillna(x.median())
)
n_imp_eval_ant = n_null_eval_ant - df['Evaluacion_Anterior'].isna().sum()
log(f"  9f. Evaluacion_Anterior imputado (mediana Nivel): {n_imp_eval_ant}")

# 9g. Sexo nulos: imputar desde Genero_Declarado si disponible
n_null_sexo = df['Sexo'].isna().sum()
genero_to_sexo = {'Masculino': 'M', 'Femenino': 'F', 'No binario': 'Otro', 'Otro': 'Otro'}
mask_sexo_null = df['Sexo'].isna() & df['Genero_Declarado'].notna()
df.loc[mask_sexo_null, 'Sexo'] = df.loc[mask_sexo_null, 'Genero_Declarado'].map(genero_to_sexo)
n_imp_sexo = n_null_sexo - df['Sexo'].isna().sum()
log(f"  9g. Sexo imputado desde Genero_Declarado: {n_imp_sexo}")

# 9h. Ausentismo_Dias nulos: imputar con mediana general
n_null_aus = df['Ausentismo_Dias'].isna().sum()
df['Ausentismo_Dias'] = df['Ausentismo_Dias'].fillna(df['Ausentismo_Dias'].median())
log(f"  9h. Ausentismo_Dias imputado (mediana global): {n_null_aus}")

# 9i. Fecha_Nacimiento nulos
n_null_fn = df['Fecha_Nacimiento'].isna().sum()
log(f"  9i. Fecha_Nacimiento nulos restantes (no imputables sin dato externo): {n_null_fn}")

log("")

# ═══════════════════════════════════════════════════════════════════
# 10. HOMOLOGAR ESCALA DE EVALUACIÓN
# ═══════════════════════════════════════════════════════════════════
log("─── 10. Homologar escala de evaluación ───")
log(f"  Eval. Desempeño rango actual: [{df['Evaluacion_Desempeno'].min():.1f}, {df['Evaluacion_Desempeno'].max():.1f}]")
log(f"  Eval. Anterior rango actual: [{df['Evaluacion_Anterior'].min():.1f}, {df['Evaluacion_Anterior'].max():.1f}]")

# Estandarizar Evaluacion_Desempeno al rango [1, 5] para que sea comparable con Anterior
# Mapeo lineal: 0→1, 6→5  → y = 1 + (x / 6) * 4
n_eval_0 = (df['Evaluacion_Desempeno'] == 0).sum()
n_eval_6 = (df['Evaluacion_Desempeno'] > 5).sum()
df['Evaluacion_Desempeno'] = 1 + (df['Evaluacion_Desempeno'] / 6) * 4
df['Evaluacion_Desempeno'] = df['Evaluacion_Desempeno'].round(2)
log(f"  Mapeo lineal aplicado: [0,6] → [1,5]")
log(f"  Nuevo rango: [{df['Evaluacion_Desempeno'].min():.2f}, {df['Evaluacion_Desempeno'].max():.2f}]")
log(f"  Registros en 0 originalmente: {n_eval_0}, en >5: {n_eval_6}")
log("")

# ═══════════════════════════════════════════════════════════════════
# EXTRA: Recalcular Edad consistente con Fecha_Nacimiento
# ═══════════════════════════════════════════════════════════════════
log("─── Extra. Recalcular Edad_Reportada ───")
ref_date = pd.Timestamp('2026-05-01')  # fecha de referencia
mask_fn_valid = df['Fecha_Nacimiento'].notna()
df.loc[mask_fn_valid, 'Edad_Reportada'] = (
    (ref_date - df.loc[mask_fn_valid, 'Fecha_Nacimiento']).dt.days / 365.25
).astype(int)
log(f"  Edad recalculada para {mask_fn_valid.sum()} registros (ref: {ref_date.date()})")
log("")

# ═══════════════════════════════════════════════════════════════════
# RESUMEN DE NULOS POST-LIMPIEZA
# ═══════════════════════════════════════════════════════════════════
log("─── Resumen de nulos post-limpieza ───")
nulos_post = df.isnull().sum()
nulos_post = nulos_post[nulos_post > 0].sort_values(ascending=False)
for col, n in nulos_post.items():
    log(f"  {col}: {n} ({n/len(df)*100:.1f}%)")
log("")

# ═══════════════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════════════
log(f"─── Guardando archivo limpio ───")
df.to_excel(OUTPUT_FILE, index=False, sheet_name='Datos_Clean')
log(f"  → {OUTPUT_FILE} ({len(df)} registros, {len(df.columns)} columnas)")

# Guardar log
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))
log(f"  → Log: {LOG_FILE}")
log("")
log(f"{'='*60}")
log(f"✅ DATA CLEANSING COMPLETADO")
log(f"{'='*60}")

#!/usr/bin/env python3
"""
genera_informe.py

Genera un Excel con estadísticas y gráficos de quizzes Moodle,
usando la vista vw_question_stats y vw_quiz_stats.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def main():
    # 1) Configuración de conexión
    load_dotenv()

    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

    conn_str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?collation=utf8mb4_general_ci"
    engine = create_engine(conn_str)

    # 2) Consulta SQL
    query = """
    SELECT
      qs.examen,
      qs.posicion as num,
      qs.texto_pregunta   AS pregunta,
      qs.veces_respondida as intentos,
      qs.aciertos_completos as aciertos,
      qs.penalizaciones   AS fallos,
      concat(ROUND(100.0 * qs.aciertos_completos / qs.veces_respondida, 2), '%') AS porcentaje_aciertos,
      concat(ROUND(100.0 * qs.penalizaciones   / qs.veces_respondida, 2), '%') AS porcentaje_fallos,
      qq.nota_media_global
    FROM vw_question_stats AS qs
    JOIN vw_quiz_stats    AS qq USING (examen)
    ORDER BY
      qs.examen,
      porcentaje_fallos DESC;"""

    # 3) Leer resultados
    df = pd.read_sql(query, engine)

    # 4) Crear columnas numéricas solo para cálculo (sin cambiar nombres originales)
    df['_porcentaje_fallos_num'] = df['porcentaje_fallos'].str.replace('%', '').astype(float)

    # 5) Generar resumen por examen
    summary = (
        df.groupby('examen')['_porcentaje_fallos_num']
          .mean()
          .reset_index()
          .rename(columns={'_porcentaje_fallos_num': 'porcentaje_fallos_promedio'})
    )

    # 6) Guardar Excel
    outdir = '/opt/bitnami/apache/htdocs/moodle/exports'
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, 'informe_quizzes.xlsx')

    with pd.ExcelWriter(outfile, engine='xlsxwriter') as writer:
        summary.to_excel(writer, sheet_name='Resumen por Examen', index=False)
        df.drop(columns=['_porcentaje_fallos_num']).to_excel(writer, sheet_name='Detalle por Pregunta', index=False)
        worksheet_resumen = writer.sheets['Resumen por Examen']
        worksheet_detalle = writer.sheets['Detalle por Pregunta']

        max_len = df['examen'].map(str).map(len).max()

        worksheet_detalle.set_column(0, 0, max_len + 2)
        worksheet_resumen.set_column(0, 0, max_len + 2)

        worksheet_detalle.autofilter(0, 0, df.shape[0], df.shape[1] -1)
        # 7) Insertar gráfico
        workbook = writer.book
        worksheet = writer.sheets['Resumen por Examen']
        chart = workbook.add_chart({'type': 'column'})

        max_row = len(summary) + 1
        chart.add_series({
            'name': '% Fallos promedio',
            'categories': ['Resumen por Examen', 1, 0, max_row, 0],
            'values':     ['Resumen por Examen', 1, 1, max_row, 1],
        })
        chart.set_title({'name': '% Fallos promedio por Examen'})
        chart.set_x_axis({'name': 'Examen'})
        chart.set_y_axis({'name': '% Fallos'})
        worksheet.insert_chart('D2', chart, {'x_scale': 2, 'y_scale': 2})

    print(f'Informe generado exitosamente en: {outfile}')

if __name__ == '__main__':
    main()


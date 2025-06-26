import os
import pandas as pd

def auto_adjust_column_width(writer, sheetname, df):
    worksheet = writer.sheets[sheetname]
    for i, col in enumerate(df.columns):
        max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, max_len)

def generate_report(df, outdir):
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, 'informe_quizzes.xlsx')
    
    # Crear resumen de fallos promedio por examen
    # Como df tiene porcentaje con '%', calculamos el promedio desde datos originales si hace falta
    # Pero aquí simplificamos usando un grupo
    df['fallos_porcentaje_num'] = df['porcentaje_fallos'].str.rstrip('%').astype(float)
    summary = df.groupby('examen')['fallos_porcentaje_num'].mean().reset_index()
    summary.rename(columns={'fallos_porcentaje_num': 'pct_fallos_promedio'}, inplace=True)
    
    with pd.ExcelWriter(outfile, engine='xlsxwriter') as writer:
        # Resumen
        summary.to_excel(writer, sheet_name='Resumen por Examen', index=False)
        auto_adjust_column_width(writer, 'Resumen por Examen', summary)
        
        # Detalle
        df.to_excel(writer, sheet_name='Detalle por Pregunta', index=False)
        worksheet = writer.sheets['Detalle por Pregunta']
        
        # Auto ajustar todas las columnas
        auto_adjust_column_width(writer, 'Detalle por Pregunta', df)
        
        # Añadir autofiltro a todas las columnas en detalle
        last_col = len(df.columns) - 1
        worksheet.autofilter(0, 0, len(df), last_col)
        
        # Gráfico en resumen
        workbook  = writer.book
        worksheet_summary = writer.sheets['Resumen por Examen']
        chart = workbook.add_chart({'type': 'column'})
        
        max_row = len(summary)
        chart.add_series({
            'name': '% Fallos promedio',
            'categories': ['Resumen por Examen', 1, 0, max_row, 0],
            'values':     ['Resumen por Examen', 1, 1, max_row, 1],
        })
        chart.set_title({'name': '% Fallos promedio por Examen'})
        chart.set_x_axis({'name': 'Examen'})
        chart.set_y_axis({'name': '% Fallos'})
        worksheet_summary.insert_chart('D2', chart, {'x_scale': 2, 'y_scale': 2})
    
    return outfile


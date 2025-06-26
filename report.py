import os
import pandas as pd

def auto_adjust_column_width(writer, sheetname, df):
    worksheet = writer.sheets[sheetname]
    first_col_width = max(
        df.iloc[:, 0].astype(str).map(len).max(),
        len(df.columns[0])
    )
    # Un poco de margen extra
    worksheet.set_column(0, 0, first_col_width + 2)

def generate_report(df, outdir):
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, 'informe_quizzes.xlsx')
    
    # Crear resumen de fallos promedio por examen
    # Como df tiene porcentaje con '%', calculamos el promedio desde datos originales si hace falta
    # Pero aquí simplificamos usando un grupo
    df['fallos_porcentaje_num'] = df['porcentaje_fallos'].astype(float)
    summary = df.groupby('examen')['fallos_porcentaje_num'].mean().reset_index()
    summary = (
    df.assign(
        pct_fallos=lambda d: d['porcentaje_fallos'].astype(float) / 100
    )
    .groupby('examen')['pct_fallos']
    .mean()
    .round(4)
    .reset_index()
    .rename(columns={'pct_fallos': 'fallos_promedio'})
    )
    
    with pd.ExcelWriter(outfile, engine='xlsxwriter') as writer:
        df.drop(columns=['fallos_porcentaje_num'], inplace=True)
        # Resumen
        summary.to_excel(writer, sheet_name='Resumen por Examen', index=False)
        worksheet_summary = writer.sheets['Resumen por Examen']
        auto_adjust_column_width(writer, 'Resumen por Examen', summary)
        
        # Detalle
        df.to_excel(writer, sheet_name='Detalle por Pregunta', index=False)
        worksheet = writer.sheets['Detalle por Pregunta']
        auto_adjust_column_width(writer, 'Detalle por Pregunta', df)
        
        # Añadir autofiltro a todas las columnas en detalle
        last_col = len(df.columns) - 1
        worksheet.autofilter(0, 0, len(df), last_col)
        # Gráfico en resumen
        workbook  = writer.book

        percent_fmt = workbook.add_format({'num_format': '0.00%'})
        worksheet.set_column('G:H', None, percent_fmt)
        worksheet_summary.set_column('B:B', None, percent_fmt)
        
        chart = workbook.add_chart({'type': 'column'}) 

        chart.add_series({
            'name': '% Fallos promedio',
            'categories': ['Resumen por Examen', 1, 0, len(summary), 0],
            'values':     ['Resumen por Examen', 1, 1, len(summary), 1],
        })
        chart.set_title({'name': '% Fallos promedio por Examen'})
        chart.set_x_axis({'name': 'Examen'})
        chart.set_y_axis({'name': '% Fallos'})
        worksheet_summary.insert_chart('D2', chart, {'x_scale': 2, 'y_scale': 2})
    
    return outfile


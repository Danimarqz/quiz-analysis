import pandas as pd
from sqlalchemy import create_engine
from config import get_db_config

def get_data():
    cfg = get_db_config()
    conn_str = f"mysql+mysqlconnector://{cfg['DB_USER']}:{cfg['DB_PASS']}@{cfg['DB_HOST']}/{cfg['DB_NAME']}?collation=utf8mb4_general_ci"
    engine = create_engine(conn_str)
    
    query = """
    SELECT
      qs.examen,
      qs.posicion as num,
      qs.texto_pregunta   AS pregunta,
      qs.veces_respondida  as intentos,
      qs.aciertos_completos as aciertos,
      qs.penalizaciones   AS fallos,
      concat(ROUND(100.0 * qs.aciertos_completos / qs.veces_respondida, 2), '%') AS porcentaje_aciertos,
      concat(ROUND(100.0 * qs.penalizaciones   / qs.veces_respondida, 2), '%') AS porcentaje_fallos,
      qq.nota_media_global
    FROM vw_question_stats AS qs
    JOIN vw_quiz_stats    AS qq USING (examen)
    ORDER BY
      qs.examen,
      porcentaje_fallos DESC;
    """
    
    df = pd.read_sql(query, engine)
    return df


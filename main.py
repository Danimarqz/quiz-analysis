from db import get_data
from report import generate_report
from config import get_db_config

def main():
    cfg = get_db_config()
    df = get_data()
    outfile = generate_report(df, cfg['EXPORT_DIR'])
    print(f'Informe generado exitosamente en: {outfile}')

if __name__ == '__main__':
    main()


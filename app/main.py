import logging
#from app.scraper_sin_ai import scrape_yogonet 
from app.scraper import scrape_yogonet
from processor import process
from bq_loader import upload_to_bigquery
from utils.ai_helper import predict_element_type 
import os

# Leer variables de entorno
PROYECTO = os.getenv("GCP_PROJECT_ID", "").strip()
DATASET = os.getenv("BIGQUERY_DATASET", "").strip()
TABLA = os.getenv("BIGQUERY_TABLE", "").strip()

def main():
    # Elimina cualquier handler de logging existente para evitar duplicados
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configura el logging para mostrar mensajes con formato y nivel INFO
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Iniciando Main")
    try:
        logging.info("Iniciando scraping de Yogonet con AI...")
        raw_data = scrape_yogonet()
        logging.info(f"Scraping finalizado. Se obtuvieron {len(raw_data)} registros.")
        
        logging.info("Procesando datos...")
        df = process(raw_data)
        print(df)

        if df.empty:
            logging.warning("El DataFrame está vacío, no se cargará nada a BigQuery.")
            return

        logging.info(f"DataFrame listo con {len(df)} filas. Iniciando carga a BigQuery...")
        upload_to_bigquery(df, PROYECTO, DATASET, TABLA)
        logging.info("Carga a BigQuery finalizada exitosamente.")

    except Exception as e:
        logging.error(f"Ocurrió un error en el flujo principal: {e}", exc_info=True)

if __name__ == "__main__":
    main()
import logging
import json
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError


def convertir_listas_a_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte columnas que contienen listas en representaciones JSON string.
    """
    try:
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
        return df
    except Exception as e:
        logging.exception(f"Error al convertir listas a strings: {e}")
        raise


def upload_to_bigquery(df: pd.DataFrame, proyecto: str, dataset: str, tabla: str) -> None:
    """
    Sube un DataFrame a una tabla de BigQuery, sobrescribiendo los datos existentes.

    Args:
        df (pd.DataFrame): DataFrame a subir.
        proyecto (str): ID del proyecto de GCP.
        dataset (str): Nombre del dataset en BigQuery.
        tabla (str): Nombre de la tabla en BigQuery.
    """
    if df.empty:
        logging.warning("El DataFrame está vacío. No se subirá nada a BigQuery.")
        return

    try:
        client = bigquery.Client(project=proyecto)
        tabla_id = f"{proyecto}.{dataset}.{tabla}"

        df = convertir_listas_a_strings(df)

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        load_job = client.load_table_from_dataframe(df, tabla_id, job_config=job_config)
        load_job.result()

        logging.info(f"Carga a BigQuery completada correctamente: {tabla_id}")

    except GoogleCloudError as gce:
        logging.error(f"Error de BigQuery: {gce.message}", exc_info=True)
        raise
    except Exception as e:
        logging.exception(f"Error inesperado durante la carga a BigQuery: {e}")
        raise
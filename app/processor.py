import pandas as pd
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

def process(data):
    """
    Convierte la lista de diccionarios en DataFrame y calcula columnas adicionales.
    Maneja errores de forma robusta y registra advertencias si la data es inválida.
    """
    try:
        if not data:
            logging.warning("No se recibió data para procesar.")
            return pd.DataFrame()  # DataFrame vacio

        df = pd.DataFrame(data)

        # Validar que la columna 'title' exista y tenga al menos un valor no nulo
        if "title" not in df.columns or df["title"].isnull().all():
            logging.warning("No hay títulos válidos para procesar.")
            return df

        # Calcular columnas adicionales
        df['UpdateDate'] = pd.Timestamp.now(tz=ZoneInfo("America/Argentina/Buenos_Aires")) 
        logging.info(f"Fecha de actualización: {df['UpdateDate'].iloc[0]}")
        
        df["title_word_count"] = df["title"].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
        df["title_char_count"] = df["title"].apply(lambda x: len(x) if isinstance(x, str) else 0)
        df["capitalized_words"] = df["title"].apply(
            lambda x: [word for word in x.split() if word and word[0].isupper()] if isinstance(x, str) else []
        )

        return df

    except Exception as e:
        logging.exception(f"Error al procesar los datos: {e}")
        return pd.DataFrame()  # Retornar un DataFrame vacio para evitar que el flujo se rompa
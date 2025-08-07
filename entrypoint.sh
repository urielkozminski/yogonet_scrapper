#!/bin/bash

# Carga variables de entorno
export $(cat .env | xargs)

# Ejecuta el scraper
python app/main.py
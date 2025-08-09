#!/bin/bash

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta el script para poblar la base de datos
python3 run.py

# Ejecuta el servidor FastAPI con Uvicorn
uvicorn main:app --reload
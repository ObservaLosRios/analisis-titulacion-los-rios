#!/bin/bash

# Script de demostración del ETL Pipeline
# Ejecuta diferentes modos del pipeline para demostrar funcionalidades

echo "🚀 Demostrando ETL Pipeline - Análisis de Titulación Los Ríos"
echo "============================================================"

# Activar entorno virtual
source .venv/bin/activate

echo ""
echo "1️⃣  Generando resumen regional..."
python main.py --regional-summary --verbose

echo ""
echo "2️⃣  Ejecutando solo extracción..."
python main.py --extract-only

echo ""
echo "3️⃣  Ejecutando validación de calidad..."
python main.py --validate-only --verbose

echo ""
echo "4️⃣  Ejecutando pipeline completo..."
python main.py --output "demo_output.csv" --quality-threshold 60

echo ""
echo "✅ Demostración completada!"
echo ""
echo "📁 Archivos generados:"
ls -la data/clean/

echo ""
echo "📊 Contenido del archivo demo:"
head -15 data/clean/demo_output.csv



# ETL para Análisis de Titulación - Región de Los Ríos

Pipeline ETL para analizar datos de titulación universitaria en la Región de Los Ríos, Chile, basado en el informe SIES 2024. El proyecto está diseñado para ser mantenible, extensible y robusto, siguiendo buenas prácticas de arquitectura y desarrollo.

**Autor:** [Bruno San Martín](https://www.linkedin.com/in/brunosanmartin/)  
**Fuente de datos:** [Mi Futuro - Ministerio de Educación de Chile](https://www.mifuturo.cl/)



## Descripción
Pipeline modular para extracción, transformación, validación y carga de datos de titulación. Permite filtrar, limpiar y analizar datos regionales, con reportes de calidad y monitoreo de métricas clave.


## Arquitectura

- Modularidad: Separación clara entre extracción, transformación, validación y carga.
- Principios de diseño: Cada componente tiene una responsabilidad única y puede ser extendido fácilmente.
- Manejo de errores: Excepciones específicas y logging estructurado.
- Tests: Cobertura de componentes críticos y mocking de dependencias.


## Estructura del Proyecto

```text
analisis-titulacion-los-rios/
├── README.md
├── TECHNICAL_DOCS.md
├── pyproject.toml
├── requirements.txt
├── main.py
├── demo.sh
├── Informe_Titulacion_2024_SIES-pdf.pdf
├── data/
│   ├── clean/
│   │   └── titulacion_los_rios_clean_1753653642.csv
│   ├── processed/
│   │   ├── carreras_summary_20250727_1829.csv
│   │   ├── instituciones_summary_20250727_1829.csv
│   │   ├── niveles_summary_20250727_1829.csv
│   │   └── temporal_summary_20250727_1829.csv
│   └── raw/
│       └── Informe_Titulacion_2024_SIES_.xlsx
├── docs/
│   └── index.html
├── logs/
│   ├── etl_errors_20250727.log
│   └── etl_pipeline_20250727.log
├── notebooks/
│   ├── analisis_los_rios.ipynb
│   ├── Analisis_titulacion_los_rios.ipynb
│   └── dashboard_economist_style.ipynb
├── src/
│   ├── etl_pipeline.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   ├── interfaces.py
│   │   ├── models.py
│   │   ├── extractors/
│   │   │   ├── __init__.py
│   │   │   └── excel_extractor.py
│   │   ├── loaders/
│   │   │   ├── __init__.py
│   │   │   └── csv_loader.py
│   │   ├── transformers/
│   │   │   ├── __init__.py
│   │   │   ├── data_cleaner.py
│   │   │   └── regional_filter.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   └── validators/
│   │       ├── __init__.py
│   │       └── data_quality_validator.py
└── tests/
    ├── conftest.py
    ├── test_extractors.py
    └── test_transformers.py
```


## Instalación


### Prerrequisitos
- Python 3.8 o superior
- pip


### Pasos
1. Clona el repositorio:
  ```bash
  git clone https://github.com/ObservaLosRios/analisis-titulacion-los-rios.git
  cd analisis-titulacion-los-rios
  ```
2. Crea un entorno virtual:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # Linux/Mac
  # .venv\Scripts\activate  # Windows
  ```
3. Instala dependencias:
  ```bash
  pip install -r requirements.txt
  ```
4. Configura variables de entorno (opcional):
  ```bash
  cp .env.example .env  # Si existe
  # Edita .env según tus necesidades
  ```


## Uso


### Pipeline completo
Ejecuta el proceso ETL:
```bash
python main.py
```

### Opciones avanzadas
- Solo extracción:
  ```bash
  python main.py --extract-only
  ```
- Solo validación:
  ```bash
  python main.py --validate-only --verbose
  ```
- Resumen regional:
  ```bash
  python main.py --regional-summary
  ```
- Parámetros personalizados:
  ```bash
  python main.py --output mi_archivo.csv --quality-threshold 85
  ```

### Script de demostración
```bash
./demo.sh
```


## Características principales


### Componentes ETL


#### Extractores
- Extracción desde archivos Excel (.xlsx, .xls)
- Validación de fuente y manejo de errores


#### Transformadores
- Limpieza y normalización de datos (columnas, texto, valores faltantes, outliers, duplicados)
- Filtrado específico para Los Ríos y reporte regional


#### Validadores
- Validación de estructura, tipos y reglas de negocio
- Reportes de calidad y score (0-100%)


#### Cargadores
- Exportación a CSV con metadatos y validación


### Validación de calidad de datos


#### Métricas
- Score de calidad: % de registros válidos
- Análisis de valores faltantes por columna
- Validación de tipos y reglas de negocio
- Detección de duplicados


#### Reglas de validación
```python
# Ejemplo:
year_range: (1990, 2030)
quantity_range: (0, 10000)
required_columns: ['region', 'ano_titulacion']
```


### Logging estructurado


#### Niveles
- INFO: Operaciones normales
- WARNING: Atención requerida
- ERROR: Errores
- DEBUG: Detalles para depuración


#### Archivos
- `etl_pipeline_YYYYMMDD.log`: Log general diario
- `etl_errors_YYYYMMDD.log`: Solo errores
- Consola con colores


### Configuración


#### Variables de entorno (.env)
```bash
DATA_RAW_PATH=data/raw
DATA_PROCESSED_PATH=data/processed  
DATA_CLEAN_PATH=data/clean
LOG_PATH=logs
LOG_LEVEL=INFO
TARGET_REGION=Los Ríos
EXCEL_FILE_NAME=Informe_Titulacion_2024_SIES_.xlsx
```


## Testing


### Ejecutar tests
```bash
# Todos los tests
pytest
# Test específico
pytest tests/test_extractors.py -v
# Con cobertura
pytest --cov=src tests/
```


### Estructura
- `tests/conftest.py`: Fixtures y configuración común
- `tests/test_extractors.py`: Extractores
- `tests/test_transformers.py`: Transformadores


## Monitoreo y métricas


### Métricas
- Tiempo de ejecución por operación y total
- Registros procesados antes y después de cada paso
- Tasa de calidad
- Uso de recursos


### Reportes de calidad
```
=== DATA QUALITY REPORT ===
Total Records: 1,000
Valid Records: 850
Invalid Records: 150
Quality Score: 85.0%
Missing Values by Column:
  - telefono: 45 (4.5%)
  - email: 23 (2.3%)
Validation Errors:
  - 12 registros con años de titulación inválidos
  - 8 registros con cantidades inválidas
```




## Manejo de errores


### Excepciones
- ExtractionError: Extracción
- TransformationError: Transformación
- ValidationError: Validación
- LoadingError: Carga
- ConfigurationError: Configuración
- DataQualityError: Calidad insuficiente


### Ejemplo
```python
try:
  result = pipeline.run_full_pipeline()
except DataQualityError as e:
  logger.error(f"Data quality below threshold: {e.quality_score}%")
except ExtractionError as e:
  logger.error(f"Failed to extract from {e.source_path}: {e.message}")
```

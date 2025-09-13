"""Test configuration and fixtures."""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add src to path for testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_data():
    """Create sample graduation data for testing."""
    data = {
        'codigo_institucion': ['001', '002', '003', '004', '005'],
        'nombre_institucion': ['Universidad A', 'Universidad B', 'Instituto C', 'Universidad D', 'Instituto E'],
        'region': ['Los Ríos', 'Los Ríos', 'Metropolitana', 'Los Ríos', 'Valparaíso'],
        'provincia': ['Valdivia', 'Ranco', 'Santiago', 'Valdivia', 'Valparaíso'],
        'carrera': ['Ingeniería', 'Medicina', 'Derecho', 'Pedagogía', 'Arquitectura'],
        'ano_titulacion': [2023, 2023, 2022, 2023, 2022],
        'mes_titulacion': [12, 6, 3, 9, 11],
        'cantidad_titulados': [45, 32, 67, 28, 51],
        'genero': ['Mixto', 'Mixto', 'Mixto', 'Mixto', 'Mixto']
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_excel_file(sample_data):
    """Create temporary Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        sample_data.to_excel(tmp.name, index=False, engine='openpyxl')
        yield tmp.name
    os.unlink(tmp.name)


@pytest.fixture
def temp_csv_file():
    """Create temporary CSV file path for testing."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        yield tmp.name
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)


@pytest.fixture
def mock_logger():
    """Create mock logger for testing."""
    return MagicMock()


@pytest.fixture
def los_rios_data():
    """Create sample data specific to Los Ríos region."""
    data = {
        'codigo_institucion': ['001', '002', '003'],
        'nombre_institucion': ['Universidad Austral', 'Instituto Los Ríos', 'Universidad Santo Tomás'],
        'region': ['Los Ríos', 'Los Ríos', 'Los Ríos'],
        'provincia': ['Valdivia', 'Ranco', 'Valdivia'],
        'carrera': ['Ingeniería Forestal', 'Técnico Agrícola', 'Derecho'],
        'ano_titulacion': [2023, 2023, 2023],
        'cantidad_titulados': [25, 18, 42]
    }
    return pd.DataFrame(data)

import pytest
from src.data_loader import DataLoader
import pandas as pd
import os

def test_load_csv_success():
    loader = DataLoader(os.path.join('data', 'raw', 'dirty_cafe_sales.csv'))
    df = loader.load_csv()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_csv_file_not_found():
    loader = DataLoader('data/raw/non_existent.csv')
    with pytest.raises(Exception) as excinfo:
        loader.load_csv()
    assert 'Fichier non trouvé' in str(excinfo.value)

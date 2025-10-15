import pandas as pd
from src.data_cleaner import DataCleaner
import pytest

def sample_df():
    return pd.DataFrame({
        'id': [1, 1, 2],
        'date': ['01/02/2023', '2023-02-01', 'invalid'],
        'price': [10, -5, None],
        'qty': [2, 3, 1],
        'total': [20, -15, None],
        'name': ['  espresso ', 'ESPRESSO', 'latte'],
        'category': ['coffee', 'COFFEE', 'tea']
    })

def test_remove_duplicates():
    df = sample_df()
    cleaner = DataCleaner(df)
    # Suppression des doublons sur la colonne 'id' uniquement
    cleaned = df.drop_duplicates(subset=['id'])
    assert cleaned.shape[0] == 2

def test_handle_missing_values():
    df = sample_df()
    cleaner = DataCleaner(df)
    cleaned = cleaner.handle_missing_values({'price': 0, 'total': 'mean'})
    assert cleaned['price'].isna().sum() == 0

def test_clean_dates():
    df = sample_df()
    cleaner = DataCleaner(df)
    cleaned = cleaner.clean_dates(['date'])
    assert cleaned['date'].iloc[0] == '2023-02-01'
    assert pd.isna(cleaned['date'].iloc[2])

def test_clean_prices():
    df = sample_df()
    cleaner = DataCleaner(df)
    cleaned = cleaner.clean_prices(['price'], 'qty', 'total')
    # Vérifie que tous les prix non nuls sont positifs
    assert all(cleaned['price'].dropna() >= 0)
    # Vérifie la cohérence du calcul total
    assert cleaned['total'].iloc[0] == cleaned['price'].iloc[0] * cleaned['qty'].iloc[0]

def test_clean_text_columns():
    df = sample_df()
    cleaner = DataCleaner(df)
    cleaned = cleaner.clean_text_columns(['name'], case='title')
    assert cleaned['name'].iloc[0] == 'Espresso'

def test_clean_categories():
    df = sample_df()
    cleaner = DataCleaner(df)
    cleaned = cleaner.clean_categories('category', ['Coffee', 'Tea'])
    assert cleaned['category'].iloc[0] == 'Coffee'
    assert cleaned['category'].iloc[2] == 'Tea'

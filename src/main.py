import os
import pandas as pd
from data_loader import DataLoader
from data_cleaner import DataCleaner

RAW_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'dirty_cafe_sales.csv')
CLEAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'cafe_sales_clean.csv')

# Colonnes du CSV
DATE_COL = 'Transaction Date'
PRICE_COL = 'Price Per Unit'
QTY_COL = 'Quantity'
TOTAL_COL = 'Total Spent'
ITEM_COL = 'Item'
CAT_COL = 'Item' 
PAYMENT_COL = 'Payment Method'
LOCATION_COL = 'Location'

# Catégories valides
VALID_ITEMS = ['Coffee', 'Cake', 'Cookie', 'Salad', 'Smoothie', 'Sandwich', 'Juice', 'Tea']
VALID_PAYMENTS = ['Credit Card', 'Cash', 'Digital Wallet']
VALID_LOCATIONS = ['Takeaway', 'In-Store']

if __name__ == "__main__":
    # Chargement
    loader = DataLoader(RAW_PATH)
    df = loader.load_csv()

    # Conversion en numérique pour Price Per Unit, Quantity et Total Spent avant calcul de la moyenne/mode
    df[PRICE_COL] = pd.to_numeric(df[PRICE_COL], errors='coerce')
    df[QTY_COL] = pd.to_numeric(df[QTY_COL], errors='coerce')
    df[TOTAL_COL] = pd.to_numeric(df[TOTAL_COL], errors='coerce')

    # Nettoyage dupliats
    cleaner = DataCleaner(df)
    df = cleaner.remove_duplicates()
    # Valeurs manquantes
    missing_strategies = {
        ITEM_COL: 'Unknown',
        QTY_COL: df[QTY_COL].mode()[0] if df[QTY_COL].notna().any() else 1,
        PRICE_COL: df[PRICE_COL].mean() if df[PRICE_COL].notna().any() else 1.0,
        TOTAL_COL: 'mean',
        PAYMENT_COL: 'Unknown',
        LOCATION_COL: 'Unknown',
        DATE_COL: 'Unknown'
    }
    df = cleaner.handle_missing_values(missing_strategies)
    # Dates
    df = cleaner.clean_dates([DATE_COL])
    # Prix et montants
    df = cleaner.clean_prices([PRICE_COL], QTY_COL, TOTAL_COL)
    # Textes
    df = cleaner.clean_text_columns([ITEM_COL, PAYMENT_COL, LOCATION_COL], case='title')
    # Catégories
    df = cleaner.clean_categories(ITEM_COL, VALID_ITEMS)
    df = cleaner.clean_categories(PAYMENT_COL, VALID_PAYMENTS)
    df = cleaner.clean_categories(LOCATION_COL, VALID_LOCATIONS)
    # Correction des erreurs dans Total Spent (ex: "ERROR")
    df[TOTAL_COL] = pd.to_numeric(df[TOTAL_COL], errors='coerce')
    df[TOTAL_COL] = (df[PRICE_COL] * df[QTY_COL]).round(2)

    # Nettoyage final : suppression des lignes critiques et imputation des non-critiques
    df = cleaner.handle_unknowns(
        critical_cols=[ITEM_COL, TOTAL_COL, DATE_COL],
        non_critical_impute={LOCATION_COL: 'Non renseigné', PAYMENT_COL: 'mode'}
    )

    # Sauvegarde
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Données nettoyées sauvegardées dans {CLEAN_PATH}")


import pandas as pd
import numpy as np
import re
from dateutil import parser

class DataCleaner:
    def handle_unknowns(self, critical_cols=None, non_critical_impute=None):
        """
        Supprime les lignes où les colonnes critiques sont 'Unknown' ou vides.
        Impute les colonnes non critiques avec une valeur par défaut ou le mode.
        critical_cols: liste de colonnes à considérer comme critiques (ex: ['Item', 'Total Spent'])
        non_critical_impute: dict {col: valeur ou 'mode'} pour imputation
        """
        if critical_cols:
            for col in critical_cols:
                self.df = self.df[(self.df[col].notna()) & (self.df[col] != 'Unknown') & (self.df[col] != '')]
        if non_critical_impute:
            for col, val in non_critical_impute.items():
                if val == 'mode':
                    mode_val = self.df[col][self.df[col] != 'Unknown'].mode()
                    if not mode_val.empty:
                        self.df[col] = self.df[col].replace('Unknown', mode_val[0])
                else:
                    self.df[col] = self.df[col].replace('Unknown', val)
        return self.df
    def __init__(self, df):
        self.df = df.copy()

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self.df

    def handle_missing_values(self, strategies):
        for col, strat in strategies.items():
            if strat == 'drop':
                self.df = self.df[self.df[col].notna()]
            elif strat == 'mean':
                self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif strat == 'median':
                self.df[col] = self.df[col].fillna(self.df[col].median())
            elif strat == 'mode':
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
            else:
                self.df[col] = self.df[col].fillna(strat)
        return self.df

    def clean_dates(self, date_columns):
        for col in date_columns:
            self.df[col] = self.df[col].apply(self._parse_date)
        return self.df

    def _parse_date(self, value):
        if pd.isna(value):
            return np.nan
        try:
            dt = parser.parse(str(value), dayfirst=True, yearfirst=False)
            return dt.strftime('%Y-%m-%d')
        except Exception:
            return np.nan

    def clean_prices(self, price_columns, qty_column=None, total_column=None):
        for col in price_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            self.df[col] = self.df[col].apply(lambda x: max(x, 0) if pd.notna(x) else x)
            self.df[col] = self.df[col].round(2)
        if qty_column and total_column:
            self.df[total_column] = self.df[price_columns[0]] * self.df[qty_column]
        return self.df

    def clean_text_columns(self, text_columns, case='title'):
        for col in text_columns:
            self.df[col] = self.df[col].astype(str)
            self.df[col] = self.df[col].apply(lambda x: re.sub(r'\s+', ' ', x.strip()))
            if case == 'title':
                self.df[col] = self.df[col].str.title()
            elif case == 'lower':
                self.df[col] = self.df[col].str.lower()
        return self.df

    def clean_categories(self, category_column, valid_categories):
        self.df[category_column] = self.df[category_column].astype(str).str.title().str.strip()
        self.df[category_column] = self.df[category_column].apply(lambda x: x if x in valid_categories else 'Unknown')
        return self.df

import pandas as pd

class DataAnalyzer:
    """
    Module d'analyse des données nettoyées du pipeline café.
    Réalise les statistiques et analyses demandées dans le sujet.
    """
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        if 'Transaction Date' in self.df.columns:
            self.df['Transaction Date'] = pd.to_datetime(self.df['Transaction Date'], errors='coerce')

    def total_revenue(self):
        """Chiffre d'affaires total"""
        return self.df['Total Spent'].sum()

    def sales_by_category(self):
        """Ventes par catégorie de produit"""
        return self.df.groupby('Item')['Total Spent'].sum()

    def sales_by_period(self, freq='M'):
        """Ventes par période (jour='D', semaine='W', mois='M')"""
        if 'Transaction Date' not in self.df.columns:
            raise ValueError("Colonne 'Transaction Date' manquante")
        return self.df.set_index('Transaction Date').resample(freq)['Total Spent'].sum()

    def top_products(self, n=10):
        """Top n des produits les plus vendus (par quantité)"""
        return self.df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(n)

    def average_ticket(self):
        """Ticket moyen"""
        return self.df['Total Spent'].mean()

    def sales_evolution(self):
        """Évolution des ventes dans le temps (par jour)"""
        if 'Transaction Date' not in self.df.columns:
            raise ValueError("Colonne 'Transaction Date' manquante")
        return self.df.groupby('Transaction Date')['Total Spent'].sum()

    def descriptive_stats(self):
        """Statistiques descriptives sur les montants"""
        return self.df['Total Spent'].describe()

    def sales_by_category_period(self, freq='M'):
        """Ventes par catégorie et par période (optionnel)"""
        if 'Transaction Date' not in self.df.columns:
            raise ValueError("Colonne 'Transaction Date' manquante")
        return self.df.set_index('Transaction Date').groupby('Item').resample(freq)['Total Spent'].sum()

if __name__ == "__main__":
    analyzer = DataAnalyzer("data/processed/cafe_sales_clean.csv")
    print("Chiffre d'affaires total:", analyzer.total_revenue())
    print("Ventes par catégorie:\n", analyzer.sales_by_category())
    print("Ventes par mois:\n", analyzer.sales_by_period('M'))
    print("Top 10 produits:\n", analyzer.top_products())
    print("Ticket moyen:", analyzer.average_ticket())
    print("Évolution des ventes:\n", analyzer.sales_evolution())
    print("Stats descriptives:\n", analyzer.descriptive_stats())

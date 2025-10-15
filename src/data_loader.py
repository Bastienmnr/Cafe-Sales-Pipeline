import pandas as pd

class DataLoader:
    def __init__(self, filepath, encoding='utf-8'):
        self.filepath = filepath
        self.encoding = encoding

    def load_csv(self):
        try:
            df = pd.read_csv(self.filepath, encoding=self.encoding)
            return df
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(self.filepath, encoding='latin1')
                return df
            except Exception as e:
                raise Exception(f"Erreur d'encodage lors de la lecture du fichier : {e}")
        except FileNotFoundError:
            raise Exception(f"Fichier non trouvé : {self.filepath}")
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier : {e}")

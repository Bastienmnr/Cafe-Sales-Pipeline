# Pipeline de Nettoyage de Données

## Contexte

Vous êtes Data Engineer dans une chaîne de cafés. Le système de caisse a généré un fichier CSV contenant les ventes, mais les données sont de mauvaise qualité. Votre mission est de créer un pipeline de nettoyage robuste et testé.

**Dataset** : Cafe Sales - Dirty Data for Cleaning Training  
**Source** : [Kaggle - Cafe Sales Dataset](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training)

---

## Structure du projet attendue

```
cafe-sales-pipeline/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── data_analyzer.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
├── data/
│   ├── raw/
│   │   └── cafe_sales_dirty.csv
│   └── processed/
│       └── cafe_sales_clean.csv
├── Dockerfile
├── docker-compose.yml
├── .gitlab-ci.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements.txt

```
pandas==2.1.0
numpy==1.24.3
pytest==7.4.0
pytest-cov==4.1.0
flake8==6.0.0
python-dotenv==1.0.0
python-dateutil==2.8.2
```

---

## Partie 1 : Analyse exploratoire

## Avant de commencer le développement, téléchargez le dataset et analysez-le pour identifier les problèmes de qualité.

---

## Partie 2 : Développement TDD

### Module : DataLoader

Charger le fichier CSV et valider sa structure de base.

**Fonctionnalités à implémenter** :

- Lecture du CSV avec gestion d'encodage
- Gestion des exceptions avec messages clairs

---

### Module : DataCleaner

**Fonctionnalités de nettoyage à implémenter** :

#### 2.1 Doublons

- Identifier et supprimer les doublons exacts

#### 2.2 Valeurs manquantes

- Identifier les colonnes avec valeurs manquantes
- Définir une stratégie par colonne :
  - Suppression des lignes si données critiques manquantes
  - Imputation avec valeur par défaut si approprié
  - Imputation par moyenne/médiane/mode selon le contexte

#### 2.3 Dates

- Identifier tous les formats de dates présents
- Convertir vers un format unique (ISO 8601 : YYYY-MM-DD)
- Gérer les dates invalides ou aberrantes

** Aide pour les dates** :

```python
# Formats courants à gérer :
# - DD/MM/YYYY
# - MM-DD-YYYY
# - YYYY-MM-DD
# - DD.MM.YYYY
# - Timestamps

# Outils recommandés :
# - pd.to_datetime() avec format='mixed' ou infer_datetime_format=True
# - dateutil.parser pour parsing flexible
# - Validation avec try/except pour détecter les dates invalides
```

#### 2.4 Prix et montants

- Vérifier qu'aucun prix n'est négatif
- Uniformiser les formats (nombre de décimales, séparateur)
- Identifier les valeurs abérantes
- S'assurer de la cohérence : prix_total = prix_unitaire × quantité

#### 2.5 Noms et textes

- Supprimer les espaces multiples et en début/fin
- Normaliser la casse (Title Case ou lowercase selon le contexte)
- Remplacer les caractères spéciaux problématiques

#### 2.6 Catégories

- Standardiser les noms de catégories
- Regrouper les variantes (ex: "Coffee" / "coffee" / "COFFEE" => "Coffee")
- Créer une liste de catégories valides
- Marquer ou corriger les catégories non reconnues

---

### Module : DataAnalyzer

Produire des analyses et statistiques sur les données nettoyées.

**Analyses à implémenter** :

- Chiffre d'affaires total
- Ventes par catégorie de produit
- Ventes par période (jour, semaine, mois)
- Top 10 des produits les plus vendus
- Ticket moyen
- Évolution des ventes dans le temps
- Statistiques descriptives (moyenne, médiane, écart-type)

---

## Partie 3 : Conteneurisation

### Dockerfile

**Exigences** :

- Utiliser une image Python officielle
- Installer toutes les dépendances du requirements.txt
- Copier le code source dans le container
- Définir le WORKDIR approprié
- Configurer le volume pour data/
- Définir une commande par défaut qui lance le pipeline

### docker-compose.yml

**Services à créer** :

1. **pipeline-runner** : Exécute le pipeline de nettoyage
2. **test-runner** : Exécute les tests avec coverage

---

## Partie 4 : CI/CD GitLab

### Pipeline GitLab CI

**Stages à implémenter** :

1. **test** : Linting + Tests unitaires + Coverage
2. **build** : Construction de l'image Docker
3. **deploy** : Déploiement (dockerhub)

**Variables GitLab à configurer** :

- Variables de registry
- Variables de déploiement
- Secrets

## Ressources utiles :

- **Pandas** : https://pandas.pydata.org/docs/
- **Pytest** : https://docs.pytest.org/
- **Docker** : https://docs.docker.com/
- **GitLab CI** : https://docs.gitlab.com/ee/ci/

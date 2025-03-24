# Qualité du Code

## Standards de Qualité

SolarCalculet maintient des standards de qualité élevés grâce à plusieurs outils et métriques :

### Score Pylint : 9.43/10

Le projet utilise [pylint](https://pylint.org/) pour l'analyse statique du code. Notre score actuel de 9.43/10 reflète notre engagement envers un code propre et maintenable.

#### Détails des Métriques

- **Formatage du Code** : Tout le code est formaté avec [black](https://black.readthedocs.io/)
- **Ordre des Imports** : Respect de la convention (imports standards avant les imports tiers)
- **Documentation** : Docstrings pour toutes les classes et fonctions
- **Nommage** : Conventions PEP8 pour les noms de variables et fonctions

### Tests et Couverture

- **Coverage** : 100% de couverture de tests
- **Approche** : Test-Driven Development (TDD)
- **Types de Tests** :
  - Tests Unitaires
  - Tests d'Intégration
  - Tests de Configuration

## Intégration Continue

Le projet utilise GitHub Actions pour l'intégration continue avec deux workflows principaux :

### Workflow de Tests (`tests.yml`)

```yaml
- Exécution des tests sur Python 3.11, 3.12, 3.13
- Vérification du formatage avec black
- Analyse du code avec pylint
- Rapport de couverture avec pytest-cov
```

### Workflow de Documentation (`docs.yml`)

```yaml
- Construction de la documentation
- Déploiement sur GitHub Pages
```

## Suivi des Métriques

Les métriques de qualité sont suivies via des badges dans le README :

- [![Tests](https://github.com/rhinosys/SolarCalculet/actions/workflows/tests.yml/badge.svg)](https://github.com/rhinosys/SolarCalculet/actions/workflows/tests.yml)
- [![Documentation](https://github.com/rhinosys/SolarCalculet/actions/workflows/docs.yml/badge.svg)](https://github.com/rhinosys/SolarCalculet/actions/workflows/docs.yml)
- [![Code Quality](https://img.shields.io/badge/pylint-9.43%2F10-green)](https://github.com/rhinosys/SolarCalculet/actions)

## Vérification Locale

Pour vérifier la qualité du code localement :

```bash
# Installation des outils
pip install black pylint pytest-cov

# Formatage du code
black src tests

# Analyse du code
pylint src/solarcalculet tests

# Tests avec couverture
pytest --cov=src/solarcalculet tests/
```

## Règles de Contribution

Pour maintenir ces standards de qualité, toute contribution doit :

1. Passer tous les tests
2. Maintenir ou améliorer le score pylint
3. Être formatée avec black
4. Inclure des tests pour les nouvelles fonctionnalités
5. Mettre à jour la documentation si nécessaire

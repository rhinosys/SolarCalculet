# SolarCalculet

[![Tests](https://github.com/rhinosys/SolarCalculet/actions/workflows/tests.yml/badge.svg)](https://github.com/rhinosys/SolarCalculet/actions/workflows/tests.yml)
[![Documentation](https://github.com/rhinosys/SolarCalculet/actions/workflows/docs.yml/badge.svg)](https://github.com/rhinosys/SolarCalculet/actions/workflows/docs.yml)
[![Code Quality](https://img.shields.io/badge/pylint-9.43%2F10-green)](https://github.com/rhinosys/SolarCalculet/actions)

Outil de traitement des données de consommation ENEDIS pour l'analyse énergétique et le dimensionnement solaire.

## 🎯 Fonctionnalités

- Lecture et validation des fichiers de consommation ENEDIS (CSV)
- Nettoyage et complétion des données manquantes
- Export au format Excel compatible avec les outils de dimensionnement solaire
- Tests unitaires et d'intégration complets
- Documentation détaillée

## 📦 Installation

```bash
# Cloner le dépôt
git clone https://github.com/rhinosys/SolarCalculet.git
cd SolarCalculet

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Unix/macOS
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation

1. Préparez votre fichier de données ENEDIS au format CSV
2. Exécutez l'outil :
```bash
python -m solarcalculet votre_fichier.csv
```
3. Récupérez les fichiers Excel générés pour 2023 et 2024

## 🧪 Tests et Qualité du Code

Le projet suit une approche TDD (Test-Driven Development) et maintient des standards de qualité élevés :

```bash
# Exécuter les tests
pytest

# Vérifier la qualité du code
pylint src/solarcalculet tests  # Score actuel : 9.43/10
```

### 📊 Métriques de Qualité

- Coverage des tests : 100%
- Score pylint : 9.43/10
- Formatage : black
- CI/CD : GitHub Actions

## 📚 Documentation

La documentation complète est disponible sur [GitHub Pages](https://rhinosys.github.io/SolarCalculet/).

- [Format des fichiers](https://rhinosys.github.io/SolarCalculet/file-format)
- [Guide des tests](https://rhinosys.github.io/SolarCalculet/testing)

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [guide de contribution](CONTRIBUTING.md) pour commencer.

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
- Ajouter une gestion des erreurs plus robuste en cas de fichiers corrompus.
- Permettre une sortie au format JSON ou autre pour plus de flexibilité.

---

📧 **Contact** : Si vous avez des questions ou suggestions, n’hésitez pas à ouvrir une issue ou à contacter l’auteur. 🚀

# SOURCE
https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html
https://eu5.fusionsolar.huawei.com/unisso/login.action?service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252Fnetecowebext%252Fhome%252Findex.html#/LOGIN


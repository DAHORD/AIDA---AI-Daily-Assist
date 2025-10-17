# Contributing to AI Daily Assist (AIDA)

Merci d'envisager une contribution ! Ce document explique comment configurer un environnement local, les bonnes pratiques de contribution, et le flux de travail recommandé pour envoyer des issues et des Pull Requests (PR).

---

## Table des matières

- Avant de commencer
- Configuration locale
- Installer les dépendances
- Exemples de lancement
- Gestion des clés API et fichiers de configuration
- Style de code & qualité
- Branching et conventions de commit
- Ouvrir une issue
- Ouvrir une Pull Request
- Revue & fusion
- Tests et CI
- Sécurité et divulgation responsable

---

## Avant de commencer

1. Forkez le dépôt et clonez votre fork :
```bash
git clone https://github.com/<votre-compte>/AIDA---AI-Daily-Assist.git
cd AIDA---AI-Daily-Assist
```

2. Créez une branche pour votre travail :
```bash
git checkout -b feat/ma-fonctionnalite
```

---

## Configuration locale

Utilisez un environnement virtuel Python pour isoler les dépendances :

Linux / macOS :
```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell :
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Installez les dépendances listées dans `requirements.txt` :
```bash
pip install -r requirements.txt
```

---

## Exemples de lancement

- Version française (terminal) :
```bash
python fr/assistant_cmd.py
```

- Version anglaise (terminal) :
```bash
python en/assistant_cmd_en.py
```

- Launcher (vérifier que PYTHON_EXECUTABLE et SCRIPT_TO_RUN sont corrects) :
```bash
python fr/launcher.py
# ou
python en/launcher_en.py
```

---

## Gestion des clés API et fichiers de configuration

Certaines fonctionnalités (météo, actualités, taux de change, blagues) nécessitent des clés API. Créez `config.ini` dans le dossier de données utilisateur. L'application crée / lit ce fichier dans :

- Windows : `%APPDATA%\AI Daily Assist\config.ini` (ex: C:\Users\<user>\AppData\Roaming\AI Daily Assist\config.ini)

Exemple minimal `config.ini` :
```ini
[API_KEYS]
exchangerate_api_key = VOTRE_CLE_EXCHANGERATE
weatherapi_key = VOTRE_CLE_WEATHERAPI
gnews_api_key = VOTRE_CLE_GNEWS
blagues_api_key = VOTRE_CLE_BLAUGES_API
```

Ne commitez JAMAIS vos clés API. Ajoutez un rappel dans les PR si votre changement aide la configuration.

---

## Style de code & qualité

- Utilisez Python 3.8+
- Respectez la PEP8.
- Outils recommandés (optionnel, pour développeurs) :
  - black
  - isort
  - flake8
  - pre-commit

Exemples d'installation (dev) :
```bash
pip install black isort flake8 pre-commit
pre-commit install
```

Formatez votre code avant de soumettre une PR :
```bash
black .
isort .
flake8
```

---

## Branching et conventions de commit

- Branches :
  - `main` — code stable publié
  - `feat/...` — nouvelles fonctionnalités
  - `fix/...` — corrections de bugs
  - `chore/...` — tâches d'infrastructure, docs, maintenance

- Conventions de commit (exemples) :
  - feat: add todo interactive improvements
  - fix: handle missing config.ini gracefully
  - docs: add CONTRIBUTING.md and requirements.txt
  - chore: update dependencies

Rédigez des messages clairs décrivant le quoi et le pourquoi.

---

## Ouvrir une Issue

Avant d'ouvrir une issue :
- Recherchez les issues existantes pour éviter les doublons.
- Si vous rapportez un bug, incluez :
  - Système d'exploitation et version
  - Version de Python
  - Étapes pour reproduire
  - Journal d'erreur (stack trace)
- Si vous proposez une fonctionnalité, décrivez le cas d'usage et une proposition d'interface (commandes / options).

---

## Ouvrir une Pull Request

1. Poussez votre branche sur votre fork :
```bash
git push origin feat/ma-fonctionnalite
```

2. Ouvrez une PR vers `DAHORD/AIDA---AI-Daily-Assist:main` en décrivant :
- Contexte et objectif
- Changements effectués (fichiers modifiés)
- Instructions pour tester localement
- Screenshots / logs si utile

3. Ajoutez des tests si possible et documentez toute nouvelle configuration requise.

---

## Revue & fusion

- Les mainteneurs peuvent demander des changements ou suggestions.
- Une fois approuvée, la PR sera fusionnée selon la politique du dépôt.
- Si votre PR a des impacts sur la sécurité (ex: nouvelle clé API à obtenir), documentez les étapes pour les utilisateurs.

---

## Tests et CI

- Actuellement, il peut ne pas y avoir de suite de tests intégrée. Si vous ajoutez des tests :
  - Utilisez `pytest`
  - Documentez comment exécuter les tests (ex: `pytest tests/`)

- Pour CI, suggérez ou ajoutez un workflow GitHub Actions qui :
  - installe les dépendances
  - exécute flake8 / black --check
  - exécute pytest (si présent)

---

## Sécurité et divulgation responsable

- Ne publiez pas de clés API dans le code.
- Si vous découvrez une vulnérabilité :
  - Créez une issue marquée `security` (privée si nécessaire) ou contactez l'auteur par e-mail pour divulgation responsable (klh08@free.fr est présent dans le repo).
- Si vous fournissez un binaire (ex: `setup-aida.exe`), donnez des détails sur la procédure de build pour auditabilité.

---

## Merci

Merci d'améliorer AIDA ! Si vous voulez, proposez une PR pour ajouter :
- un `requirements-dev.txt` (dev dependencies et hooks),
- un `pre-commit` config,
- un workflow CI GitHub Actions (lint + tests).

Nous sommes impatients de parcourir vos contributions.
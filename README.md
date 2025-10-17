# AI Daily Assist (AIDA)

AI Daily Assist — ou AIDA — est un assistant en ligne de commande conçu pour améliorer votre productivité quotidienne. Il regroupe des outils pratiques (gestion de tâches, conversion, recherche dans les fichiers), des utilitaires système, des mini-outils web (météo, actualités, définitions), et des fonctions créatives (QR code, ASCII art, générateur de mots de passe). L'interface se veut simple, interactive et agréable grâce à la bibliothèque rich.

Version courante : v3.0
Auteur : DAHORD  
Site : https://ai-daily-assist.x10.mx
Repo : https://github.com/DAHORD/AIDA---AI-Daily-Assist

---

Table des matières

- Présentation
- Fonctionnalités
- Prérequis
- Installation
- Configuration (config.ini)
- Utilisation (commandes principales)
- Lancer le programme
- Paquet d'installation / Setup
- Contribution
- Dépannage
- Licence & Contact

---

## Présentation

AIDA transforme votre terminal en un assistant polyvalent. Il fonctionne principalement sous Python et propose des interactions guidées (prompts) pour chaque commande. L'interface console utilise la librairie rich pour afficher des tableaux, panneaux et animations.

## Fonctionnalités principales

- Gestion de tâches (todo) : ajout, liste, suppression, suppression totale.
- Convertisseur de devises (convert) via ExchangeRate API.
- Recherche de texte dans des fichiers d'un dossier (search).
- Affichage de l'arborescence d'un dossier (tree).
- Utilitaires disque et système : disk, sys.
- Organisation de fichiers par extension (org).
- Météo (weather / meteo) via WeatherAPI.
- Actualités (news) via GNews.
- Raccourcisseur d'URL (tinyurl).
- Requêtes Wikipédia (wiki) et définitions (def).
- Génération de QR Code (qrcode), ASCII art (ascii).
- Générateur de mot de passe sécurisé (pass / mdp).
- Minuteur (timer).
- Blagues catégorisées (blg / joke) via API (optionnelle).
- Affichage IP publique (ip).
- Interface bilingue FR / EN (dossiers `fr/` et `en/`).

## Prérequis

- Python 3.8+ recommandé
- Packages Python (voir plus bas pour l'installation) :
  - requests
  - wikipediaapi
  - qrcode
  - Pillow (PIL)
  - pyfiglet
  - beautifulsoup4
  - rich
  - psutil

Exemple d'installation des dépendances :

```bash
pip install -r requirements.txt
```

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/DAHORD/AIDA---AI-Daily-Assist.git
cd AIDA---AI-Daily-Assist
```

2. Installez les dépendances (voir la section Prérequis).

3. Configurez vos clés API (fichier `config.ini`, voir ci-dessous).

## Configuration (config.ini)

Certaines fonctionnalités utilisent des API externes (WeatherAPI, ExchangeRate, GNews, API de blagues). Créez un fichier `config.ini` dans le dossier d'application (AIDA crée automatiquement un dossier AppData/Roaming/AI Daily Assist). Exemple de fichier `config.ini` :

```ini
[API_KEYS]
exchangerate_api_key = VOTRE_CLE_EXCHANGERATE
weatherapi_key = VOTRE_CLE_WEATHERAPI
gnews_api_key = VOTRE_CLE_GNEWS
blagues_api_key = VOTRE_CLE_BLAUGES_API
```

- Si vous n'avez pas toutes les clés, l'application affiche un message et certaines commandes ne fonctionneront pas (des alternatives simples sont parfois fournies).

## Emplacement des fichiers de configuration et de tâches

AIDA utilise le dossier de l'utilisateur :

- Windows : %USERPROFILE%\AppData\Roaming\AI Daily Assist
- Fichiers importants :
  - `todolist.json` — stockage local des tâches
  - `config.ini` — clés API

## Utilisation — commandes principales

(Les commandes existent en version française et anglaise suivant le dossier / script que vous lancez.)

Productivité

- todo — Mode gestionnaire de tâches (add, list, del <#>, clear)
- convert — Convertisseur de devises
- search — Recherche de texte dans les fichiers d'un dossier

Utilitaires

- tree — Affiche l'arborescence d'un dossier
- disk — Affiche l'utilisation disque
- org — Organise les fichiers par extension
- sys — Affiche l'utilisation CPU et RAM

Web & Réseau

- weather (meteo) — Météo (WeatherAPI)
- news — Actualités (GNews)
- ip — Montre l'IP publique
- shorten (ou url) — Raccourcit une URL
- wiki — Résumé Wikipédia
- def — Définitions (API dictionnaire ou scraping Larousse selon la langue)
- blg / joke — Raconte une blague par thème (optionnel)

Créatif & divers

- qrcode — Génère un QR Code PNG
- ascii — Transforme du texte en ASCII art
- pass / mdp — Génère un mot de passe aléatoire
- timer — Minuteur

## Lancer le programme

Deux manières courantes :

1. Lancer directement le script Python (recommandé pendant le développement) :

- Version anglaise :

```bash
python en/assistant_cmd_en.py
```

- Version française :

```bash
python fr/assistant_cmd.py
```

2. Utiliser les launchers fournis (ils tentent d'ouvrir le script principal) :

- Version anglaise : `en/launcher_en.py` — veillez à ce que le nom du script cible (défini dans la variable `SCRIPT_TO_RUN`) corresponde. Par défaut, le launcher essaie d'exécuter `assistant_cmd.py` dans le même dossier. Ajustez si nécessaire.
- Version française : `fr/launcher.py`

Note : Les scripts `launcher_*.py` utilisent `subprocess.Popen` pour démarrer l'assistant et fermer le launcher. Ils supposent que `python` est disponible dans le PATH. Vous pouvez modifier `PYTHON_EXECUTABLE` si besoin.

## Paquet d'installation / Setup

Un installeur Windows est inclus dans le dossier `setup/` : `setup-aida.exe`. Téléchargez et utilisez-le à vos risques et périls — faites confiance à la source et vérifiez le repo. Le fichier binaire est fourni tel quel ; vous pouvez préférer lancer les scripts Python directement pour plus de transparence.

## Personnalisation & traduction

Le projet contient déjà des versions française et anglaise du terminal (`fr/` et `en/`). Vous pouvez :

- Traduire les invites ou ajouter d'autres langues.
- Créer une interface graphique (GUI) en utilisant la fonction `process_command(...)` comme cœur logique — elle a été pensée pour être appelée depuis un GUI.

## Contribuer

Contributions bienvenues ! Suggestions typiques :

- Améliorer l'UX des prompts.
- Ajouter des tests unitaires.
- Corriger des bugs et rendre l'installation plus simple (packaging pip, wheel).
- Ajouter d'autres API / intégrations.

Processus recommandé :

1. Forkez le dépôt.
2. Créez une branche feature/bugfix.
3. Ouvrez une Pull Request avec une description claire.

## Dépannage rapide

- Erreur : "Configuration file not found" — créez `config.ini` dans %APPDATA%/AI Daily Assist (ou laissez vide si vous n'utilisez pas d'API).
- Le launcher ne démarre pas : vérifiez la valeur de `PYTHON_EXECUTABLE` et la présence du script ciblé.
- Problèmes de dépendances : utilisez un environnement virtuel :

```bash
python -m venv .venv
source .venv\Scripts\activate (sur Windows)
pip install -r requirements.txt
```

## Sécurité & vie privée

- Les données locales (tâches) sont stockées en clair dans `todolist.json` sous le dossier AppData/Roaming/AI Daily Assist.
- Aucune donnée n'est envoyée au dépôt GitHub. Les API externes (météo, news, blagues, taux de change) sont appelées selon les clés fournies dans `config.ini`. Protégez vos clés.
- L'exécutable `setup-aida.exe` est fourni pour faciliter l'installation Windows — analysez-le avant usage si vous avez des doutes.

## Licence

Projet open source, consulter la LICENSE

## Contact

Auteur : DAHORD  
Repo : https://github.com/DAHORD/AIDA---AI-Daily-Assist  
Site : https://ai-daily-assist.x10.mx
Email : klh08@free.fr (mentionné en bas de la page d'accueil du site)

---

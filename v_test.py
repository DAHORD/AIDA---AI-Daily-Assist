import os
import random
import string
import requests
import configparser
import psutil
import shutil
import time
import wikipediaapi
import qrcode
import json
from PIL import Image
import pyfiglet
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.tree import Tree
from rich.live import Live
from rich.text import Text
from rich.highlighter import ReprHighlighter

# --- Initialisation ---
console = Console()
wiki_wiki = wikipediaapi.Wikipedia('MonAssistantTerminal/1.0', 'fr')
TODO_FILE = "todolist.json"

# --- Fonctions de Configuration et d'Aide ---

def charger_cles_api():
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        console.print("[bold red]Erreur : Le fichier 'config.ini' est introuvable.[/bold red]")
        return {}
    config.read('config.ini')
    if 'API_KEYS' not in config:
        console.print("[bold red]Erreur : Section [API_KEYS] manquante dans 'config.ini'.[/bold red]")
        return {}
    return config['API_KEYS']

def afficher_aide():
    table = Table(title="💎 Commandes Disponibles v5.0 💎", style="cyan", header_style="bold magenta")
    table.add_column("Commande (Alias)", justify="right")
    table.add_column("Description")
    
    commandes_aide = {
        "--- Productivité ---": "",
        "todo": "Gestionnaire de tâches (add, list, del, clear).",
        "convert": "Convertisseur de devises.",
        "search": "Cherche un texte dans les fichiers d'un dossier.",
        "--- Utilitaires ---": "",
        "tree": "Affiche l'arborescence d'un dossier.",
        "disk": "Montre l'utilisation de l'espace disque.",
        "org": "Organise les fichiers par extension.",
        "sys": "Affiche l'utilisation CPU et RAM.",
        "--- Outils Web ---": "",
        "meteo": "Affiche la météo actuelle.",
        "news": "Recherche des actualités.",
        "ip": "Affiche votre IP publique.",
        "shorten (url)": "Raccourcit une URL.",
        "wiki": "Cherche un résumé sur Wikipédia.",
        "def": "Donne la définition d'un mot.",
        "--- Outils Créatifs ---": "",
        "qrcode": "Génère un QR Code en image (.png).",
        "ascii": "Convertit un texte en art ASCII.",
        "mdp": "Génère un mot de passe sécurisé.",
        "timer": "Lance un compte à rebours.",
        "blg (joke)": "Raconte une blague par thème.",
        "--- Général ---": "",
        "help": "Affiche ce message d'aide.",
        "q (quit, exit)": "Termine le programme."
    }
    
    for cmd, desc in commandes_aide.items():
        if "---" in cmd:
            table.add_row(f"[bold yellow]{cmd}[/bold yellow]", "")
        else:
            table.add_row(f"[bold green]{cmd}[/bold green]", desc)
    console.print(table)

# --- Fonctions de Productivité ---

def charger_taches():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def sauvegarder_taches(taches):
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(taches, f, indent=4, ensure_ascii=False)

def _afficher_liste_taches():
    """Helper interne pour afficher la table des tâches."""
    taches = charger_taches()
    table = Table(title="📝 Ma To-Do List", style="green", show_header=True, header_style="bold magenta")
    table.add_column("N°", style="bold cyan", width=4)
    table.add_column("Tâche", style="white")
    
    if not taches:
        table.add_row("🎉", "Aucune tâche pour le moment. Bravo !")
    else:
        for i, tache in enumerate(taches):
            table.add_row(str(i + 1), tache)
            
    console.print(table)

def gerer_todo(args):
    """Point d'entrée pour la gestion des tâches. Gère les commandes directes et le mode interactif."""

    # --- Gestion des commandes directes (ex: todo add ...) ---
    if args:
        taches = charger_taches()
        action = args[0]
        
        if action == "add":
            if len(args) < 2:
                console.print("[red]Veuillez spécifier une tâche à ajouter.[/red]")
                return
            tache = " ".join(args[1:])
            taches.append(tache)
            sauvegarder_taches(taches)
            console.print(f"[green]✅ Tâche ajoutée : '{tache}'[/green]")
        elif action == "list":
            _afficher_liste_taches()
        elif action == "del":
            try:
                index = int(args[1]) - 1
                if 0 <= index < len(taches):
                    tache_supprimee = taches.pop(index)
                    sauvegarder_taches(taches)
                    console.print(f"[red]❌ Tâche supprimée : '{tache_supprimee}'[/red]")
                else:
                    console.print("[red]Numéro de tâche invalide.[/red]")
            except (IndexError, ValueError):
                console.print("[red]Veuillez fournir un numéro de tâche valide à supprimer.[/red]")
        elif action == "clear":
            sauvegarder_taches([])
            console.print("[bold red]🗑️ Toutes les tâches ont été supprimées.[/bold red]")
        else:
            console.print(f"[red]Action '{action}' non reconnue.[/red]")
        return

    # --- Mode interactif (si 'todo' est tapé seul) ---
    console.print(Panel(
        "Vous êtes en mode [bold]To-Do[/bold]. Commandes : [cyan]add[/cyan], [cyan]list[/cyan], [cyan]del <n°>[/cyan], [cyan]clear[/cyan], [cyan]exit[/cyan].",
        title="📝 Gestionnaire de Tâches",
        border_style="green"
    ))
    
    _afficher_liste_taches()

    while True:
        try:
            entree = Prompt.ask("\n[bold](todo) >>> [/bold]").strip()
            if not entree:
                continue

            parties = entree.split()
            commande = parties[0].lower()
            args_todo = parties[1:]
            
            taches = charger_taches() # Recharger les tâches à chaque commande

            if commande in ["exit", "q", "back"]:
                console.print("[yellow]Retour au menu principal.[/yellow]")
                break
            elif commande == "add":
                if not args_todo:
                    console.print("[red]Veuillez spécifier une tâche à ajouter.[/red]")
                    continue
                tache = " ".join(args_todo)
                taches.append(tache)
                sauvegarder_taches(taches)
                console.print(f"[green]✅ Tâche ajoutée.[/green]")
                _afficher_liste_taches()
            elif commande == "list":
                _afficher_liste_taches()
            elif commande == "del":
                try:
                    index = int(args_todo[0]) - 1
                    if 0 <= index < len(taches):
                        taches.pop(index)
                        sauvegarder_taches(taches)
                        console.print("[red]❌ Tâche supprimée.[/red]")
                        _afficher_liste_taches()
                    else:
                        console.print("[red]Numéro invalide.[/red]")
                except (IndexError, ValueError):
                    console.print("[red]Usage : del <numéro>[/red]")
            elif commande == "clear":
                sauvegarder_taches([])
                console.print("[bold red]🗑️ Toutes les tâches ont été supprimées.[/bold red]")
                _afficher_liste_taches()
            elif commande == "help":
                 console.print("Commandes : [cyan]add <tâche>[/cyan], [cyan]list[/cyan], [cyan]del <n°>[/cyan], [cyan]clear[/cyan], [cyan]exit[/cyan].")
            else:
                console.print("[red]Commande non reconnue. Tapez 'help' pour de l'aide.[/red]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Retour au menu principal.[/yellow]")
            break

def convertir_devises():
    api_keys = charger_cles_api()
    api_key = api_keys.get('exchangerate_api_key')
    if not api_key or "VOTRE_CLE" in api_key:
        console.print("[yellow]Clé API pour ExchangeRate non configurée dans config.ini.[/yellow]")
        return
    
    try:
        montant = float(Prompt.ask("[cyan]Montant à convertir[/cyan]"))
        devise_base = Prompt.ask("[cyan]Devise de base (ex: EUR)[/cyan]").upper()
        devise_cible = Prompt.ask("[cyan]Devise cible (ex: USD)[/cyan]").upper()

        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{devise_base}"
        with console.status("[yellow]Récupération des taux de change...[/yellow]"):
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        
        if data['result'] == 'success':
            taux = data['conversion_rates'].get(devise_cible)
            if taux:
                resultat = montant * taux
                console.print(f"[bold green]✅ {montant} {devise_base} = {resultat:.2f} {devise_cible}[/bold green]")
            else:
                console.print(f"[red]Devise cible '{devise_cible}' non trouvée.[/red]")
        else:
            console.print(f"[red]Erreur de l'API : {data.get('error-type', 'inconnue')}[/red]")

    except ValueError:
        console.print("[red]Veuillez entrer un montant numérique valide.[/red]")
    except requests.exceptions.HTTPError as err:
        console.print(f"[red]Erreur HTTP : {err.response.status_code}. Vérifiez vos devises ou votre clé API.[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Erreur de connexion : {e}[/red]")

def rechercher_dans_fichiers():
    terme = Prompt.ask("[cyan]Texte à rechercher[/cyan]")
    dossier = Prompt.ask("[cyan]Dans quel dossier chercher ?[/cyan]", default=".")
    if not os.path.isdir(dossier):
        console.print(f"[red]Dossier '{dossier}' introuvable.[/red]")
        return

    highlighter = ReprHighlighter()
    compteur = 0
    with console.status(f"[yellow]Recherche de '{terme}'...[/yellow]"):
        for root, _, files in os.walk(dossier):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for num_ligne, ligne in enumerate(f, 1):
                            if terme in ligne:
                                if compteur == 0:
                                    console.print("\n[bold green]--- Résultats trouvés ---[/bold green]")
                                console.print(f"📄 [blue]{path}[/blue]:[yellow]{num_ligne}[/yellow]")
                                console.print(highlighter(ligne.strip()))
                                compteur += 1
                except Exception:
                    continue
    if compteur == 0:
        console.print("[yellow]Aucun résultat trouvé.[/yellow]")

# --- Outils Créatifs & Pratiques ---

def raconter_blague():
    """Raconte une blague en utilisant l'API Blagues-API et en demandant un thème."""
    api_keys = charger_cles_api()
    api_key = api_keys.get('blagues_api_key')

    if not api_key or "VOTRE_CLE" in api_key:
        console.print("[bold yellow]Clé API pour les blagues non configurée dans config.ini.[/bold yellow]")
        console.print("Sauvegarde sur une blague hors ligne :")
        console.print(f"\n[italic]Pourquoi les plongeurs tombent-ils toujours en arrière du bateau ?\n... Parce que sinon ils tomberaient dans le bateau.[/italic]")
        return

    themes = {
        "1": ("Général", "global"),
        "2": ("Développeur", "dev"),
        "3": ("Blond", "blondes"),
        "4": ("Toto", "toto"),
        "5": ("Beauf", "beauf"),
        "6": ("Humour noir", "dark"),
    }

    console.print("\n[bold]Choisissez un thème pour la blague :[/bold]")
    for key, (label, _) in themes.items():
        console.print(f"  [cyan]{key}[/cyan] - {label}")
    
    choix_theme = Prompt.ask("[bold]Votre choix[/bold]", choices=themes.keys(), default="1")
    categorie = themes[choix_theme][1]
    
    url = f"https://www.blagues-api.fr/api/type/{categorie}/random"
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        with console.status("[yellow]Je cherche une bonne blague...[/yellow]"):
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        blague = data['joke']
        reponse_blague = data['answer']
        
        console.print(Panel(
            f"[italic cyan]{blague}[/italic cyan]",
            title="Devinette...",
            border_style="blue"
        ))
        
        Prompt.ask("\n[bold](Appuyez sur Entrée pour la réponse)[/bold]")
        
        console.print(Panel(
            f"[bold green]{reponse_blague}[/bold green]",
            title="La chute !",
            border_style="green"
        ))

    except requests.exceptions.HTTPError as err:
        if err.response.status_code in [401, 403]:
            console.print("[bold red]Erreur : Clé API pour les blagues invalide. Vérifiez votre config.ini.[/bold red]")
        else:
            console.print(f"[bold red]Erreur HTTP en contactant l'API des blagues : {err}[/bold red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Erreur de connexion : {e}[/bold red]")


# --- Utilitaires Fichiers & Système ---
def afficher_arborescence():
    path_str = Prompt.ask("[cyan]Entrez le chemin du dossier à inspecter[/cyan]", default=".")
    if not os.path.isdir(path_str):
        console.print(f"[red]Erreur : Le dossier '{path_str}' n'existe pas.[/red]")
        return

    tree = Tree(f"📁 [bold blue]{os.path.abspath(path_str)}[/bold blue]")
    try:
        paths = sorted(os.listdir(path_str))
        for path in paths:
            if os.path.isdir(os.path.join(path_str, path)):
                tree.add(f"📁 [blue]{path}[/blue]")
            else:
                tree.add(f"📄 [green]{path}[/green]")
    except Exception as e:
        console.print(f"[red]Une erreur est survenue : {e}[/red]")
    
    console.print(tree)

def afficher_usage_disque():
    table = Table(title="💿 Utilisation des Disques", style="yellow", header_style="bold blue")
    table.add_column("Périphérique", justify="left")
    table.add_column("Total", justify="right")
    table.add_column("Utilisé", justify="right")
    table.add_column("Libre", justify="right")
    table.add_column("Pourcentage", justify="center")

    for part in psutil.disk_partitions():
        if os.name == 'nt' or part.mountpoint == '/' or part.mountpoint.startswith('/System'):
             try:
                usage = psutil.disk_usage(part.mountpoint)
                total = f"{usage.total / (1024**3):.2f} Go"
                used = f"{usage.used / (1024**3):.2f} Go"
                free = f"{usage.free / (1024**3):.2f} Go"
                percent = f"[bold {'red' if usage.percent > 85 else 'green'}]{usage.percent}%[/bold {'red' if usage.percent > 85 else 'green'}]"
                table.add_row(part.mountpoint, total, used, free, percent)
             except (PermissionError, FileNotFoundError):
                 continue
    console.print(table)
    
def organiser_fichiers():
    chemin = Prompt.ask("[cyan]Entrez le chemin du dossier à organiser[/cyan]")
    if not os.path.isdir(chemin):
        console.print(f"[red]Ce dossier n'existe pas : {chemin}[/red]")
        return

    compteur = 0
    with console.status("[bold green]Organisation en cours...[/bold green]"):
        for fichier in os.listdir(chemin):
            if os.path.isfile(os.path.join(chemin, fichier)):
                extension = fichier.split('.')[-1].lower() if '.' in fichier else 'sans_extension'
                dossier_dest = os.path.join(chemin, extension)
                if not os.path.exists(dossier_dest):
                    os.makedirs(dossier_dest)
                shutil.move(os.path.join(chemin, fichier), os.path.join(dossier_dest, fichier))
                compteur += 1
    
    console.print(f"\n[bold green]✅ {compteur} fichier(s) organisé(s) avec succès dans '{chemin}' ![/bold green]")


# --- Outils Web & Réseau ---
def obtenir_meteo():
    # On récupère le dictionnaire de clés, puis la clé spécifique.
    api_keys = charger_cles_api()
    api_key = api_keys.get('weatherapi_key')

    if not api_key or "VOTRE_CLE" in api_key:
        console.print("[bold yellow]Clé API météo (WeatherAPI) non configurée dans config.ini.[/bold yellow]")
        return

    ville = Prompt.ask("[bold cyan]Entrez le nom de la ville[/bold cyan]", default="La Neuville-Roy")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={ville}&lang=fr"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        panel_content = (
            f"[bold]Météo pour {data['location']['name']}, {data['location']['country']}[/bold]\n"
            f"Condition : [yellow]{data['current']['condition']['text']}[/yellow]\n"
            f"Température : [bold bright_magenta]{data['current']['temp_c']}°C[/bold bright_magenta] (Ressenti : {data['current']['feelslike_c']}°C)\n"
            f"Humidité : {data['current']['humidity']}% | Vent : {data['current']['wind_kph']} km/h"
        )
        console.print(Panel(panel_content, title="☀️ Météo Fiable", border_style="blue", expand=False))

    except requests.exceptions.HTTPError as err:
        if err.response.status_code in [401, 403]:
            console.print("[bold red]Erreur : Clé API invalide. Vérifiez votre config.ini.[/bold red]")
        elif err.response.status_code == 400:
            console.print(f"[bold red]Ville '{ville}' non trouvée ou requête invalide.[/bold red]")
        else:
            console.print(f"[bold red]Erreur HTTP : {err}[/bold red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Erreur de connexion : {e}[/bold red]")

def obtenir_actualites():
    api_keys = charger_cles_api()
    api_key = api_keys.get('gnews_api_key')

    if not api_key or "VOTRE_CLE" in api_key:
        console.print("[bold yellow]Clé API news (GNews) non configurée dans config.ini.[/bold yellow]")
        return

    categories = { "1": ("Général", "general"), "2": ("Monde", "world"), "3": ("France", "nation"), "4": ("Business/Éco", "business"), "5": ("Technologie", "technology"), "6": ("Divertissement", "entertainment"), "7": ("Sport", "sports"), "8": ("Science", "science"), "9": ("Santé", "health") }
    console.print("\n[bold]Choisissez une catégorie d'actualités :[/bold]")
    for key, (label, _) in categories.items(): console.print(f"  [cyan]{key}[/cyan] - {label}")

    choix_cat = Prompt.ask("[bold]Votre choix[/bold]", choices=categories.keys(), default="1")
    topic = categories[choix_cat][1]
    keyword = Prompt.ask("\n[bold cyan]Entrez un mot-clé (ex: Le Monde, écologie) ou laissez vide[/bold cyan]", default="").strip()
    url = f"https://gnews.io/api/v4/top-headlines?lang=fr&country=fr&topic={topic}&token={api_key}"
    if keyword: url += f"&q={keyword}"

    try:
        with console.status("[bold green]Recherche des actualités...[/bold green]"):
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

        if not data.get("articles"):
            console.print("[yellow]Aucun article trouvé pour ces critères.[/yellow]")
            return

        table = Table(title=f"📰 Actualités pour '{categories[choix_cat][0]}' avec le mot-clé '{keyword}'", style="yellow")
        table.add_column("N°", style="bold cyan")
        table.add_column("Titre", style="white", no_wrap=False)
        table.add_column("Source", style="green")
        for i, article in enumerate(data["articles"][:10]): table.add_row(str(i + 1), article['title'], article['source']['name'])
        console.print(table)
    except requests.exceptions.HTTPError as err:
        if err.response.status_code in [401, 403]: console.print("[bold red]Erreur : Clé API GNews invalide.[/bold red]")
        else: console.print(f"[bold red]Erreur HTTP : {err}[/bold red]")
    except requests.exceptions.RequestException as e: console.print(f"[bold red]Erreur de connexion : {e}[/bold red]")

def raccourcir_url():
    long_url = Prompt.ask("[cyan]Entrez l'URL à raccourcir[/cyan]")
    if not long_url.startswith(('http://', 'https://')):
        console.print("[red]URL invalide. Doit commencer par http:// ou https://[/red]")
        return
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        response.raise_for_status()
        console.print(f"🔗 URL raccourcie : [bold green]{response.text}[/bold green]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Impossible de raccourcir l'URL : {e}[/red]")

def resume_wiki():
    sujet = Prompt.ask("[cyan]Quel sujet cherchez-vous sur Wikipédia ?[/cyan]")
    with console.status(f"[bold green]Recherche de '{sujet}'...[/bold green]"):
        page = wiki_wiki.page(sujet)
    
    if not page.exists():
        console.print(f"[red]Désolé, aucune page trouvée pour '{sujet}'.[/red]")
        return
    
    panel_content = f"[bold]{page.title}[/bold]\n\n{page.summary[0:500]}..."
    console.print(Panel(panel_content, title="📖 Résumé Wikipédia", border_style="yellow", subtitle=f"[link={page.fullurl}]Lire la suite[/link]"))

def definir_mot():
    mot = Prompt.ask("[bold cyan]Quel mot souhaitez-vous définir ?[/bold cyan]")
    url = f"https://www.larousse.fr/dictionnaires/francais/{mot}"

    try:
        with console.status(f"[yellow]Recherche de '{mot}' sur Larousse...[/yellow]"):
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

        definition_div = soup.find('ul', {'class': 'Definitions'})

        if definition_div:
            definitions_content = []
            definitions = definition_div.find_all('li', class_='DivisionDefinition')

            for i, definition in enumerate(definitions[:5]):
                for tag in definition.find_all(['span', 'p'], class_=['numDef', 'LibelleSynonyme', 'Synonymes']):
                    tag.decompose()
                
                definition_text = definition.get_text(separator=' ', strip=True)
                example_tag = definition.find('span', class_='ExempleDefinition')
                example_text = ""
                
                if example_tag:
                    example_text = example_tag.get_text(strip=True)
                    definition_text = definition_text.replace(example_text, '').strip()
                if definition_text.endswith(':'):
                    definition_text = definition_text[:-1].strip()

                definitions_content.append(f"[bold green]{i+1}.[/bold green] {definition_text}")
                if example_text:
                    definitions_content.append(f"   [italic red]Exemple : {example_text}[/italic red]\n")
                else:
                    definitions_content.append("")

            if len(definitions) > 5:
                definitions_content.append(f"[yellow]... et {len(definitions) - 5} autre(s) définition(s).[/yellow]")

            console.print(Panel(
                "\n".join(definitions_content), 
                title=f"[bold magenta]Définitions pour '{mot}'[/bold magenta]", 
                border_style="bold magenta",
                subtitle=f"[link={url}]Voir plus sur Larousse[/link]"
            ))

        else:
            console.print(f"[bold red]Aucune définition trouvée pour le mot '{mot}' sur Larousse.[/bold red]")
    
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Erreur de connexion : {e}[/red]")
    except Exception as e:
        console.print(f"[red]Une erreur inattendue est survenue : {e}[/red]")

def generer_qrcode():
    data = Prompt.ask("[cyan]Entrez le texte ou l'URL pour le QR Code[/cyan]")
    filename = Prompt.ask("[cyan]Nom du fichier de sortie (ex: site_web)[/cyan]", default="qrcode")
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    filepath = f"{filename}.png"
    img.save(filepath)
    console.print(f"[bold green]✅ QR Code sauvegardé avec succès sous le nom '{filepath}' ![/bold green]")

def art_ascii():
    texte = Prompt.ask("[cyan]Entrez le texte à convertir[/cyan]")
    police = Prompt.ask("[cyan]Choisissez une police (ex: standard, big, slant, small)[/cyan]", default="standard")
    try:
        ascii_art = pyfiglet.figlet_format(texte, font=police)
        console.print(f"[bold magenta]{ascii_art}[/bold magenta]")
    except pyfiglet.FontNotFound:
        console.print(f"[red]Police '{police}' non trouvée. Essayez une autre.[/red]")

def compte_a_rebours():
    try:
        secondes = int(Prompt.ask("[cyan]Entrez la durée en secondes pour le minuteur[/cyan]"))
        with Live(console=console, screen=False, auto_refresh=False) as live:
            for s in range(secondes, -1, -1):
                temps_restant = Text(f"⏳ Temps restant : {s} seconde{'s' if s > 1 else ''}", justify="center", style="bold green")
                live.update(Panel(temps_restant, title="Minuteur"), refresh=True)
                time.sleep(1)
        console.print("[bold yellow]⏰ Le temps est écoulé ![/bold yellow]")

    except ValueError:
        console.print("[red]Veuillez entrer un nombre entier de secondes.[/red]")

def info_systeme():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    console.print(f"🖥️ Utilisation [bold cyan]CPU[/bold cyan] : {cpu}% | [bold magenta]RAM[/bold magenta] : {ram}%")

def mon_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        console.print(f"🌍 Votre IP publique est : [bold green]{ip}[/bold green]")
    except requests.exceptions.RequestException:
        console.print("[bold red]Impossible de récupérer l'adresse IP.[/bold red]")

def generer_mdp():
    try:
        longueur = int(Prompt.ask("[bold cyan]Longueur du mot de passe[/bold cyan]", default="16"))
        caracteres = string.ascii_letters + string.digits + string.punctuation
        mdp = ''.join(random.choice(caracteres) for i in range(longueur))
        console.print(f"🔐 Mot de passe généré : [bold green]{mdp}[/bold green]")
    except ValueError:
        console.print("[red]Veuillez entrer un nombre valide.[/red]")

# --- MODIFICATION POUR L'INTEGRATION ---

def process_command(command_line: str, commandes: dict, aliases: dict):
    """
    Traite une seule ligne de commande. 
    Cette fonction est le cœur logique que notre GUI appellera.
    """
    if not command_line: return True # Continue la boucle

    parties = command_line.lower().strip().split()
    commande_base = parties[0]
    args = parties[1:]
    
    commande_resolue = aliases.get(commande_base, commande_base)

    if commande_resolue in ["q", "quit", "exit"]:
        console.print("[bold blue]À bientôt ![/bold blue]")
        return False # Arrête la boucle
    
    elif commande_resolue in commandes:
        try:
            if commande_resolue in ["todo"]:
                commandes[commande_resolue](args)
            else:
                commandes[commande_resolue]()
        except Exception as e:
            console.print(f"[bold red]Une erreur est survenue dans la commande '{commande_resolue}': {e}[/bold red]")
    else:
        console.print("[bold red]Commande non reconnue. Tapez 'help' pour de l'aide.[/bold red]")
    
    return True # Continue la boucle

def main():
    """Fonction principale pour l'exécution en mode terminal classique."""
    console.print(Panel("[bold green]🚀 Assistant de Terminal v5.0 - Mode Productivité 🚀[/bold green]", border_style="green"))
    console.print("Tapez '[cyan]help[/cyan]' pour voir la liste des commandes.")
    
    commandes = {
        "todo": gerer_todo, "convert": convertir_devises, "search": rechercher_dans_fichiers,
        "tree": afficher_arborescence, "disk": afficher_usage_disque, "org": organiser_fichiers, "sys": info_systeme,
        "meteo": obtenir_meteo, "news": obtenir_actualites, "ip": mon_ip, "shorten": raccourcir_url, 
        "wiki": resume_wiki, "def": definir_mot, "qrcode": generer_qrcode, "ascii": art_ascii, 
        "mdp": generer_mdp, "timer": compte_a_rebours, "blg": raconter_blague, "help": afficher_aide,
    }
    aliases = { "q": "q", "quit": "q", "exit": "q", "url": "shorten", "joke": "blg" }

    running = True
    while running:
        try:
            user_input = Prompt.ask(">>>")
            running = process_command(user_input, commandes, aliases)
            
        except EOFError: # Gère Ctrl+D
            running = False
        except KeyboardInterrupt: # Gère Ctrl+C
            console.print("\n[bold cyan]Fermeture forcée...[/bold cyan]")
            running = False

if __name__ == "__main__":
    main()
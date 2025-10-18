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

# --- Initialization ---
console = Console()
wiki_wiki = wikipediaapi.Wikipedia('MyTerminalAssistant/1.0', 'en') # Changed to 'en'

# --- Configuration and Helper Functions ---
APP_DATA_FOLDER_NAME = "AI Daily Assist"

def get_app_data_path(filename=""):
    app_data_root = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
    app_folder = os.path.join(app_data_root, APP_DATA_FOLDER_NAME)
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    return os.path.join(app_folder, filename)

TODO_FILE = get_app_data_path("todolist.json")
CONFIG_FILE = get_app_data_path("config.ini")

def load_api_keys():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        console.print(f"[bold red]Error: Configuration file not found at {CONFIG_FILE}.[/bold red]")
        return {}
    config.read(CONFIG_FILE)
    if 'API_KEYS' not in config:
        console.print("[bold red]Error: [API_KEYS] section missing in 'config.ini'.[/bold red]")
        return {}
    return config['API_KEYS']

def show_help():
    table = Table(title="💎 Available Commands v2.9 💎 by DAHORD", style="cyan", header_style="bold magenta")
    table.add_column("Command (Alias)", justify="right")
    table.add_column("Description")
    
    commands_help = {
        "--- Productivity ---": "",
        "todo": "Task manager (add, list, del, clear).",
        "convert": "Currency converter.",
        "search": "Searches for text within files in a directory.",
        "--- Utilities ---": "",
        "tree": "Displays the directory tree.",
        "disk": "Shows disk space usage.",
        "org": "Organizes files by extension.",
        "sys": "Displays CPU and RAM usage.",
        "--- Web Tools ---": "",
        "weather": "Displays the current weather.",
        "news": "Searches for news headlines.",
        "ip": "Displays your public IP address.",
        "shorten (url)": "Shortens a URL.",
        "wiki": "Searches for a summary on Wikipedia.",
        "def": "Provides the definition of a word.",
        "--- Creative Tools ---": "",
        "qrcode": "Generates a QR Code as a .png image.",
        "ascii": "Converts text to ASCII art.",
        "pass (mdp)": "Generates a secure password.",
        "timer": "Starts a countdown timer.",
        "--- General ---": "",
        "lang": "Changes the assistant's language (fr/en).",
        "help": "Displays this help message.",
        "q (quit, exit)": "Exits the program."
    }
    
    for cmd, desc in commands_help.items():
        if "---" in cmd:
            table.add_row(f"[bold yellow]{cmd}[/bold yellow]", "")
        else:
            table.add_row(f"[bold green]{cmd}[/bold green]", desc)
    console.print(table)

# --- Productivity Functions ---

def load_tasks():
    if not os.path.exists(TODO_FILE): return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w', encoding='utf-8') as f: json.dump(tasks, f, indent=4, ensure_ascii=False)

def _display_task_list():
    tasks = load_tasks()
    table = Table(title="📝 My To-Do List", style="green", show_header=True, header_style="bold magenta")
    table.add_column("#", style="bold cyan", width=4)
    table.add_column("Task", style="white")
    if not tasks:
        table.add_row("🎉", "No tasks at the moment. Well done!")
    else:
        for i, task in enumerate(tasks): table.add_row(str(i + 1), task)
    console.print(table)

def manage_todo(args):
    if args:
        tasks = load_tasks()
        action = args[0]
        if action == "add":
            if len(args) < 2: console.print("[red]Please specify a task to add.[/red]"); return
            task = " ".join(args[1:]); tasks.append(task); save_tasks(tasks)
            console.print(f"[green]✅ Task added: '{task}'[/green]")
        elif action == "list": _display_task_list()
        elif action == "del":
            try:
                index = int(args[1]) - 1
                if 0 <= index < len(tasks):
                    removed_task = tasks.pop(index); save_tasks(tasks)
                    console.print(f"[red]❌ Task removed: '{removed_task}'[/red]")
                else: console.print("[red]Invalid task number.[/red]")
            except (IndexError, ValueError): console.print("[red]Please provide a valid task number to delete.[/red]")
        elif action == "clear":
            save_tasks([]); console.print("[bold red]🗑️ All tasks have been deleted.[/bold red]")
        else: console.print(f"[red]Unknown action '{action}'.[/red]")
        return

    console.print(Panel("You are in [bold]To-Do[/bold] mode. Commands: [cyan]add[/cyan], [cyan]list[/cyan], [cyan]del <#>[/cyan], [cyan]clear[/cyan], [cyan]exit[/cyan].", title="📝 Task Manager", border_style="green"))
    _display_task_list()
    while True:
        try:
            entry = Prompt.ask("\n[bold](todo) >>> [/bold]").strip()
            if not entry: continue
            parts = entry.split(); command = parts[0].lower(); todo_args = parts[1:]
            tasks = load_tasks()
            if command in ["exit", "q", "back"]: console.print("[yellow]Returning to main menu.[/yellow]"); break
            elif command == "add":
                if not todo_args: console.print("[red]Please specify a task to add.[/red]"); continue
                task = " ".join(todo_args); tasks.append(task); save_tasks(tasks)
                console.print(f"[green]✅ Task added.[/green]"); _display_task_list()
            elif command == "list": _display_task_list()
            elif command == "del":
                try:
                    index = int(todo_args[0]) - 1
                    if 0 <= index < len(tasks):
                        tasks.pop(index); save_tasks(tasks)
                        console.print("[red]❌ Task removed.[/red]"); _display_task_list()
                    else: console.print("[red]Invalid number.[/red]")
                except (IndexError, ValueError): console.print("[red]Usage: del <number>[/red]")
            elif command == "clear":
                save_tasks([]); console.print("[bold red]🗑️ All tasks deleted.[/bold red]"); _display_task_list()
            elif command == "help": console.print("Commands: [cyan]add <task>[/cyan], [cyan]list[/cyan], [cyan]del <#>[/cyan], [cyan]clear[/cyan], [cyan]exit[/cyan].")
            else: console.print("[red]Unknown command. Type 'help' for assistance.[/red]")
        except KeyboardInterrupt: console.print("\n[yellow]Returning to main menu.[/yellow]"); break

def convert_currency():
    api_keys = load_api_keys(); api_key = api_keys.get('exchangerate_api_key')
    if not api_key or "YOUR_KEY" in api_key: console.print("[yellow]ExchangeRate API key not configured in config.ini.[/yellow]"); return
    try:
        amount = float(Prompt.ask("[cyan]Amount to convert[/cyan]"))
        base_currency = Prompt.ask("[cyan]Base currency (e.g., USD)[/cyan]").upper()
        target_currency = Prompt.ask("[cyan]Target currency (e.g., EUR)[/cyan]").upper()
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        with console.status("[yellow]Fetching exchange rates...[/yellow]"):
            response = requests.get(url); response.raise_for_status(); data = response.json()
        if data['result'] == 'success':
            rate = data['conversion_rates'].get(target_currency)
            if rate:
                result = amount * rate
                console.print(f"[bold green]✅ {amount} {base_currency} = {result:.2f} {target_currency}[/bold green]")
            else: console.print(f"[red]Target currency '{target_currency}' not found.[/red]")
        else: console.print(f"[red]API Error: {data.get('error-type', 'unknown')}[/red]")
    except ValueError: console.print("[red]Please enter a valid numeric amount.[/red]")
    except requests.exceptions.HTTPError as err: console.print(f"[red]HTTP Error: {err.response.status_code}. Check your currencies or API key.[/red]")
    except requests.exceptions.RequestException as e: console.print(f"[red]Connection error: {e}[/red]")

def search_in_files():
    term = Prompt.ask("[cyan]Text to search for[/cyan]")
    directory = Prompt.ask("[cyan]Directory to search in[/cyan]", default=".")
    if not os.path.isdir(directory): console.print(f"[red]Directory '{directory}' not found.[/red]"); return
    highlighter = ReprHighlighter(); count = 0
    with console.status(f"[yellow]Searching for '{term}'...[/yellow]"):
        for root, _, files in os.walk(directory):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if term in line:
                                if count == 0: console.print("\n[bold green]--- Found Results ---[/bold green]")
                                console.print(f"📄 [blue]{path}[/blue]:[yellow]{line_num}[/yellow]")
                                console.print(highlighter(line.strip())); count += 1
                except Exception: continue
    if count == 0: console.print("[yellow]No results found.[/yellow]")

def show_tree():
    path_str = Prompt.ask("[cyan]Enter the path to inspect[/cyan]", default=".")
    if not os.path.isdir(path_str): console.print(f"[red]Error: Directory '{path_str}' does not exist.[/red]"); return
    tree = Tree(f"📁 [bold blue]{os.path.abspath(path_str)}[/bold blue]")
    try:
        paths = sorted(os.listdir(path_str))
        for path in paths:
            if os.path.isdir(os.path.join(path_str, path)): tree.add(f"📁 [blue]{path}[/blue]")
            else: tree.add(f"📄 [green]{path}[/green]")
    except Exception as e: console.print(f"[red]An error occurred: {e}[/red]")
    console.print(tree)

def show_disk_usage():
    table = Table(title="💿 Disk Usage", style="yellow", header_style="bold blue")
    table.add_column("Device", justify="left"); table.add_column("Total", justify="right")
    table.add_column("Used", justify="right"); table.add_column("Free", justify="right"); table.add_column("Percentage", justify="center")
    for part in psutil.disk_partitions():
        if os.name == 'nt' or part.mountpoint == '/' or part.mountpoint.startswith('/System'):
             try:
                usage = psutil.disk_usage(part.mountpoint)
                total = f"{usage.total / (1024**3):.2f} GB"; used = f"{usage.used / (1024**3):.2f} GB"
                free = f"{usage.free / (1024**3):.2f} GB"
                percent = f"[bold {'red' if usage.percent > 85 else 'green'}]{usage.percent}%[/bold {'red' if usage.percent > 85 else 'green'}]"
                table.add_row(part.mountpoint, total, used, free, percent)
             except (PermissionError, FileNotFoundError): continue
    console.print(table)
    
def organize_files():
    path = Prompt.ask("[cyan]Enter the path of the directory to organize[/cyan]")
    if not os.path.isdir(path): console.print(f"[red]This directory does not exist: {path}[/red]"); return
    counter = 0
    with console.status("[bold green]Organizing files...[/bold green]"):
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                extension = filename.split('.')[-1].lower() if '.' in filename else 'no_extension'
                dest_dir = os.path.join(path, extension)
                if not os.path.exists(dest_dir): os.makedirs(dest_dir)
                shutil.move(os.path.join(path, filename), os.path.join(dest_dir, filename)); counter += 1
    console.print(f"\n[bold green]✅ Successfully organized {counter} file(s) in '{path}'![/bold green]")

def get_weather():
    api_keys = load_api_keys(); api_key = api_keys.get('weatherapi_key')
    if not api_key or "YOUR_KEY" in api_key: console.print("[bold yellow]WeatherAPI key not configured in config.ini.[/bold yellow]"); return
    city = Prompt.ask("[bold cyan]Enter city name[/bold cyan]", default="La Neuville-Roy")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=en"
    try:
        response = requests.get(url); response.raise_for_status(); data = response.json()
        panel_content = (f"[bold]Weather for {data['location']['name']}, {data['location']['country']}[/bold]\n"
                         f"Condition: [yellow]{data['current']['condition']['text']}[/yellow]\n"
                         f"Temperature: [bold bright_magenta]{data['current']['temp_c']}°C[/bold bright_magenta] (Feels like: {data['current']['feelslike_c']}°C)\n"
                         f"Humidity: {data['current']['humidity']}% | Wind: {data['current']['wind_kph']} kph")
        console.print(Panel(panel_content, title="☀️ Weather Report", border_style="blue", expand=False))
    except requests.exceptions.HTTPError as err:
        if err.response.status_code in [401, 403]: console.print("[bold red]Error: Invalid API key. Check your config.ini.[/bold red]")
        elif err.response.status_code == 400: console.print(f"[bold red]City '{city}' not found or invalid request.[/bold red]")
        else: console.print(f"[bold red]HTTP Error: {err}[/bold red]")
    except requests.exceptions.RequestException as e: console.print(f"[bold red]Connection error: {e}[/bold red]")

def get_news():
    api_keys = load_api_keys(); api_key = api_keys.get('gnews_api_key')
    if not api_key or "YOUR_KEY" in api_key: console.print("[bold yellow]GNews API key not configured in config.ini.[/bold yellow]"); return
    categories = {"1": ("General", "general"), "2": ("World", "world"), "3": ("Nation", "nation"), "4": ("Business", "business"), "5": ("Technology", "technology"), "6": ("Entertainment", "entertainment"), "7": ("Sports", "sports"), "8": ("Science", "science"), "9": ("Health", "health")}
    console.print("\n[bold]Choose a news category:[/bold]")
    for key, (label, _) in categories.items(): console.print(f"  [cyan]{key}[/cyan] - {label}")
    cat_choice = Prompt.ask("[bold]Your choice[/bold]", choices=categories.keys(), default="1"); topic = categories[cat_choice][1]
    keyword = Prompt.ask("\n[bold cyan]Enter a keyword (e.g., Tesla, ecology) or leave empty[/bold cyan]", default="").strip()
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=us&topic={topic}&token={api_key}" # Changed country to 'us'
    if keyword: url += f"&q={keyword}"
    try:
        with console.status("[bold green]Fetching news...[/bold green]"):
            response = requests.get(url); response.raise_for_status(); data = response.json()
        if not data.get("articles"): console.print("[yellow]No articles found for these criteria.[/yellow]"); return
        table = Table(title=f"📰 News for '{categories[cat_choice][0]}' with keyword '{keyword}'", style="yellow")
        table.add_column("#", style="bold cyan"); table.add_column("Title", style="white", no_wrap=False); table.add_column("Source", style="green")
        for i, article in enumerate(data["articles"][:10]): table.add_row(str(i + 1), article['title'], article['source']['name'])
        console.print(table)
    except requests.exceptions.HTTPError as err:
        if err.response.status_code in [401, 403]: console.print("[bold red]Error: Invalid GNews API key.[/bold red]")
        else: console.print(f"[bold red]HTTP Error: {err}[/bold red]")
    except requests.exceptions.RequestException as e: console.print(f"[bold red]Connection error: {e}[/bold red]")

def shorten_url():
    long_url = Prompt.ask("[cyan]Enter the URL to shorten[/cyan]")
    if not long_url.startswith(('http://', 'https://')): console.print("[red]Invalid URL. Must start with http:// or https://[/red]"); return
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}"); response.raise_for_status()
        console.print(f"🔗 Shortened URL: [bold green]{response.text}[/bold green]")
    except requests.exceptions.RequestException as e: console.print(f"[red]Could not shorten URL: {e}[/red]")

def get_wiki_summary():
    topic = Prompt.ask("[cyan]What topic are you looking for on Wikipedia?[/cyan]")
    with console.status(f"[bold green]Searching for '{topic}'...[/bold green]"): page = wiki_wiki.page(topic)
    if not page.exists(): console.print(f"[red]Sorry, no page found for '{topic}'.[/red]"); return
    panel_content = f"[bold]{page.title}[/bold]\n\n{page.summary[0:500]}..."
    console.print(Panel(panel_content, title="📖 Wikipedia Summary", border_style="yellow", subtitle=f"[link={page.fullurl}]Read more[/link]"))

def get_definition():
    word = Prompt.ask("[bold cyan]Which word would you like to define?[/bold cyan]")
    try:
        with console.status(f"[yellow]Looking up '{word}'...[/yellow]"):
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"); response.raise_for_status(); data = response.json()[0]
        definitions_content = []
        for meaning in data['meanings']:
            definitions_content.append(f"\n[bold yellow]({meaning['partOfSpeech']})[/bold yellow]")
            for i, definition in enumerate(meaning['definitions'][:3]):
                definitions_content.append(f"[bold green]{i+1}.[/bold green] {definition['definition']}")
                if 'example' in definition: definitions_content.append(f"   [italic red]Example: {definition['example']}[/italic red]")
        console.print(Panel("\n".join(definitions_content), title=f"[bold magenta]Definitions for '{word}'[/bold magenta]", border_style="magenta"))
    except requests.exceptions.HTTPError: console.print(f"[red]No definition found for the word '{word}'.[/red]")
    except requests.exceptions.RequestException as e: console.print(f"[red]Connection error: {e}[/red]")
    except Exception as e: console.print(f"[red]An unexpected error occurred: {e}[/red]")

def generate_qrcode():
    data = Prompt.ask("[cyan]Enter text or URL for the QR Code[/cyan]")
    filename = Prompt.ask("[cyan]Output filename (e.g., website)[/cyan]", default="qrcode")
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data); qr.make(fit=True); img = qr.make_image(fill_color="black", back_color="white")
    filepath = f"{filename}.png"; img.save(filepath)
    console.print(f"[bold green]✅ QR Code successfully saved as '{filepath}'![/bold green]")

def generate_ascii_art():
    text = Prompt.ask("[cyan]Enter text to convert[/cyan]")
    font = Prompt.ask("[cyan]Choose a font (e.g., standard, big, slant, small)[/cyan]", default="standard")
    try:
        ascii_art = pyfiglet.figlet_format(text, font=font)
        console.print(f"[bold magenta]{ascii_art}[/bold magenta]")
    except pyfiglet.FontNotFound: console.print(f"[red]Font '{font}' not found. Please try another one.[/red]")

def start_timer():
    try:
        seconds = int(Prompt.ask("[cyan]Enter duration in seconds for the timer[/cyan]"))
        with Live(console=console, screen=False, auto_refresh=False) as live:
            for s in range(seconds, -1, -1):
                remaining_time = Text(f"⏳ Time remaining: {s} second{'s' if s != 1 else ''}", justify="center", style="bold green")
                live.update(Panel(remaining_time, title="Timer"), refresh=True); time.sleep(1)
        console.print("[bold yellow]⏰ Time is up![/bold yellow]")
    except ValueError: console.print("[red]Please enter a valid integer for seconds.[/red]")

def show_system_info():
    cpu = psutil.cpu_percent(interval=1); ram = psutil.virtual_memory().percent
    console.print(f"🖥️ [bold cyan]CPU[/bold cyan] Usage: {cpu}% | [bold magenta]RAM[/bold magenta] Usage: {ram}%")

def show_my_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        console.print(f"🌍 Your public IP is: [bold green]{ip}[/bold green]")
    except requests.exceptions.RequestException: console.print("[bold red]Could not retrieve IP address.[/bold red]")

def generate_password():
    try:
        length = int(Prompt.ask("[bold cyan]Password length[/bold cyan]", default="16"))
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        console.print(f"🔐 Generated password: [bold green]{password}[/bold green]")
    except ValueError: console.print("[red]Please enter a valid number.[/red]")

def process_command(command_line: str, commands: dict, aliases: dict):
    if not command_line: return True
    parts = command_line.lower().strip().split(); command_base = parts[0]; args = parts[1:]
    resolved_command = aliases.get(command_base, command_base)
    if resolved_command in ["q", "quit", "exit"]:
        console.print("[bold blue]Goodbye! - DAHORD[/bold blue]"); time.sleep(1); return False
    elif resolved_command in commands:
        try:
            if resolved_command == "todo" or resolved_command == "lang": commands[resolved_command](args)
            else: commands[resolved_command]()
        except Exception as e: console.print(f"[bold red]An error occurred in command '{resolved_command}': {e}[/bold red]")
    else: console.print("[bold red]Command not recognized. Type 'help' for assistance.[/bold red]")
    return True

def handle_lang_command(args):
    """Handles language switching."""
    if not args or args[0] not in ['fr', 'en']:
        console.print("[yellow]Usage: lang <fr|en>[/yellow]")
        return

    new_lang = args[0].lower()
    
    try:
        app_data_root = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
        app_folder = os.path.join(app_data_root, "AI Daily Assist")
        settings_file = os.path.join(app_folder, "settings.json")
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump({'language': new_lang}, f, indent=4)
        
        if new_lang == 'en':
            console.print("[cyan]Language is already set to English.[/cyan]")
        else:
            console.print(f"[bold green]Language changed to '{new_lang}'. Please restart the application.[/bold green]")
            
    except Exception as e:
        console.print(f"[red]Error changing language: {e}[/red]")

def main():
    console.print(Panel("[bold green]🚀 Terminal Assistant v2.9 - Productivity Mode 🚀 - By DAHORD[/bold green]", border_style="green"))
    console.print("Type '[cyan]help[/cyan]' to see the list of commands.")
    commands = {
        "todo": manage_todo, "convert": convert_currency, "search": search_in_files, "tree": show_tree,
        "disk": show_disk_usage, "org": organize_files, "sys": show_system_info, "weather": get_weather,
        "news": get_news, "ip": show_my_ip, "shorten": shorten_url, "wiki": get_wiki_summary,
        "def": get_definition, "qrcode": generate_qrcode, "ascii": generate_ascii_art,
        "pass": generate_password, "timer": start_timer, "lang": handle_lang_command, "help": show_help,
    }
    aliases = {"q": "q", "quit": "q", "exit": "q", "url": "shorten", "blg": "joke", "mdp": "pass"}
    running = True
    while running:
        try:
            user_input = Prompt.ask(">>>")
            running = process_command(user_input, commands, aliases)
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold cyan]Forced shutdown...[/bold cyan]"); running = False
if __name__ == "__main__":
    main()
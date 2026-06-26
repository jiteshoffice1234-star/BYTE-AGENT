"""Code Templates - BYTE's knowledge of how to write code."""


class CodeTemplates:
    """Pre-built code templates for common requests."""

    @staticmethod
    def generate(language: str, task: str) -> str:
        """Generate code based on language and task."""
        templates = {
            ("python", "hello"): CodeTemplates._py_hello,
            ("python", "calculator"): CodeTemplates._py_calculator,
            ("python", "todo"): CodeTemplates._py_todo,
            ("python", "api"): CodeTemplates._py_api,
            ("python", "web app"): CodeTemplates._py_flask_app,
            ("python", "scraper"): CodeTemplates._py_scraper,
            ("python", "game"): CodeTemplates._py_game,
            ("python", "password"): CodeTemplates._py_password,
            ("python", "file organizer"): CodeTemplates._py_file_organizer,
            ("python", "weather"): CodeTemplates._py_weather,

            ("javascript", "hello"): CodeTemplates._js_hello,
            ("javascript", "todo"): CodeTemplates._js_todo,
            ("javascript", "game"): CodeTemplates._js_game,
            ("javascript", "api"): CodeTemplates._js_api,

            ("html", "website"): CodeTemplates._html_website,
            ("html", "login"): CodeTemplates._html_login,
            ("html", "dashboard"): CodeTemplates._html_dashboard,
            ("html", "portfolio"): CodeTemplates._html_portfolio,
            ("html", "landing"): CodeTemplates._html_landing,

            ("react", "app"): CodeTemplates._react_app,
            ("react", "component"): CodeTemplates._react_component,

            ("sql", "database"): CodeTemplates._sql_database,
            ("sql", "query"): CodeTemplates._sql_query,

            ("docker", "file"): CodeTemplates._dockerfile,
            ("docker", "compose"): CodeTemplates._docker_compose,
        }
        key = (language.lower(), task.lower())
        for (lang, tsk), func in templates.items():
            if lang in language.lower() and tsk in task.lower():
                return func()
        return f"# I can create a {language} {task} for you.\n# Tell me more details and I'll write the full code."

    @staticmethod
    def list_known() -> list:
        return [
            "python: hello, calculator, todo, api, web app, scraper, game, password generator, file organizer, weather",
            "javascript: hello, todo, game, api",
            "html: website, login, dashboard, portfolio, landing page",
            "react: app, component",
            "sql: database, query",
            "docker: dockerfile, compose"
        ]

    @staticmethod
    def _py_hello():
        return '''def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}! Welcome to Python 3."


if __name__ == "__main__":
    user = input("Enter your name: ")
    print(greet(user))'''

    @staticmethod
    def _py_calculator():
        return '''class Calculator:
    """A simple calculator class."""

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def power(a: float, b: float) -> float:
        return a ** b

    @staticmethod
    def sqrt(a: float) -> float:
        if a < 0:
            raise ValueError("Cannot sqrt negative number")
        return a ** 0.5


def main():
    calc = Calculator()
    print("=== BYTE Calculator ===")
    print("Operations: +, -, *, /, ^, sqrt")
    while True:
        try:
            expr = input("\\nEnter expression (or 'q'): ").strip()
            if expr.lower() == 'q':
                break
            if expr.startswith("sqrt"):
                n = float(expr[4:].strip())
                print(f"Result: {calc.sqrt(n)}")
            elif "+" in expr:
                a, b = map(float, expr.split("+"))
                print(f"Result: {calc.add(a, b)}")
            elif "-" in expr:
                a, b = map(float, expr.split("-"))
                print(f"Result: {calc.subtract(a, b)}")
            elif "*" in expr:
                a, b = map(float, expr.split("*"))
                print(f"Result: {calc.multiply(a, b)}")
            elif "/" in expr:
                a, b = map(float, expr.split("/"))
                print(f"Result: {calc.divide(a, b)}")
            elif "^" in expr:
                a, b = map(float, expr.split("^"))
                print(f"Result: {calc.power(a, b)}")
            else:
                print("Unknown expression")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _py_todo():
        return '''"""Todo App - Command line todo list."""

import json
import os
from datetime import datetime


class TodoApp:
    def __init__(self, filename: str = "todos.json"):
        self.filename = filename
        self.todos = self._load()

    def _load(self) -> list:
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump(self.todos, f, indent=2)

    def add(self, title: str, priority: str = "medium"):
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "priority": priority,
            "done": False,
            "created": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self._save()
        print(f"Added: {title}")

    def list(self):
        if not self.todos:
            print("No todos yet!")
            return
        print(f"\\n{'ID':<4} {'Done':<6} {'Priority':<10} Title")
        print("-" * 50)
        for t in self.todos:
            done = "[x]" if t["done"] else " "
            print(f"{t['id']:<4} [{done}]    {t['priority']:<10} {t['title']}")

    def done(self, todo_id: int):
        for t in self.todos:
            if t["id"] == todo_id:
                t["done"] = True
                self._save()
                print(f"Done: {t['title']}")
                return
        print(f"Todo #{todo_id} not found")

    def delete(self, todo_id: int):
        self.todos = [t for t in self.todos if t["id"] != todo_id]
        self._save()
        print(f"Deleted todo #{todo_id}")


def main():
    app = TodoApp()
    print("=== BYTE Todo App ===")
    while True:
        cmd = input("\\ntodo> ").strip().lower()
        if cmd in ("q", "quit"):
            break
        elif cmd in ("l", "list"):
            app.list()
        elif cmd.startswith("add "):
            app.add(cmd[4:])
        elif cmd.startswith("done "):
            try:
                app.done(int(cmd[5:]))
            except:
                print("Usage: done <id>")
        elif cmd.startswith("del "):
            try:
                app.delete(int(cmd[4:]))
            except:
                print("Usage: del <id>")
        else:
            print("Commands: list, add <text>, done <id>, del <id>, quit")


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _py_api():
        return '''"""FastAPI REST API template."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="BYTE API", version="1.0.0")


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float


items_db: List[Item] = []
counter = 1


@app.get("/")
def root():
    return {"message": "BYTE API is running", "version": "1.0.0"}


@app.get("/items", response_model=List[Item])
def get_items():
    return items_db


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(404, "Item not found")


@app.post("/items", response_model=Item)
def create_item(item: Item):
    global counter
    item.id = counter
    counter += 1
    items_db.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for i, existing in enumerate(items_db):
        if existing.id == item_id:
            item.id = item_id
            items_db[i] = item
            return item
    raise HTTPException(404, "Item not found")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return {"message": "Deleted"}
    raise HTTPException(404, "Item not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)'''

    @staticmethod
    def _py_flask_app():
        return '''"""Flask Web App template."""

from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "app.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "<h1>BYTE Flask App</h1><p>Server is running!</p>"


@app.route("/api/items")
def get_items():
    conn = sqlite3.connect(DB_FILE)
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return jsonify([{"id": i[0], "title": i[1]} for i in items])


@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title required"}), 400
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO items (title) VALUES (?)", (data["title"],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Created"}), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)'''

    @staticmethod
    def _py_scraper():
        return '''"""Web scraper template."""

import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Dict


class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "BYTE-Scraper/1.0"
        })

    def fetch(self, url: str) -> str:
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def parse_links(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            links.append({
                "text": a.get_text(strip=True),
                "href": a["href"]
            })
        return links

    def save_csv(self, data: List[Dict], filename: str):
        if not data:
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved {len(data)} items to {filename}")


def main():
    url = input("URL to scrape: ").strip()
    scraper = WebScraper(url)
    try:
        html = scraper.fetch(url)
        links = scraper.parse_links(html)
        print(f"Found {len(links)} links")
        scraper.save_csv(links, "scraped_data.csv")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _py_game():
        return '''"""Simple Snake game using Pygame."""

import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 400
CELL = 20


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BYTE Snake")
    clock = pygame.time.Clock()

    snake = [(100, 100)]
    direction = (CELL, 0)
    food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if head == food:
            snake.insert(0, head)
            food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            score += 1
        else:
            snake.insert(0, head)
            snake.pop()

        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            len(snake) != len(set(snake))):
            running = False

        screen.fill((0, 0, 0))
        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL, CELL))
        pygame.draw.rect(screen, (255, 0, 0), (*food, CELL, CELL))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(10)

    print(f"Game Over! Score: {score}")
    pygame.quit()


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _py_password():
        return '''"""Password Generator."""

import random
import string


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True
) -> str:
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not chars:
        raise ValueError("At least one character type required")

    return "".join(random.choice(chars) for _ in range(length))


def check_strength(password: str) -> str:
    score = 0
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 3:
        return "Medium"
    elif score <= 4:
        return "Strong"
    return "Very Strong"


def main():
    print("=== BYTE Password Generator ===")
    length = int(input("Length (default 16): ") or "16")
    pw = generate_password(length)
    strength = check_strength(pw)
    print(f"\\nPassword: {pw}")
    print(f"Strength: {strength}")


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _py_file_organizer():
        return '''"""File Organizer - Organizes files by type."""

import os
import shutil
from pathlib import Path


FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".csv", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".go", ".rs"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Executables": [".exe", ".msi", ".deb", ".rpm", ".app"],
}


def organize(directory: str = ".", dry_run: bool = False) -> None:
    path = Path(directory)
    if not path.exists():
        print(f"Directory not found: {directory}")
        return

    for item in path.iterdir():
        if item.is_file():
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if item.suffix.lower() in extensions:
                    dest = path / category
                    if not dry_run:
                        dest.mkdir(exist_ok=True)
                        shutil.move(str(item), str(dest / item.name))
                    print(f"{'[DRY]' if dry_run else ''} Moving: {item.name} -> {category}/")
                    moved = True
                    break
            if not moved:
                other = path / "Other"
                if not dry_run:
                    other.mkdir(exist_ok=True)
                    shutil.move(str(item), str(other / item.name))
                print(f"{'[DRY]' if dry_run else ''} Moving: {item.name} -> Other/")


def main():
    directory = input("Directory to organize (default .): ").strip() or "."
    dry = input("Dry run? (y/n): ").strip().lower() == "y"
    organize(directory, dry)
    print("\\nDone!")


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _py_weather():
        return '''"""Weather App - Fetches weather data."""

import requests
import json


def get_weather(city: str, api_key: str = "") -> dict:
    """Fetch weather data for a city."""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        return {
            "city": city,
            "temp": current["temp_C"],
            "feels_like": current["FeelsLikeC"],
            "humidity": current["humidity"],
            "description": current["weatherDesc"][0]["value"],
            "wind": current["windspeedKmph"],
        }
    except Exception as e:
        return {"error": str(e)}


def display(weather: dict):
    if "error" in weather:
        print(f"Error: {weather['error']}")
        return
    print(f"\\n=== Weather in {weather['city']} ===")
    print(f"Temperature: {weather['temp']}C")
    print(f"Feels like: {weather['feels_like']}C")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Conditions: {weather['description']}")
    print(f"Wind: {weather['wind']} km/h")


def main():
    city = input("Enter city name: ").strip()
    if city:
        weather = get_weather(city)
        display(weather)


if __name__ == "__main__":
    main()'''

    @staticmethod
    def _js_hello():
        return '''// Hello World in JavaScript
function greet(name) {
    return `Hello, ${name}! Welcome to JavaScript.`;
}

console.log(greet("BYTE User"));

// Run with: node hello.js'''

    @staticmethod
    def _js_todo():
        return '''// Todo App in JavaScript

class TodoApp {
    constructor() {
        this.todos = [];
        this.counter = 1;
    }

    add(title, priority = "medium") {
        this.todos.push({
            id: this.counter++,
            title,
            priority,
            done: false,
            createdAt: new Date().toISOString()
        });
        console.log(`Added: ${title}`);
    }

    list() {
        if (this.todos.length === 0) {
            console.log("No todos yet!");
            return;
        }
        console.log("\\nID  Done  Priority   Title");
        console.log("-".repeat(40));
        this.todos.forEach(t => {
            const done = t.done ? "[x]" : " ";
            console.log(`${t.id.toString().padEnd(3)} [${done}]   ${t.priority.padEnd(10)} ${t.title}`);
        });
    }

    done(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.done = true;
            console.log(`Done: ${todo.title}`);
        }
    }

    delete(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        console.log(`Deleted #${id}`);
    }
}

// Example usage
const app = new TodoApp();
app.add("Learn JavaScript", "high");
app.add("Build a project", "medium");
app.list();

// Run with: node todo.js'''

    @staticmethod
    def _js_game():
        return '''// Number Guessing Game in JavaScript

function guessingGame() {
    const secret = Math.floor(Math.random() * 100) + 1;
    let attempts = 0;
    const maxAttempts = 7;

    console.log("\\n=== BYTE Number Guessing Game ===");
    console.log("I'm thinking of a number between 1 and 100.");
    console.log(`You have ${maxAttempts} attempts.\\n`);

    const readline = require("readline");
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    function ask() {
        if (attempts >= maxAttempts) {
            console.log(`\\nGame Over! The number was ${secret}.`);
            rl.close();
            return;
        }

        rl.question(`Guess (${attempts + 1}/${maxAttempts}): `, (input) => {
            const guess = parseInt(input);
            attempts++;

            if (isNaN(guess)) {
                console.log("Please enter a number!");
            } else if (guess < secret) {
                console.log("Too low!");
            } else if (guess > secret) {
                console.log("Too high!");
            } else {
                console.log(`\\nCorrect! You got it in ${attempts} attempts!`);
                rl.close();
                return;
            }
            ask();
        });
    }
    ask();
}

guessingGame();

// Run with: node game.js'''

    @staticmethod
    def _js_api():
        return '''// Express.js REST API

const express = require("express");
const app = express();
app.use(express.json());

let items = [];
let counter = 1;

app.get("/", (req, res) => {
    res.json({ message: "BYTE API is running", version: "1.0.0" });
});

app.get("/items", (req, res) => {
    res.json(items);
});

app.get("/items/:id", (req, res) => {
    const item = items.find(i => i.id === parseInt(req.params.id));
    if (!item) return res.status(404).json({ error: "Not found" });
    res.json(item);
});

app.post("/items", (req, res) => {
    const item = { id: counter++, ...req.body };
    items.push(item);
    res.status(201).json(item);
});

app.put("/items/:id", (req, res) => {
    const idx = items.findIndex(i => i.id === parseInt(req.params.id));
    if (idx === -1) return res.status(404).json({ error: "Not found" });
    items[idx] = { ...items[idx], ...req.body };
    res.json(items[idx]);
});

app.delete("/items/:id", (req, res) => {
    items = items.filter(i => i.id !== parseInt(req.params.id));
    res.json({ message: "Deleted" });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`BYTE API running on http://localhost:${PORT}`);
});

// Run with: node api.js'''

    @staticmethod
    def _html_website():
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BYTE Website</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 0; text-align: center; }
        header h1 { font-size: 3em; margin-bottom: 10px; }
        header p { font-size: 1.2em; opacity: 0.9; }
        nav { background: #333; padding: 15px 0; }
        nav a { color: white; text-decoration: none; margin: 0 15px; }
        nav a:hover { color: #667eea; }
        .section { padding: 60px 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        .card { background: #f5f5f5; padding: 30px; border-radius: 10px; }
        .card h3 { margin-bottom: 15px; color: #667eea; }
        footer { background: #333; color: white; text-align: center; padding: 20px 0; }
        @media (max-width: 768px) {
            header h1 { font-size: 2em; }
            nav a { display: block; margin: 10px 0; }
        }
    </style>
</head>
<body>
    <header>
        <h1>Welcome to BYTE</h1>
        <p>Built with precision by BYTE AGENT</p>
    </header>
    <nav>
        <div class="container">
            <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#services">Services</a>
            <a href="#contact">Contact</a>
        </div>
    </nav>
    <section class="section" id="about">
        <div class="container">
            <h2>About Us</h2>
            <p>We build amazing software solutions using cutting-edge technology.</p>
        </div>
    </section>
    <section class="section" id="services">
        <div class="container">
            <h2>Our Services</h2>
            <div class="grid">
                <div class="card">
                    <h3>Web Development</h3>
                    <p>Modern, responsive websites and web applications.</p>
                </div>
                <div class="card">
                    <h3>API Design</h3>
                    <p>RESTful and GraphQL APIs built to scale.</p>
                </div>
                <div class="card">
                    <h3>Cloud Solutions</h3>
                    <p>Deploy and manage infrastructure with ease.</p>
                </div>
            </div>
        </div>
    </section>
    <footer>
        <p>&copy; 2026 BYTE. Built by BYTE AGENT.</p>
    </footer>
</body>
</html>'''

    @staticmethod
    def _html_login():
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - BYTE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        .login-box h2 {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #666;
            font-weight: 500;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
            margin: 0 10px;
        }
        .links a:hover { text-decoration: underline; }
        .error { color: #e74c3c; margin-bottom: 15px; text-align: center; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" placeholder="Enter your email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn">Sign In</button>
        </form>
        <div class="links">
            <a href="#">Forgot Password?</a>
            <a href="#">Create Account</a>
        </div>
    </div>
    <script>
        document.getElementById("loginForm").addEventListener("submit", function(e) {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            console.log("Login attempt:", { email, password });
            alert("Login demo - check console");
        });
    </script>
</body>
</html>'''

    @staticmethod
    def _html_dashboard():
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - BYTE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; }
        .sidebar {
            position: fixed; left: 0; top: 0; bottom: 0; width: 250px;
            background: #1a1a2e; color: white; padding: 20px;
        }
        .sidebar h2 { margin-bottom: 30px; font-size: 1.5em; }
        .sidebar a {
            display: block; color: #a0a0b0; text-decoration: none;
            padding: 12px; margin: 5px 0; border-radius: 8px;
            transition: all 0.3s;
        }
        .sidebar a:hover, .sidebar a.active { background: #16213e; color: white; }
        .main { margin-left: 250px; padding: 30px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .header h1 { color: #333; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-card h3 { color: #666; font-size: 0.9em; margin-bottom: 10px; }
        .stat-card .value { font-size: 2em; font-weight: bold; color: #333; }
        .stat-card .change { font-size: 0.9em; margin-top: 5px; }
        .up { color: #27ae60; } .down { color: #e74c3c; }
        table { width: 100%; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; color: #666; font-weight: 600; }
        .badge { padding: 5px 10px; border-radius: 20px; font-size: 0.8em; }
        .badge.success { background: #d4edda; color: #155724; }
        .badge.warning { background: #fff3cd; color: #856404; }
        .badge.danger { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>BYTE Dashboard</h2>
        <a href="#" class="active">Overview</a>
        <a href="#">Analytics</a>
        <a href="#">Users</a>
        <a href="#">Settings</a>
        <a href="#">Help</a>
    </div>
    <div class="main">
        <div class="header">
            <h1>Dashboard Overview</h1>
            <span>Welcome back, BYTE User</span>
        </div>
        <div class="stats">
            <div class="stat-card">
                <h3>Total Users</h3>
                <div class="value">2,847</div>
                <div class="change up">+12.5%</div>
            </div>
            <div class="stat-card">
                <h3>Revenue</h3>
                <div class="value">$48,290</div>
                <div class="change up">+8.2%</div>
            </div>
            <div class="stat-card">
                <h3>Active Now</h3>
                <div class="value">142</div>
                <div class="change down">-3.1%</div>
            </div>
            <div class="stat-card">
                <h3>Tasks</h3>
                <div class="value">24</div>
                <div class="change up">+5</div>
            </div>
        </div>
        <table>
            <thead>
                <tr><th>Name</th><th>Email</th><th>Status</th><th>Role</th></tr>
            </thead>
            <tbody>
                <tr><td>John Doe</td><td>john@example.com</td><td><span class="badge success">Active</span></td><td>Admin</td></tr>
                <tr><td>Jane Smith</td><td>jane@example.com</td><td><span class="badge success">Active</span></td><td>Editor</td></tr>
                <tr><td>Bob Wilson</td><td>bob@example.com</td><td><span class="badge warning">Pending</span></td><td>Viewer</td></tr>
            </tbody>
        </table>
    </div>
</body>
</html>'''

    @staticmethod
    def _html_portfolio():
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio - BYTE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #333; }
        .hero {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white; text-align: center; padding: 100px 20px;
        }
        .hero h1 { font-size: 3.5em; margin-bottom: 10px; }
        .hero p { font-size: 1.3em; opacity: 0.9; margin-bottom: 30px; }
        .hero .btn {
            display: inline-block; padding: 15px 30px; background: #e94560;
            color: white; text-decoration: none; border-radius: 5px; font-weight: bold;
        }
        .section { padding: 80px 20px; max-width: 1200px; margin: 0 auto; }
        .section h2 { text-align: center; font-size: 2.5em; margin-bottom: 50px; }
        .projects { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        .project-card {
            background: #f5f5f5; border-radius: 10px; overflow: hidden;
            transition: transform 0.3s;
        }
        .project-card:hover { transform: translateY(-5px); }
        .project-card .content { padding: 20px; }
        .project-card h3 { margin-bottom: 10px; }
        .project-card .tags { margin: 10px 0; }
        .project-card .tag {
            display: inline-block; padding: 5px 10px; background: #e94560;
            color: white; border-radius: 3px; font-size: 0.8em; margin: 2px;
        }
        .skills { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; }
        .skill {
            padding: 15px 25px; background: #f5f5f5; border-radius: 10px;
            font-weight: bold; transition: all 0.3s;
        }
        .skill:hover { background: #e94560; color: white; }
        footer { text-align: center; padding: 30px; background: #1a1a2e; color: white; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>BYTE Developer</h1>
        <p>Full-Stack Developer & AI Enthusiast</p>
        <a href="#projects" class="btn">View My Work</a>
    </div>
    <div class="section" id="about">
        <h2>About Me</h2>
        <p style="text-align:center;max-width:600px;margin:0 auto;font-size:1.2em;line-height:1.8;">
            I build modern web applications with cutting-edge technology.
            Passionate about AI, clean code, and great user experiences.
        </p>
    </div>
    <div class="section" id="projects">
        <h2>Projects</h2>
        <div class="projects">
            <div class="project-card">
                <div class="content">
                    <h3>BYTE Agent</h3>
                    <p>An AI coding agent that runs locally on your machine.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">AI</span></div>
                </div>
            </div>
            <div class="project-card">
                <div class="content">
                    <h3>Cloud Platform</h3>
                    <p>A scalable cloud infrastructure management platform.</p>
                    <div class="tags"><span class="tag">React</span><span class="tag">Go</span></div>
                </div>
            </div>
            <div class="project-card">
                <div class="content">
                    <h3>Analytics Dashboard</h3>
                    <p>Real-time data visualization and analytics dashboard.</p>
                    <div class="tags"><span class="tag">Vue.js</span><span class="tag">D3.js</span></div>
                </div>
            </div>
        </div>
    </div>
    <footer>&copy; 2026 BYTE. Built by BYTE AGENT.</footer>
</body>
</html>'''

    @staticmethod
    def _html_landing():
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page - BYTE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .hero {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            color: white; text-align: center; padding: 20px;
        }
        .hero h1 { font-size: 4em; margin-bottom: 20px; }
        .hero p { font-size: 1.3em; max-width: 600px; margin-bottom: 40px; opacity: 0.9; }
        .cta-btn {
            display: inline-block; padding: 18px 40px; background: white;
            color: #667eea; text-decoration: none; border-radius: 50px;
            font-weight: bold; font-size: 1.1em;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .cta-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .features {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px; max-width: 1200px; margin: 80px auto; padding: 0 20px;
        }
        .feature {
            text-align: center; padding: 40px 20px;
        }
        .feature .icon { font-size: 3em; margin-bottom: 20px; }
        .feature h3 { margin-bottom: 15px; color: #333; }
        .feature p { color: #666; line-height: 1.6; }
        footer { text-align: center; padding: 30px; color: #666; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Build Faster</h1>
        <p>Create amazing products with BYTE - your AI-powered development partner</p>
        <a href="#" class="cta-btn">Get Started Free</a>
    </div>
    <div class="features">
        <div class="feature">
            <div class="icon">[BOLT]</div>
            <h3>Lightning Fast</h3>
            <p>Build and deploy in minutes, not days. Accelerate your development.</p>
        </div>
        <div class="feature">
            <div class="icon">[LOCK]</div>
            <h3>Secure</h3>
            <p>Enterprise-grade security built in. Your code stays safe.</p>
        </div>
        <div class="feature">
            <div class="icon">[TARGET]</div>
            <h3>Precise</h3>
            <p>AI-powered suggestions that understand your codebase.</p>
        </div>
    </div>
    <footer>Built with BYTE AGENT &copy; 2026</footer>
</body>
</html>'''

    @staticmethod
    def _react_app():
        return '''import React, { useState, useEffect } from "react";

function App() {
    const [items, setItems] = useState([]);
    const [input, setInput] = useState("");

    useEffect(() => {
        const saved = localStorage.getItem("byte-items");
        if (saved) setItems(JSON.parse(saved));
    }, []);

    useEffect(() => {
        localStorage.setItem("byte-items", JSON.stringify(items));
    }, [items]);

    const addItem = () => {
        if (input.trim()) {
            setItems([...items, { id: Date.now(), text: input.trim(), done: false }]);
            setInput("");
        }
    };

    const toggleItem = (id) => {
        setItems(items.map(i => i.id === id ? { ...i, done: !i.done } : i));
    };

    const deleteItem = (id) => {
        setItems(items.filter(i => i.id !== id));
    };

    return (
        <div style={{ maxWidth: 500, margin: "50px auto", fontFamily: "sans-serif" }}>
            <h1>BYTE Todo App</h1>
            <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && addItem()}
                    placeholder="Add a todo..."
                    style={{ flex: 1, padding: 10, fontSize: 16, border: "2px solid #ddd", borderRadius: 5 }}
                />
                <button onClick={addItem} style={{ padding: "10px 20px", background: "#667eea", color: "white", border: "none", borderRadius: 5, cursor: "pointer" }}>
                    Add
                </button>
            </div>
            <ul style={{ listStyle: "none", padding: 0 }}>
                {items.map(item => (
                    <li key={item.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: 10, borderBottom: "1px solid #eee" }}>
                        <input type="checkbox" checked={item.done} onChange={() => toggleItem(item.id)} />
                        <span style={{ flex: 1, textDecoration: item.done ? "line-through" : "none", color: item.done ? "#999" : "#333" }}>
                            {item.text}
                        </span>
                        <button onClick={() => deleteItem(item.id)} style={{ background: "#e74c3c", color: "white", border: "none", borderRadius: 3, padding: "5px 10px", cursor: "pointer" }}>
                            Delete
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;'''

    @staticmethod
    def _react_component():
        return '''import React from "react";

function Card({ title, children, style = {} }) {
    return (
        <div style={{
            background: "white",
            borderRadius: 10,
            padding: 20,
            boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
            ...style
        }}>
            {title && <h3 style={{ marginBottom: 15, color: "#333" }}>{title}</h3>}
            {children}
        </div>
    );
}

function Button({ children, onClick, variant = "primary", ...props }) {
    const styles = {
        primary: { background: "#667eea", color: "white" },
        danger: { background: "#e74c3c", color: "white" },
        ghost: { background: "transparent", color: "#667eea", border: "2px solid #667eea" }
    };
    return (
        <button
            onClick={onClick}
            style={{
                padding: "10px 20px",
                border: "none",
                borderRadius: 5,
                cursor: "pointer",
                fontWeight: "bold",
                fontSize: 14,
                transition: "transform 0.2s",
                ...styles[variant] || styles.primary,
                ...props.style
            }}
            {...props}
        >
            {children}
        </button>
    );
}

function Modal({ show, onClose, title, children }) {
    if (!show) return null;
    return (
        <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
            background: "rgba(0,0,0,0.5)",
            display: "flex", alignItems: "center", justifyContent: "center",
            zIndex: 1000
        }} onClick={onClose}>
            <div style={{
                background: "white", borderRadius: 10, padding: 30,
                maxWidth: 500, width: "90%"
            }} onClick={(e) => e.stopPropagation()}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
                    <h2>{title}</h2>
                    <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 24, cursor: "pointer" }}>&times;</button>
                </div>
                {children}
            </div>
        </div>
    );
}

export { Card, Button, Modal };'''

    @staticmethod
    def _sql_database():
        return '''-- Database Schema Template

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS post_tags (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_post_tags_tag_id ON post_tags(tag_id);'''

    @staticmethod
    def _sql_query():
        return '''-- SQL Query Examples

-- Basic queries
SELECT * FROM users;
SELECT id, username, email FROM users WHERE role = 'admin';
SELECT COUNT(*) FROM users;

-- Joins
SELECT p.title, u.username, p.created_at
FROM posts p
JOIN users u ON p.user_id = u.id
ORDER BY p.created_at DESC
LIMIT 10;

-- Aggregation
SELECT u.username, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id
HAVING post_count > 0
ORDER BY post_count DESC;

-- Subquery
SELECT username, email
FROM users
WHERE id IN (
    SELECT user_id FROM posts GROUP BY user_id HAVING COUNT(*) > 5
);

-- Search
SELECT * FROM posts
WHERE title LIKE '%search%' OR content LIKE '%search%';

-- Pagination
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;

-- Update
UPDATE users SET role = 'editor' WHERE email LIKE '%@example.com';

-- Delete old records
DELETE FROM posts WHERE created_at < date('now', '-1 year') AND status = 'draft';'''

    @staticmethod
    def _dockerfile():
        return '''# Multi-stage Docker build

# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Production
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app .
EXPOSE 8000
CMD ["python", "main.py"]'''

    @staticmethod
    def _docker_compose():
        return '''version: "3.9"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
    volumes:
      - .:/app
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:'''

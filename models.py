"""
models.py - Database Layer
============================
Uses Python's built-in sqlite3 module.
No extra packages needed beyond Flask!

Tables: admins | skills | projects | messages
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "database.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    c    = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now')))""")

    c.execute("""CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        icon TEXT DEFAULT 'fas fa-code',
        category TEXT DEFAULT 'General',
        level INTEGER DEFAULT 80,
        created_at TEXT DEFAULT (datetime('now')))""")

    c.execute("""CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        image TEXT DEFAULT 'images/placeholder.jpg',
        technologies TEXT DEFAULT '',
        github_url TEXT DEFAULT '#',
        live_url TEXT DEFAULT '#',
        category TEXT DEFAULT 'fullstack',
        featured INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')))""")

    c.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')))""")

    conn.commit()
    conn.close()
    print("Tables created/verified")


def seed_db():
    conn = get_db()
    c    = conn.cursor()

    c.execute("SELECT COUNT(*) FROM admins")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
                  ("admin", generate_password_hash("admin123")))
        print("Admin created → username: admin | password: admin123")

    c.execute("SELECT COUNT(*) FROM skills")
    if c.fetchone()[0] == 0:
        skills = [
            ("HTML5","fab fa-html5","Frontend",95),
            ("CSS3","fab fa-css3-alt","Frontend",90),
            ("JavaScript","fab fa-js-square","Frontend",88),
            ("React","fab fa-react","Frontend",82),
            ("Python","fab fa-python","Backend",90),
            ("Flask","fas fa-flask","Backend",85),
            ("C++","fas fa-code","Backend",75),
            ("WordPress","fab fa-wordpress","CMS",80),
            ("Git","fab fa-git-alt","Tools",88),
            ("Docker","fab fa-docker","Tools",70),
            ("MySQL","fas fa-database","Database",82),
            ("SQLite","fas fa-database","Database",85),
        ]
        c.executemany("INSERT INTO skills (name,icon,category,level) VALUES(?,?,?,?)", skills)
        print("Default skills seeded")

    c.execute("SELECT COUNT(*) FROM projects")
    if c.fetchone()[0] == 0:
        projects = [
            ("E-Commerce Platform","A full-featured online store with cart, payments, and admin dashboard.","images/project1.jpg","React, Flask, SQLite, Stripe API","https://github.com/alexdev/ecommerce","https://demo-ecommerce.com","fullstack",1),
            ("Task Management App","A productivity app with drag-and-drop tasks and team collaboration.","images/project2.jpg","JavaScript, Python, WebSockets, SQLite","https://github.com/alexdev/taskapp","https://demo-tasks.com","fullstack",1),
            ("Portfolio Website","A modern developer portfolio with Flask backend and admin panel.","images/project3.jpg","HTML, CSS, JavaScript, Flask, SQLite","https://github.com/alexdev/portfolio","https://alexdev.com","frontend",0),
            ("Blog CMS","Custom CMS for bloggers with markdown support and SEO tools.","images/project4.jpg","Python, Flask, SQLite, Markdown","https://github.com/alexdev/blogcms","https://demo-blog.com","backend",0),
        ]
        c.executemany("INSERT INTO projects (title,description,image,technologies,github_url,live_url,category,featured) VALUES(?,?,?,?,?,?,?,?)", projects)
        print("Default projects seeded")

    conn.commit()
    conn.close()
    print("Database ready!")


def row_to_dict(row):
    return dict(row)

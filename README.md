# 🚀 Full Stack Developer Portfolio

A modern, responsive portfolio website with a Flask backend, SQLite database, and a fully functional admin panel.

---

## 📁 Project Structure

```
portfolio_project/
├── frontend/
│   ├── index.html          ← Main portfolio page
│   ├── css/
│   │   └── style.css       ← All portfolio styles
│   ├── js/
│   │   └── script.js       ← All frontend JavaScript
│   └── images/             ← Project & profile images
│
└── backend/
    ├── app.py              ← Flask app entry point
    ├── models.py           ← SQLite database models
    ├── routes.py           ← API & admin routes
    ├── requirements.txt    ← Python dependencies
    ├── database.db         ← SQLite database (auto-created)
    └── templates/
        ├── admin_login.html
        ├── base_admin.html
        ├── dashboard.html
        ├── add_project.html
        ├── manage_projects.html
        ├── add_skill.html
        └── messages.html
```

---

## ⚡ Quick Start (3 Steps)

### Step 1 — Install dependencies

```bash
cd portfolio_project/backend
pip install -r requirements.txt
```

### Step 2 — Start the server

```bash
python app.py
```

### Step 3 — Open in browser

| Page       | URL                                    |
|------------|----------------------------------------|
| Portfolio  | http://localhost:5000                  |
| Admin Login| http://localhost:5000/admin/login      |

---

## 🔑 Default Admin Credentials

```
Username: admin
Password: admin123
```
> ⚠️ Change these in `app.py` → `seed_database()` before deploying to production!

---

## ✨ Features

### Portfolio (Frontend)
- 🌙 Dark / Light mode toggle (saved to localStorage)
- ⌨️ Typing animation in hero section
- 📱 Fully responsive (mobile + tablet + desktop)
- ✨ Scroll-triggered reveal animations
- 🎛️ Project category filter (All / Frontend / Backend / Full Stack)
- 📬 AJAX contact form
- 🔄 Skills & projects loaded dynamically from the database

### Admin Panel (Backend)
- 🔐 Secure login with password hashing
- 📊 Dashboard with stats (projects, skills, messages)
- ➕ Add / Edit / Delete projects
- ⭐ Add / Delete skills with proficiency levels
- 💬 View, mark-as-read, delete contact messages

---

## 🛠 Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript   |
| Backend  | Python 3, Flask                   |
| Database | SQLite (via Flask-SQLAlchemy)     |
| Admin UI | Jinja2 templates, custom CSS      |
| Icons    | Font Awesome 6                    |
| Fonts    | Cormorant Garamond + DM Sans      |

---

## 📸 Adding Your Own Images

1. Place your photos inside `frontend/images/`
2. Recommended image names:
   - `profile.jpg` — hero section profile photo
   - `about.jpg`   — about section photo
   - `project1.jpg`, `project2.jpg`, etc. — project screenshots

3. Update the image paths in the admin panel when adding projects.

---

## 🚀 Deployment

For production, consider:
- Setting `DEBUG = False` in `app.py`
- Changing `SECRET_KEY` to a random 32-character string
- Using **Gunicorn** instead of Flask's dev server:
  ```bash
  pip install gunicorn
  gunicorn -w 4 app:app
  ```
- Deploying on **Railway**, **Render**, or **DigitalOcean**

---

## 📝 Customization

To make this portfolio your own:

1. **Name & Info** — Edit `frontend/index.html` (search for "Alex Morgan")
2. **Colors** — Edit CSS variables at the top of `frontend/css/style.css`
3. **Projects** — Use the Admin Panel at `/admin/dashboard`
4. **Skills** — Use the Admin Panel → Skills section
5. **Services** — Edit the Services section in `index.html`
6. **Testimonials** — Edit the Testimonials section in `index.html`

---

*Built with ❤️ using Python, Flask, SQLite, and Vanilla JavaScript.*

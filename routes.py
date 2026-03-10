"""
routes.py - All Flask Routes
==============================
api_bp   → Public JSON API  (/api/skills, /api/projects, /api/contact)
admin_bp → Admin HTML pages (/admin/login, /admin/dashboard, ...)
"""

from flask import (
    Blueprint, jsonify, request, session,
    render_template, redirect, url_for, flash
)
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from models import get_db, row_to_dict

api_bp   = Blueprint("api",   __name__)
admin_bp = Blueprint("admin", __name__)


# ── Login Required Decorator ──────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please log in to access the dashboard.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


# ═════════════════════════════════════════════════════════════════════════════
# PUBLIC API ROUTES  /api/...
# ═════════════════════════════════════════════════════════════════════════════

@api_bp.route("/skills")
def get_skills():
    db = get_db()
    rows = db.execute("SELECT * FROM skills ORDER BY category, name").fetchall()
    db.close()
    return jsonify([row_to_dict(r) for r in rows])


@api_bp.route("/projects")
def get_projects():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM projects ORDER BY featured DESC, created_at DESC"
    ).fetchall()
    db.close()
    return jsonify([row_to_dict(r) for r in rows])


@api_bp.route("/contact", methods=["POST"])
def submit_contact():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received"}), 400

    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields are required"}), 400
    if "@" not in email:
        return jsonify({"success": False, "error": "Invalid email address"}), 400

    db = get_db()
    db.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    db.commit()
    db.close()
    return jsonify({"success": True, "message": "Message sent! I'll get back to you soon."})


# ═════════════════════════════════════════════════════════════════════════════
# ADMIN PANEL ROUTES  /admin/...
# ═════════════════════════════════════════════════════════════════════════════

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if "admin_id" in session:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db   = get_db()
        admin = db.execute(
            "SELECT * FROM admins WHERE username = ?", (username,)
        ).fetchone()
        db.close()
        if admin and check_password_hash(admin["password"], password):
            session["admin_id"]   = admin["id"]
            session["admin_name"] = admin["username"]
            flash("Welcome back! 👋", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "danger")

    return render_template("admin_login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    stats = {
        "total_projects":  db.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
        "total_skills":    db.execute("SELECT COUNT(*) FROM skills").fetchone()[0],
        "total_messages":  db.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
        "unread_messages": db.execute("SELECT COUNT(*) FROM messages WHERE is_read=0").fetchone()[0],
    }
    messages = db.execute(
        "SELECT * FROM messages ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    db.close()
    return render_template("dashboard.html", stats=stats, messages=[row_to_dict(m) for m in messages])


# ── Projects ──────────────────────────────────────────────────────────────────

@admin_bp.route("/projects")
@login_required
def manage_projects():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    db.close()
    return render_template("manage_projects.html", projects=[row_to_dict(p) for p in projects])


@admin_bp.route("/projects/add", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        db = get_db()
        db.execute(
            """INSERT INTO projects (title, description, image, technologies,
               github_url, live_url, category, featured)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                request.form.get("title",        "").strip(),
                request.form.get("description",  "").strip(),
                request.form.get("image",        "images/placeholder.jpg").strip(),
                request.form.get("technologies", "").strip(),
                request.form.get("github_url",   "#").strip(),
                request.form.get("live_url",     "#").strip(),
                request.form.get("category",     "fullstack"),
                1 if "featured" in request.form else 0,
            )
        )
        db.commit()
        db.close()
        flash("Project added successfully! ✅", "success")
        return redirect(url_for("admin.manage_projects"))
    return render_template("add_project.html", project=None)


@admin_bp.route("/projects/edit/<int:pid>", methods=["GET", "POST"])
@login_required
def edit_project(pid):
    db = get_db()
    if request.method == "POST":
        db.execute(
            """UPDATE projects SET title=?, description=?, image=?, technologies=?,
               github_url=?, live_url=?, category=?, featured=? WHERE id=?""",
            (
                request.form.get("title",        "").strip(),
                request.form.get("description",  "").strip(),
                request.form.get("image",        "images/placeholder.jpg").strip(),
                request.form.get("technologies", "").strip(),
                request.form.get("github_url",   "#").strip(),
                request.form.get("live_url",     "#").strip(),
                request.form.get("category",     "fullstack"),
                1 if "featured" in request.form else 0,
                pid
            )
        )
        db.commit()
        db.close()
        flash("Project updated! ✅", "success")
        return redirect(url_for("admin.manage_projects"))

    project = db.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    db.close()
    if not project:
        flash("Project not found.", "danger")
        return redirect(url_for("admin.manage_projects"))
    return render_template("add_project.html", project=row_to_dict(project))


@admin_bp.route("/projects/delete/<int:pid>", methods=["POST"])
@login_required
def delete_project(pid):
    db = get_db()
    db.execute("DELETE FROM projects WHERE id=?", (pid,))
    db.commit()
    db.close()
    flash("Project deleted.", "info")
    return redirect(url_for("admin.manage_projects"))


# ── Skills ────────────────────────────────────────────────────────────────────

@admin_bp.route("/skills")
@login_required
def manage_skills():
    db = get_db()
    skills = db.execute("SELECT * FROM skills ORDER BY category, name").fetchall()
    db.close()
    return render_template("add_skill.html", skills=[row_to_dict(s) for s in skills])


@admin_bp.route("/skills/add", methods=["POST"])
@login_required
def add_skill():
    db = get_db()
    db.execute(
        "INSERT INTO skills (name, icon, category, level) VALUES (?,?,?,?)",
        (
            request.form.get("name",     "").strip(),
            request.form.get("icon",     "fas fa-code").strip(),
            request.form.get("category", "General").strip(),
            int(request.form.get("level", 80)),
        )
    )
    db.commit()
    db.close()
    flash("Skill added! ✅", "success")
    return redirect(url_for("admin.manage_skills"))


@admin_bp.route("/skills/delete/<int:sid>", methods=["POST"])
@login_required
def delete_skill(sid):
    db = get_db()
    db.execute("DELETE FROM skills WHERE id=?", (sid,))
    db.commit()
    db.close()
    flash("Skill deleted.", "info")
    return redirect(url_for("admin.manage_skills"))


# ── Messages ──────────────────────────────────────────────────────────────────

@admin_bp.route("/messages")
@login_required
def view_messages():
    db = get_db()
    messages = db.execute(
        "SELECT * FROM messages ORDER BY created_at DESC"
    ).fetchall()
    db.close()
    return render_template("messages.html", messages=[row_to_dict(m) for m in messages])


@admin_bp.route("/messages/read/<int:mid>", methods=["POST"])
@login_required
def mark_read(mid):
    db = get_db()
    db.execute("UPDATE messages SET is_read=1 WHERE id=?", (mid,))
    db.commit()
    db.close()
    return redirect(url_for("admin.view_messages"))


@admin_bp.route("/messages/delete/<int:mid>", methods=["POST"])
@login_required
def delete_message(mid):
    db = get_db()
    db.execute("DELETE FROM messages WHERE id=?", (mid,))
    db.commit()
    db.close()
    flash("Message deleted.", "info")
    return redirect(url_for("admin.view_messages"))

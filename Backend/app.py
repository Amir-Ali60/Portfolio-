"""
app.py - Main Flask Application
=================================
Run this file to start the server:
    cd portfolio_project/backend
    python app.py

Then visit:
    Portfolio → http://localhost:5000
    Admin     → http://localhost:5000/admin/login

Default admin: username=admin  password=admin123
"""

from flask import Flask, send_from_directory
import os

# ── Create app ────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "change-this-secret-key-in-production-2024"

# ── Register Blueprints ───────────────────────────────────────────────────────
from routes import api_bp, admin_bp
app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/admin")

# ── Serve Frontend Files ──────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ── Start ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from models import init_db, seed_db

    # Initialize database
    init_db()
    seed_db()
    print("\n🚀 Server started!")

    # Render automatically provides PORT environment variable
    port = int(os.environ.get("PORT", 5000))

    # 0.0.0.0 host = external access allowed
    app.run(host="0.0.0.0", port=port)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from config import Config
from database import db
from models.user import User
from models.event import Event  # noqa: F401  (register model)
from routes.auth_routes import auth_bp
from routes.event_routes import event_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # VULN A05: CORS wide open to any origin.
    # FIX: CORS(app, resources={r"/api/*": {"origins": ["https://your.app"]}})
    CORS(app, resources={r"/*": {"origins": "*"}})

    JWTManager(app)
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(event_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")

    @app.errorhandler(Exception)
    def handle_error(e):
        # VULN A05: leaks stack-trace-level detail (exception repr) to clients.
        # FIX: return a generic message; log details server-side only.
        import traceback
        return jsonify({
            "error": str(e),
            "type": e.__class__.__name__,
            "trace": traceback.format_exc(),
        }), 500

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(
            name="Admin",
            email="admin@example.com",
            password=generate_password_hash("Admin@123"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    # VULN A05: debug mode enabled -> Werkzeug debugger / PIN, code exec risk.
    # FIX: debug=False, host="127.0.0.1" behind a proper WSGI server (gunicorn).
    app.run(host="0.0.0.0", port=5000, debug=True)

from pathlib import Path

from flask import Flask


def _load_version() -> str:
    file_path = Path(__file__).resolve()
    candidates = [
        file_path.parents[2] / "docs" / "VERSION",  # entorno local
        file_path.parents[1] / "docs" / "VERSION",  # contenedor (/app/docs/VERSION)
    ]
    for version_file in candidates:
        if version_file.exists():
            value = version_file.read_text(encoding="utf-8").strip()
            if value:
                return value
    return "0.0.0"


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.setdefault("SECRET_KEY", "dev-secret-change-me")
    app.config.setdefault("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)  # 16 MB uploads
    app.config.setdefault("APP_VERSION", _load_version())

    @app.context_processor
    def inject_version():
        return {"app_version": app.config.get("APP_VERSION", "0.0.0")}

    from .routes import bp as main_bp

    app.register_blueprint(main_bp)
    return app

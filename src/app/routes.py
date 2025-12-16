from __future__ import annotations

from flask import Blueprint, flash, render_template, request

from .services import ComparisonResult, compare_records

bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"xls", "xlsx"}


def _allowed(filename: str | None) -> bool:
    return bool(filename and "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS)


@bp.app_template_filter("money")
def money_filter(value):
    """Format numeric values as Spanish-style currency."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return "-"
    text = f"{amount:,.2f}"
    text = text.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{text} €"


@bp.route("/", methods=["GET", "POST"])
def index():
    comparison: ComparisonResult | None = None
    error_message: str | None = None

    if request.method == "POST":
        balance_file = request.files.get("balance_file")
        ddp_file = request.files.get("ddp_file")

        if not balance_file or balance_file.filename == "":
            error_message = "Falta el archivo de Balance."
        elif not ddp_file or ddp_file.filename == "":
            error_message = "Falta el archivo DDP."
        elif not _allowed(balance_file.filename) or not _allowed(ddp_file.filename):
            error_message = "Solo se permiten archivos .xls o .xlsx."
        else:
            try:
                comparison = compare_records(balance_file, ddp_file)
            except Exception as exc:  # pragma: no cover - surface error to UI
                error_message = "No se pudo procesar los archivos. Verifica el formato."
                flash(str(exc), "debug")

        if error_message:
            flash(error_message, "error")

    return render_template("upload.html", comparison=comparison)


@bp.route("/documentacion", methods=["GET"])
def documentation():
    return render_template("documentation.html")

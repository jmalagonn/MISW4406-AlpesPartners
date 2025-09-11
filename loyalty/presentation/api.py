from flask import Blueprint


bp = Blueprint("loyalty", __name__, url_prefix="/loyalty")


@bp.get("/health")
def health():
    return {"status": "Loyalty health serivce ok"}, 200
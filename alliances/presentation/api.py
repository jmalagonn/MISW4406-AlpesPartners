from flask import Blueprint


bp = Blueprint("alliances", __name__, url_prefix="/alliances")

@bp.get("/health")
def health():
    return {"status": "Alliances health serivce ok"}, 200
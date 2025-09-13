from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(httpx.HTTPError)
    def handle_httpx(err):
        return jsonify({"error": "upstream_error", "detail": str(err)}), 502

    @app.errorhandler(Exception)
    def handle_generic(err):
        app.logger.exception("Unhandled error", exc_info=err)
        return jsonify({"error": "internal_error"}), 500

import httpx 

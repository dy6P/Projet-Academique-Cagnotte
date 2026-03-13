from flask import Flask

def create_app():
    app = Flask(__name__)
    from .views import web_ui
    app.register_blueprint(web_ui, url_prefix="/")
    return app
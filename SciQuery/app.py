from flask import Flask
from views.author_views import author_bp
from views.field_views import field_bp
from views.article_views import article_bp

app = Flask(__name__)

app.register_blueprint(author_bp, url_prefix="/api")
app.register_blueprint(field_bp, url_prefix="/api")
app.register_blueprint(article_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
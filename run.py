from app import app
from admin import admin_bp

app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)

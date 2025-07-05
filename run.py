from app import app
from admin import admin_bp
import os

app.register_blueprint(admin_bp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # use Render's assigned port, or 10000 locally
    app.run(debug=False, host='0.0.0.0', port=port)
    

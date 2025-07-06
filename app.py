from flask import Flask
from flask_login import LoginManager
from mongoengine import connect
from config import Config
from dotenv import load_dotenv
load_dotenv()

# Import semua blueprint
from blueprints.auth import auth_bp
from blueprints.menu import menu_bp
from blueprints.transaksi import transaksi_bp
from blueprints.shift import shift_bp
from blueprints.dashboard import dashboard_bp
from blueprints.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Koneksi MongoDB Atlas
    try:
        connect(
            db="restohub",
            host=Config.MONGODB_URI,
            tls=True,
            tlsAllowInvalidCertificates=True  # optional jika TLS error
        )
        print("✅ Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")

    # Setup Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.objects(id=user_id).first()

    # ✅ Context processor untuk template ({{ now }}, {{ datetime }})
    @app.context_processor
    def inject_datetime():
        from datetime import datetime
        return {
            'now': datetime.now(),
            'datetime': datetime
        }

    # Registrasi semua blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(transaksi_bp, url_prefix='/transaksi')
    app.register_blueprint(shift_bp, url_prefix='/shift')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app

# Buat app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

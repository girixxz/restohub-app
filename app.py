from flask import Flask
from flask_login import LoginManager
from mongoengine import connect
from config import Config
from dotenv import load_dotenv
load_dotenv()


# Import blueprints
from blueprints.auth import auth_bp
from blueprints.menu import menu_bp
from blueprints.transaksi import transaksi_bp
from blueprints.shift import shift_bp
from blueprints.dashboard import dashboard_bp
from blueprints.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # MongoDB Atlas connection
    try:
        connect(host=Config.MONGODB_URI)
        print("✅ Connected to MongoDB Atlas!")
        print("🌐 Database: restohub-app.tsghcp7.mongodb.net")
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {str(e)}")
        print("💡 Check your internet connection and MongoDB Atlas credentials")
    
    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign in to access this page.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.objects(id=user_id).first()
    
    # Context processor untuk menyediakan fungsi datetime ke template
    @app.context_processor
    def inject_datetime():
        from datetime import datetime
        return {
            'now': datetime.now(),
            'datetime': datetime
        }
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(transaksi_bp, url_prefix='/transaksi')
    app.register_blueprint(shift_bp, url_prefix='/shift')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

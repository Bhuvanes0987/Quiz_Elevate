
# from flask import Flask
# from .config import Config
# from .db import db
# from .models import *
# from .routes.auth_routes import bp as auth_bp
# from .routes.test_routes import bp as test_bp
# from .routes.admin_routes import bp as admin_bp
# from .routes.analytics_routes import bp as analytics_bp
# from flask_migrate import Migrate
# import mysql.connector

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     db.init_app(app)
#     migrate = Migrate(app, db)
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(test_bp)
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(analytics_bp)
    
    
#     @app.route('/')
#     def root():
#         return jsonify({"message": "QuizElevate API running"}), 200

#     @app.route('/api/health')
#     def health():
#         return jsonify({"status": "ok"}), 200

#     return app

# # db = mysql.connector.connect(
# #     host="localhost",
# #     user="root",
# #     password="Excel@123",
# #     database="quizelevate"
# # )

# if __name__ == '__main__':
#     app = create_app()
#     app.run(host='0.0.0.0', port=8000, debug=True)



# from flask import Flask, jsonify
# from .config import Config
# from .db import db
# from .models import *
# from .routes.auth_routes import bp as auth_bp
# from .routes.test_routes import bp as test_bp
# from .routes.admin_routes import bp as admin_bp
# from .routes.analytics_routes import bp as analytics_bp
# from flask_migrate import Migrate
# import mysql.connector

# def create_app():
#     app = Flask(__name__)   
#     app.config.from_object(Config)

#     # Initialize SQLAlchemy
#     db.init_app(app)
#     migrate = Migrate(app, db)

#     # Register all blueprints
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(test_bp)
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(analytics_bp)

#     DB_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME"),
#     "port": int(os.getenv("DB_PORT", 3306))
# }
# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)

#     # ✅ Health check route
#     @app.route('/api/health', methods=['GET'])
#     def health():
#         return jsonify({"status": "ok"}), 200

#     return app


# # ✅ Create the app
# app = create_app()

# # ✅ Database connection test (runs once on startup)
# try:
#     db_conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Excel@123",
#         database="quizelevate"
#     )
#     print("✅ MySQL connected successfully!")
# except mysql.connector.Error as err:
#     print("❌ MySQL connection failed:", err)


# # ✅ Run the app
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)


# from flask import Flask, jsonify
# from .config import Config
# from .db import db
# from .models import *
# from .routes.auth_routes import bp as auth_bp
# from .routes.test_routes import bp as test_bp
# from .routes.admin_routes import bp as admin_bp
# from .routes.analytics_routes import bp as analytics_bp
# from flask_migrate import Migrate
# import mysql.connector
# import os  # ✅ Needed for env variables

# def create_app():
#     app = Flask(__name__)   
#     app.config.from_object(Config)

#     # ✅ Initialize SQLAlchemy & migrations
#     db.init_app(app)
#     migrate = Migrate(app, db)

#     # ✅ Register blueprints
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(test_bp)
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(analytics_bp)

#     # ✅ Load DB config from .env
#     DB_CONFIG = {
#         "host": os.getenv("DB_HOST"),
#         "user": os.getenv("DB_USER"),
#         "password": os.getenv("DB_PASSWORD"),
#         "database": os.getenv("DB_NAME"),
#         "port": int(os.getenv("DB_PORT", 3306))
#     }

#     def get_db_connection():
#         """Utility function for MySQL connection"""
#         return mysql.connector.connect(**DB_CONFIG)

#     # ✅ Health check route
#     @app.route('/api/health', methods=['GET'])
#     def health():
#         try:
#             conn = get_db_connection()
#             conn.close()
#             return jsonify({"status": "ok", "db": "connected"}), 200
#         except Exception as e:
#             return jsonify({"status": "error", "message": str(e)}), 500

#     return app


# # ✅ Create app instance
# app = create_app()

# # ✅ Run the Flask server
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)


# from flask import Flask, jsonify
# from flask_cors import CORS
# from .config import Config
# from .db import db
# from .models import *
# from .routes.auth_routes import bp as auth_bp
# from .routes.test_routes import bp as test_bp
# from .routes.admin_routes import bp as admin_bp
# from .routes.analytics_routes import bp as analytics_bp
# from .routes.signup_routes import bp as signup_bp  # <-- NEW
# from flask_migrate import Migrate
# import mysql.connector
# import os

# def create_app():
#     app = Flask(__name__)
#     CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
#     app.config.from_object(Config)
#     app.register_blueprint(signup_bp)

#     # Initialize SQLAlchemy + migrations
#     db.init_app(app)
#     Migrate(app, db)

#     # Register all routes
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(test_bp)
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(analytics_bp)
#     app.register_blueprint(signup_bp)   # <-- IMPORTANT

#     return app


# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .config import Config
from .db import db
from .models import *
from .routes.auth_routes import bp as auth_bp
from .routes.test_routes import bp as test_bp
from .routes.admin_routes import bp as admin_bp
from .routes.analytics_routes import bp as analytics_bp
from .routes.signup_routes import bp as signup_bp
from flask_migrate import Migrate
import os
from app.routes.login_routes import bp_login
from app.settings.users import users_bp


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    CORS(app,
     origins=["http://localhost:4200"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])


    # Load config (reads DB from .env)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(bp_login)
    app.register_blueprint(users_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 8000)),
        debug=os.getenv("FLASK_DEBUG", "True") == "True"
    )


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



from flask import Flask, jsonify
from .config import Config
from .db import db
from .models import *
from .routes.auth_routes import bp as auth_bp
from .routes.test_routes import bp as test_bp
from .routes.admin_routes import bp as admin_bp
from .routes.analytics_routes import bp as analytics_bp
from flask_migrate import Migrate
import mysql.connector

def create_app():
    app = Flask(__name__)   
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register all blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)

    # ✅ Health check route
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


# ✅ Create the app
app = create_app()

# ✅ Database connection test (runs once on startup)
try:
    db_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Excel@123",
        database="quizelevate"
    )
    print("✅ MySQL connected successfully!")
except mysql.connector.Error as err:
    print("❌ MySQL connection failed:", err)


# ✅ Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

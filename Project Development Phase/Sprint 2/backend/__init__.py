from dotenv import dotenv_values
from flask import Flask, render_template
from flask_cors import CORS
import ibm_db
from dotenv import load_dotenv
import os
from flask import Flask, send_from_directory

load_dotenv()

dsn_hostname = os.getenv("DB2_HOSTNAME")
dsn_uid = os.getenv("DB2_USERNAME")
dsn_pwd = os.getenv("DB2_PASSWORD")

dsn_driver = os.getenv("DBDRIVER")
dsn_database = os.getenv("DB2_DATABASE")
dsn_port = os.getenv("DB2_PORT")
dsn_protocol = os.getenv("DBPROTOCOL")

# Get the environment variables
config = dotenv_values("backend/.env")

# Connect to db
try:
    conn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)
    print("Connected to IBM_DB2 successfully!!")
    # print(conn)
except:
    print("Failed to connect to Database!")

def create_app():

    app = Flask(__name__, static_folder='../dist')

    # Set the secret key for flask
    app.config['SECRET_KEY'] = 'asdvaweg'

    # Import and register auth_router
    from .auth_router import auth
    app.register_blueprint(auth, url_prefix='/api/auth')

    from .files_router import files
    app.register_blueprint(files, url_prefix='/api/files')

    from .user_router import user
    app.register_blueprint(user, url_prefix='/api/user')

    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    if __name__ == '__main__':
        app.run(use_reloader=True, port=5000, threaded=True)

    return app

# def create_app():
#     # Tell flask to use the build directory of react to serve static content
#     app = Flask(__name__, static_folder='../dist', static_url_path='/')

#     CORS(app)

#     # Set the secret key for flask
#     app.config['SECRET_KEY'] = 'asdvaweg'

#     # Import and register auth_router
#     from .auth_router import auth
#     app.register_blueprint(auth, url_prefix='/api/auth')

#     from .files_router import files
#     app.register_blueprint(files, url_prefix='/api/files')

#     from .user_router import user
#     app.register_blueprint(user, url_prefix='/api/user')

#     # In production serve the index.html page at root

#     @app.route('/')
#     def home():
#         return render_template('index.html')

#     return app

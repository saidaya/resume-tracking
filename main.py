from flask import Flask
from resume_jd.resume_jd_controller import resume_jd_route,resume_jd_route_path
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app)
# register modules/blueprints
CORS(app, resources={r"/*": {"origins": '*'}})
app.register_blueprint(resume_jd_route, url_prefix=f'/{resume_jd_route_path}')
app.config['CORS_HEADERS'] = 'Content-Type'
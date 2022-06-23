n
from flask import Flask,request, jsonify
from flask_cors import CORS
from src.cvreader import CvReader
def return_errors(body):
    if body is None:
            return jsonify({"error":"Body is None"}), 400
    if "cv" not in body:
        return jsonify({"error":"No 'cv' key in body"}), 400
    if "requirements" not in body:
        return jsonify({"error":"No 'requirements' key in body"}), 400
    if "knowledges" not in body["requirements"]:
        return jsonify({"error":"No 'knowledges' key in requirements"}), 400
    if "soft" not in body["requirements"]:
        return jsonify({"error":"No 'soft' key in requirements"}), 400
    if "education" not in body["requirements"]:
        return jsonify({"error":"No 'education' key in requirements"}), 400

def create_app():
    app = Flask(__name__)
    CORS(app)
 
    @app.route("/api/v1/cv", methods=["POST"])

    def post_pdf():
        body = request.json
        base64str = body["cv"]
        requirements = body["requirements"]
        cv = CvReader(base64str,requirements)
        cv.convert_base64_to_pdf()
        return jsonify({
            "knowledges":cv.get_common_knowledges(),
            "soft":cv.get_common_soft_skills(),
            "education":cv.get_common_educations(),
            "translated":cv.translate_text(),
            "compatibility":cv.get_percentage()
        })
 
    return app
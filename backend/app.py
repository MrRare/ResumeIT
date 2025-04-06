from flask import Flask, request, jsonify
from flask_cors import CORS
from jd_processor import process_job_description

app = Flask(__name__)
CORS(app)

@app.route('/match', methods=['POST'])
def match_job_description():
    try:
        data = request.get_json()
        jd_text = data.get('jd_text', '')
        if not jd_text:
            return jsonify({"error": "Job description text is required"}), 400
            
        top_resumes = process_job_description(jd_text)
        return jsonify({"matches": top_resumes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
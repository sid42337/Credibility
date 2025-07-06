from flask import Flask, render_template, request, jsonify
import asyncio

from password_analyzer import analyze_password_strength
from hibp_checker import check_password_breach

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

@app.route("/")
def index():
    """Serves the main HTML page for the password tool."""
    return render_template("index.html")

@app.route("/analyze-password", methods=['POST'])
def analyze_password_route():
    """API endpoint to analyze password strength."""
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({"error": "Password not provided"}), 400

    strength_result = analyze_password_strength(password)
    return jsonify(strength_result)

@app.route("/check-breach", methods=['POST'])
async def check_breach_route():
    """API endpoint to check if a password has been exposed in data breaches."""
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({"error": "Password not provided"}), 400

    breach_result = await check_password_breach(password)
    return jsonify(breach_result)

@app.route("/check-all", methods=['POST'])
async def check_all_route():
    """API endpoint to analyze password strength and check for breaches in one go."""
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({"error": "Password not provided"}), 400

    strength_result = analyze_password_strength(password)
    breach_result = await check_password_breach(password)

    return jsonify({
        "strength": strength_result,
        "breach": breach_result
    })

if __name__ == "__main__":
    app.run(debug=False, port=8000)

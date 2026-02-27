"""
ShapeShift API Server — Backend for the WEB? AI?? website generator UI.
"""
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os, re, uuid, json, sys, random

# New SDK import
try:
    from google import genai
except ImportError:
    genai = None

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

from core import increment_counter, generate_and_save, SITES_DIR, GEN_DIR, BASE_DIR, send_verification_code, verify_code, notify_admin_site_created

# --- BAD WORDS FILTER ---
BAD_WORDS = [
    "pula", "pizda", "muie", "futu-te", "fututi", "jeg", "cacat", "cur", "sugi", 
    "nigger", "faggot", "hitler", "nazi", "porn", "xxx", "sex", "escort"
]

def contains_bad_words(text):
    if not text: return False
    text = text.lower()
    for word in BAD_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            return True
    return False

# Configure Gemini via New SDK
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key and genai:
    try:
        client = genai.Client(api_key=api_key)
        print("READY: ShapeShift Engine Loaded (New SDK)", flush=True)
    except Exception as e:
        print(f"ERROR: Gemini Init — {e}", flush=True)

@app.route('/')
def index():
    return send_from_directory('.', 'shapeshift.html')

@app.route('/view')
def view_page():
    return send_from_directory('.', 'view.html')

@app.route('/demos/<path:filename>')
def serve_demo(filename):
    # Security: only allow the exact basename — no directory traversal
    clean_name = os.path.basename(filename)
    # Use send_from_directory — handles Windows paths + special chars reliably
    try:
        return send_from_directory(SITES_DIR, clean_name)
    except Exception as e:
        print(f"serve_demo error for '{clean_name}': {e}", flush=True)
        return f"<h1>404 – '{clean_name}' not found on server.</h1>", 404

@app.route('/api/demos', methods=['GET'])
def list_demos():
    """Returns a list of all demo sites in the folder."""
    try:
        files = [f for f in os.listdir(SITES_DIR) if f.endswith('.html')]
        # Optional: Parse some info from the filename or just return names
        return jsonify({"demos": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    stats_path = os.path.join(BASE_DIR, 'stats.json')
    try:
        with open(stats_path, 'r') as f:
            stats = json.load(f)
        return jsonify(stats)
    except Exception:
        return jsonify({"sites_created": 149})

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "path": SITES_DIR, "gemini_ready": client is not None})

@app.route('/api/verify/request', methods=['POST'])
def request_verification():
    data = request.get_json()
    email = data.get('email')
    if not email or '@' not in email:
        return jsonify({"error": "Email valid necesar"}), 400
    
    send_verification_code(email)
    return jsonify({"success": True, "message": "Cod trimis pe email (verifică consola în Beta)"})

@app.route('/api/verify/check', methods=['POST'])
def check_verification():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    if verify_code(email, code):
        return jsonify({"success": True})
    return jsonify({"error": "Cod incorect"}), 400

@app.route('/api/generate', methods=['POST'])
def generate_site():
    if not client:
        return jsonify({"error": "Gemini not configured — check API key"}), 503
    
    try:
        data = request.get_json(silent=True) or {}
        biz_name = data.get('biz_name', 'Business')
        biz_category = data.get('biz_category', 'Afacere')
        prompt = data.get('prompt', f"Nume: {biz_name}, Nisa: {biz_category}")

        if contains_bad_words(prompt) or contains_bad_words(biz_name):
            return jsonify({"error": "Offensive content detected. Please keep it professional."}), 400

        biz_data = {
            "name": biz_name,
            "category": biz_category,
            "address": data.get("address", "România"),
            "phone": data.get("phone", ""),
            "reviews": [], "rating": 5, "reviews_count": 0
        }
        
        site_id, filename = generate_and_save(biz_data)
        
        import os
        with open(os.path.join(SITES_DIR, filename), 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Notify Admin
        public_url = os.getenv("PUBLIC_URL", "http://localhost:5000")
        site_url = f"{public_url}/demos/{filename}"
        notify_admin_site_created(biz_name, site_id, site_url)
        
        print(f"GENERATED: {filename}", flush=True)
        return jsonify({"site_id": site_id, "filename": filename, "html": html})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"GENERATE ERROR TRACE: {error_trace}", flush=True)
        return jsonify({
            "error": "A apărut o eroare la generarea site-ului.", 
            "details": str(e),
            "trace": error_trace
        }), 500

@app.route('/api/site/<site_id>', methods=['GET'])
def get_site(site_id):
    # Try direct filename first
    filename = site_id if site_id.endswith('.html') else f"{site_id}.html"
    path = os.path.join(SITES_DIR, filename)
    
    if not os.path.exists(path):
        # Scan dir for the site_id suffix
        files = os.listdir(SITES_DIR)
        match = next((f for f in files if site_id in f), None)
        if match:
            path = os.path.join(SITES_DIR, match)
        else:
            return jsonify({"error": "Not found"}), 404
            
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    return jsonify({"html": html, "site_id": site_id})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"SERVER STARTING ON PORT {port}", flush=True)
    app.run(debug=False, port=port, host='0.0.0.0')

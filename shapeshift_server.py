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

# Use ABSOLUTE path for SITES_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITES_DIR = os.path.join(BASE_DIR, 'demos')
GEN_DIR   = os.path.join(BASE_DIR, 'generated_sites')
os.makedirs(SITES_DIR, exist_ok=True)
os.makedirs(GEN_DIR, exist_ok=True)

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

def increment_counter():
    stats_path = os.path.join(BASE_DIR, 'stats.json')
    try:
        if os.path.exists(stats_path):
            with open(stats_path, 'r') as f:
                stats = json.load(f)
        else:
            stats = {"sites_created": 149}
        
        stats["sites_created"] += 1
        
        with open(stats_path, 'w') as f:
            json.dump(stats, f)
    except Exception as e:
        print(f"Counter Error: {e}")

@app.route('/api/generate', methods=['POST'])
def generate_site():
    if not client:
        return jsonify({"error": "Gemini not configured — check API key"}), 503
    
    data = request.get_json()
    prompt = data.get('prompt', '')
    biz_name = data.get('biz_name', 'Business')

    if contains_bad_words(prompt) or contains_bad_words(biz_name):
        return jsonify({"error": "Offensive content detected. Please keep it professional."}), 400

    try:
        # NEW SDK SYNTAX
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Using stable high-speed flash
            contents=prompt
        )
        html = response.text.strip()
        html = re.sub(r'^```html\n?', '', html)
        html = re.sub(r'\n?```$', '', html)
        
        site_id = str(uuid.uuid4())[:8].upper()
        clean_biz = re.sub(r'[^a-zA-Z0-9]', '_', biz_name).lower()
        filename = f"{clean_biz}_{site_id}.html"
        
        # Save to demos/ (served by Flask) AND generated_sites/ (compatibility)
        for save_dir in [SITES_DIR, GEN_DIR]:
            with open(os.path.join(save_dir, filename), 'w', encoding='utf-8') as f:
                f.write(html)
        
        # Increment counter
        increment_counter()
        
        print(f"GENERATED: {filename} ({len(html)} chars)", flush=True)
        return jsonify({"html": html, "site_id": site_id, "filename": filename})
    except Exception as e:
        print(f"GENERATE ERROR: {type(e).__name__}: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

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

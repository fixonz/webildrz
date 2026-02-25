import os
import json
import re
import uuid
from datetime import datetime
from web_generator import WebGenerator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITES_DIR = os.path.join(BASE_DIR, 'demos')
GEN_DIR = os.path.join(BASE_DIR, 'generated_sites')
STATS_FILE = os.path.join(BASE_DIR, 'stats.json')

os.makedirs(SITES_DIR, exist_ok=True)
os.makedirs(GEN_DIR, exist_ok=True)

def increment_counter():
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        else:
            stats = {"sites_created": 149}
        
        stats["sites_created"] += 1
        
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f)
        return stats["sites_created"]
    except Exception as e:
        print(f"Counter Error: {e}")
        return None

def generate_and_save(biz_data):
    generator = WebGenerator()
    html = generator._generate_ai_html(biz_data)
    
    site_id = str(uuid.uuid4())[:8].upper()
    clean_biz = re.sub(r'[^a-zA-Z0-9]', '_', biz_data['name']).lower()
    filename = f"{clean_biz}_{site_id}.html"
    
    # Save to both folders for consistency
    for d in [SITES_DIR, GEN_DIR]:
        with open(os.path.join(d, filename), 'w', encoding='utf-8') as f:
            f.write(html)
            
    increment_counter()
    return site_id, filename

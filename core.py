import os
import json
import re
import uuid
import random
import requests
import resend
from datetime import datetime
from web_generator import WebGenerator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITES_DIR = os.path.join(BASE_DIR, 'demos')
GEN_DIR = os.path.join(BASE_DIR, 'generated_sites')
STATS_FILE = os.path.join(BASE_DIR, 'stats.json')

os.makedirs(SITES_DIR, exist_ok=True)
os.makedirs(GEN_DIR, exist_ok=True)

# Temporary in-memory storage for verification codes
verification_codes = {}

def send_verification_code(email):
    """Generates and sends a verification code via Resend or Admin Telegram."""
    code = str(random.randint(100000, 999999))
    verification_codes[email] = {
        "code": code,
        "timestamp": datetime.now()
    }
    
    resend_key = os.getenv("RESEND_API_KEY")
    sent_via_email = False
    
    if resend_key:
        try:
            resend.api_key = resend_key
            resend.Emails.send({
                "from": "ShapeShift AI <onboarding@resend.dev>",
                "to": [email],
                "subject": f"Codul tău ShapeShift: {code}",
                "html": f"""
                <div style="font-family: sans-serif; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                    <h2 style="color: #6C63FF;">Salut! 🤖</h2>
                    <p>Codul tău de verificare pentru generarea site-ului este:</p>
                    <div style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #1a1a2e; margin: 20px 0;">{code}</div>
                    <p style="color: #666; font-size: 14px;">Dacă nu tu ai cerut acest cod, poți ignora acest email.</p>
                    <hr>
                    <p style="font-size: 12px; color: #aaa;">WEB? DONE! — N-ai site? Ai acum.</p>
                </div>
                """
            })
            sent_via_email = True
            print(f"📧 EMAIL SENT to {email}")
        except Exception as e:
            print(f"❌ Resend Error: {e}")

    # Fallback/Mirror: Always notify Admin so they can give the code manually if email fails
    admin_id = os.getenv("ADMIN_ID")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if admin_id and bot_token:
        try:
            msg = f"🔑 **COD VERIFICARE NOU**\n\n📧 Email: `{email}`\n🔢 Cod: `{code}`\n\n{'✅ Trimis pe email' if sent_via_email else '⚠️ Eroare Email - Trimite-l manual!'}"
            api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(api_url, json={"chat_id": admin_id, "text": msg, "parse_mode": "Markdown"})
        except Exception as e:
            print(f"Admin Notify Error: {e}")

    return code

def verify_code(email, user_code):
    """Checks if the code is correct."""
    # MASTER CODE for easy testing during Beta
    if str(user_code) == "772517":
        return True
        
    if email in verification_codes:
        saved = verification_codes[email]
        if saved["code"] == str(user_code):
            # Clean up after use
            del verification_codes[email]
            return True
    return False

def notify_admin_site_created(biz_name, site_id, url, chat_id=None):
    """Sends a notification to the ADMIN_ID via Telegram."""
    admin_id = os.getenv("ADMIN_ID")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not admin_id or not bot_token:
        return

    msg = f"✨ **SIT NOU CREAT!**\n\n🏢 Afacere: `{biz_name}`\n🔑 ID: `{site_id}`\n🔗 [Vezi Site-ul]({url})"
    if chat_id:
        msg += f"\n👤 Creat de: `{chat_id}`"
    else:
        msg += f"\n🌐 Creat via: `Website`"

    try:
        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(api_url, json={
            "chat_id": admin_id,
            "text": msg,
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print(f"Admin Notification Error: {e}")

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

def update_site_links(site_id, extra_info):
    """Finds a site by ID and updates its content with new links/info."""
    # Find the file
    filename = None
    files = os.listdir(SITES_DIR)
    for f in files:
        if site_id in f and f.endswith('.html'):
            filename = f
            break
    
    if not filename:
        return False, "Site-ul nu a fost găsit."

    path = os.path.join(SITES_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        old_html = f.read()

    generator = WebGenerator()
    new_html = generator.enrich_html_with_links(old_html, extra_info)

    # Save back to both
    for d in [SITES_DIR, GEN_DIR]:
        with open(os.path.join(d, filename), 'w', encoding='utf-8') as f:
            f.write(new_html)
    
    return True, filename

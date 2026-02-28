import os
import re
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    genai = None

load_dotenv()

class WebGenerator:
    """
    Generates personalized demo landing pages for Romanian businesses.
    Uses Gemini AI to craft the entire HTML/CSS.
    """
    def __init__(self, output_dir="demos"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Configure Gemini via New SDK
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and genai:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None

    def _generate_ai_html(self, biz_data):
        """Uses Gemini and enriches the prompt with real reviews and business context."""
        if not self.client:
            return f"<!DOCTYPE html><html><body><h1>Cheia API Gemini lipsește</h1></body></html>"

        # ... (reviews and street view blocks same as before) ...
        reviews = biz_data.get("reviews", [])
        rating = biz_data.get("rating", 0)
        reviews_count = biz_data.get("reviews_count", 0)
        street_view_url = biz_data.get("street_view_url", None)

        reviews_block = ""
        if reviews:
            reviews_block = f"\nRECENZII REALE GOOGLE ({rating}⭐ din {reviews_count} recenzii):\n"
            for r in reviews:
                stars = "⭐" * int(r.get("rating", 5))
                reviews_block += f'- {stars} "{r["text"]}" — {r["author"]}\n'
        else:
            reviews_block = "\nNu există recenzii disponibile, creează 3 testimoniale plauzibile.\n"

        extra_info = biz_data.get("extra_info", "")
        extra_block = f"\nDETALII IMPORTANTE DE LA CLIENT (Folosește-le în text!):\n{extra_info}\n" if extra_info else ""
        
        logo_base64 = biz_data.get("logo_base64")
        logo_block = f"\nLOGO CLIENT (Include-l în Navbar și Hero): <img src='{logo_base64}' alt='Logo {biz_data['name']}' style='max-height:80px;'>\n" if logo_base64 else ""

        prompt = f"""Creează un landing page HTML complet, single-file, premium, mobile-first pentru:
Afacere: {biz_data['name']} | Nișă: {biz_data['category']} | Loc: {biz_data['address']} | Tel: {biz_data['phone']}
{logo_block}{reviews_block}{extra_block}

TECH: Tailwind CDN + AOS 2.3.4 + Google Fonts.
DESIGN UNIC & CREATIVITATE:
- Fii EXTREM de variat: Folosește font-uri diferite (ex: Roboto+Oswald, Poppins+Merriweather, Syne+Inter, etc) în funcție de nișă.
- Paleta de culori: Alege o paletă de culori UNICĂ și perfect adaptată nișei (ex: pasteluri pentru beauty, dark/gold pentru lux, neon/black pentru tech, earth-tones pentru cafea). Nu folosi mereu albastru/dark-mode.
- Layout Variate: Schimbă structura de bază. Uneori fă un Hero 'split-screen' (text stânga, imagine dreapta), alteori 'centered' cu background full, sau cu un card de contact direct în hero. Diversifică formatele de afișare pentru cards (grid asimetric, masonry, etc).

HEAD obligatoriu:
<script src="https://cdn.tailwindcss.com"></script>
<script>window.tailwind=window.tailwind||{{}};tailwind.config={{content:[],theme:{{extend:{{fontFamily:{{sans:['sans-serif'],display:['serif']}}}}}}}}</script>
<link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">

Înainte de </body>:
<script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
<script>document.addEventListener("DOMContentLoaded",function(){{AOS.init({{duration:800,once:true}})}});</script>

SECȚIUNI (obligatorii dar ordinea și designul să fie CREATIVE, nu rigide): Navbar | Hero cu CTA puternic | Trust bar / Asigurări | Despre/De Ce Noi | Servicii | Testimoniale reale | Footer cu "Site creat de WEB? DONE! © 2026"

IMAGINI — OBLIGATORIU (minim 4 poze reale pe pagină):
Pentru imagini, folosește STRICT formatul loremflickr.com adăugând CUVINTE CHEIE RELEVANTE ÎN ENGLEZĂ extrase din nișă ({biz_data['category']}) și un lock random (1-100) pentru consistență:
Exemple concrete (adaptate la nișă!):
- Hero background: style="background-image: url('https://loremflickr.com/1920/1080/mechanic,car/all?lock=1'); background-size: cover; background-position: center;"
- Secțiunea Despre: <img src="https://loremflickr.com/800/600/engine,repair/all?lock=2" class="w-full h-64 object-cover rounded-xl" alt="Echipa">
- Imagini servicii: <img src="https://loremflickr.com/800/600/auto,service/all?lock=3" class="w-full h-48 object-cover rounded-xl" alt="Serviciu 1">
PUNE MINIM 4-5 imagini pe pagină! AȘA CUM SUNT EXEMPLELE DE MAI SUS. FĂRĂ placeholder urât, folosește DOAR loremflickr.com cu tag-uri STRICT ÎN ENGLEZĂ (ex: dentist,smile / pizza,food / car,mechanic etc).

REGULI: Texte 100% în română, naturale, fără placeholder. Mobile-first cu clase Tailwind responsive. Buton tel:{biz_data['phone']}.{' Logo furnizat: pune-l în navbar și hero.' if biz_data.get('logo_base64') else ''} AOS pe elemente. Returnează DOAR HTML valid începând cu <!DOCTYPE html>. Fără markdown, fără explicații."""
                
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            html_content = response.text.strip()
            
            # Robust cleaning of markdown delimiters
            html_content = re.sub(r'^```(?:html)?\s*', '', html_content, flags=re.MULTILINE)
            html_content = re.sub(r'```\s*$', '', html_content, flags=re.MULTILINE)
            html_content = html_content.strip()

            if "<!DOCTYPE html>" not in html_content and "<html>" not in html_content:
                 raise ValueError("AI response did not provide valid HTML")
            
            return self._surgical_fixes(html_content, biz_data)
        except Exception as e:
            print(f"CRITICAL ERROR (Mobile Fix): {e}")
            return f"<!DOCTYPE html><html><body style='padding:40px; font-family:sans-serif; text-align:center;'><h1>{biz_data['name']}</h1><p>Contact: {biz_data['phone']}</p><p style='color:red;'>AI Generation Failed. Please try again.</p></body></html>"

    def _surgical_fixes(self, html, biz_data):
        """Inyects bulletproof fixes for images and branding."""
        # 1. Broken Image Handler Script
        image_handler = """
        <script>
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('img').forEach(img => {
                img.onerror = function() {
                    if (this.dataset.fixed) return;
                    this.dataset.fixed = "true";
                    this.style.display = 'none';
                    const div = document.createElement('div');
                    div.style.cssText = 'width:100%; min-height:200px; background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%); display:flex; align-items:center; justify-content:center; color:#38bdf8; font-family:system-ui; font-weight:700; text-align:center; padding:20px; border-radius:12px;';
                    div.textContent = '📸 ' + (this.alt || 'Imagine');
                    this.insertAdjacentElement('afterend', div);
                };
            });
        });
        </script>
        """
        
        # Inject before </body>
        if "</body>" in html:
            html = html.replace("</body>", f"{image_handler}</body>")
        else:
            html += image_handler
            
        return html

    def enrich_html_with_links(self, html_content, extra_info):
        """Surgically injects or updates links in existing HTML using a focused AI call."""
        if not self.client or not extra_info:
            return html_content

        prompt = f"""
        Ești un Expert Web Developer. Modifică acest cod HTML pentru a insera/actualiza următoarele link-uri de Social Media sau Info:
        DATE NOI: {extra_info}

        REGULI:
        1. NU MODIFICA Design-ul, Culorile sau Structura principală.
        2. Menține optimizarea MOBILE existentă.
        3. Caută secțiunea de 'Contact' sau 'Footer' și inserează link-urile folosind iconițe sociale (FontAwesome sau simple SVGs).
        4. Dacă link-urile există deja, actualizează-le cu noile valori.
        5. Returnează codul HTML COMPLET actualizat.
        6. Fără ```html, începe direct cu <!DOCTYPE html>.

        COD SURSĂ:
        {html_content[:30000]}
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.1-pro-preview',
                contents=prompt
            )
            enriched_html = response.text.strip()
            # Clean here too
            enriched_html = re.sub(r'^```(?:html)?\s*', '', enriched_html, flags=re.MULTILINE)
            enriched_html = re.sub(r'```\s*$', '', enriched_html, flags=re.MULTILINE)
            enriched_html = enriched_html.strip()

            if "<!DOCTYPE html>" in enriched_html:
                return self._surgical_fixes(enriched_html, {"name": "Enriched Site"})
            return self._surgical_fixes(html_content, {"name": "Enriched Site"})
        except Exception as e:
            print(f"ENRICH ERROR: {e}")
            return html_content

    def generate_site(self, biz_data):
        """Generates a complete unique website using AI and returns (site_id, file_path)."""
        import uuid
        import json
        from datetime import datetime

        print(f"🤖 AI-ul lucrează intens la un design UNIC pentru {biz_data['name']}...")
        html_raw = self._generate_ai_html(biz_data)
        
        # Apply surgical fixes also during final generation call to be sure
        html_content = self._surgical_fixes(html_raw, biz_data)
        
        # Generate ID matching server style
        site_id = str(uuid.uuid4())[:8].upper()
        
        # Unified storage in 'demos' directory (Absolute path)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sites_dir = os.path.join(base_dir, 'demos')
        os.makedirs(sites_dir, exist_ok=True)
        
        file_path = os.path.join(sites_dir, f"{site_id}.html")
        meta_path = os.path.join(sites_dir, f"{site_id}.json")

        meta = {
            "id": site_id,
            "biz_name": biz_data["name"],
            "created": datetime.now().isoformat()
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)
        
        return site_id, os.path.abspath(file_path)

if __name__ == "__main__":
    gen = WebGenerator()
    test_biz = {"name": "Test Auto", "phone": "0722", "address": "Bucuresti", "category": "Service Auto"}
    print(gen.generate_site(test_biz))

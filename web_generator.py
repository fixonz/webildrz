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
        extra_block = f"\nINFORMAȚII SUPLIMENTARE / SOCIAL MEDIA:\n{extra_info}\n" if extra_info else ""

        prompt = f"""
        Ești un Director Creativ de Top Mondial. Creează un Landing Page de LUX, MOBILE-FIRST și VISUALLY STUNNING pentru:
        Nume Afacere: {biz_data['name']}
        Nișă: {biz_data['category']}
        Locație: {biz_data['address']}
        Tel: {biz_data['phone']}
        Rating Google: {rating}⭐ ({reviews_count} recenzii)
        {extra_block}
        
        CERINȚE TEHNICE OBLIGATORII (PRIORITATE MAXIMĂ MOBILE):
        1. MOBILE-FIRST DESIGN: Design-ul trebuie să fie PERFECT pe telefon. Folosește containere flexibile, fonturi lizibile pe ecrane mici și butoane mari, ușor de apăsat.
        2. FAVICON: Trebuie să incluzi un favicon relevant.
        3. BRANDING "WEB? DONE!" în Footer.
        4. DIVERSITATE CROMATICĂ: Culori premium, moderne, potrivite nișei.
        5. IMAGINI (OBLIGATORIU 8-10 POZE): 
           - Hero Background Cinematic.
           - Service Cards specific imagery.
           - O secțiune "Galerie" sau "Atmosferă" cu 4-6 imagini.
           - Folosește Unsplash cu termeni de căutare preciși.
        6. VISUAL RICHNESS: 
           - Design VIBRANT, Image-First, cu spații largi între secțiuni.
           - Folosește overlay-uri subtile de gradient peste imagini.
        7. SOCIAL MEDIA: Dacă au fost oferite link-uri în 'INFORMAȚII SUPLIMENTARE', include-le cu iconițe oficiale în subsol.

        Returnează DOAR codul HTML complet (fără ```html). Începe cu <!DOCTYPE html>.
        """
        
        try:
            # NEW SDK SYNTAX - Updated to Flash experimental for guaranteed access
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            html_content = response.text.strip()
            html_content = re.sub(r'^```html\n?', '', html_content)
            html_content = re.sub(r'\n?```$', '', html_content)

            if "<!DOCTYPE html>" not in html_content and "<html>" not in html_content:
                 raise ValueError("AI response did not provide valid HTML")
            
            return html_content
        except Exception as e:
            print(f"CRITICAL ERROR (Mobile Fix): {e}")
            return f"<!DOCTYPE html><html><body style='padding:40px; font-family:sans-serif; text-align:center;'><h1>{biz_data['name']}</h1><p>Contact: {biz_data['phone']}</p><p style='color:red;'>AI Generation Failed. Please try again.</p></body></html>"

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
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            enriched_html = response.text.strip()
            enriched_html = re.sub(r'^```html\n?', '', enriched_html)
            enriched_html = re.sub(r'\n?```$', '', enriched_html)

            if "<!DOCTYPE html>" in enriched_html:
                return enriched_html
            return html_content
        except Exception as e:
            print(f"ENRICH ERROR: {e}")
            return html_content

    def generate_site(self, biz_data):
        """Generates a complete unique website using AI and returns (site_id, file_path)."""
        import uuid
        import json
        from datetime import datetime

        print(f"🤖 AI-ul lucrează intens la un design UNIC pentru {biz_data['name']}...")
        html_content = self._generate_ai_html(biz_data)
        
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

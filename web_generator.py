import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

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
        
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Using the latest available model in this environment: Gemini 3 Flash
            # Based on debug logs, this model is available and supported.
            self.model = genai.GenerativeModel('models/gemini-3-flash-preview')
        else:
            self.model = None

    def _generate_ai_html(self, biz_data):
        """Uses Gemini and enriches the prompt with real reviews and business context."""
        if not self.model:
            return f"<!DOCTYPE html><html><body><h1>Cheia API Gemini lipsește</h1></body></html>"

        # Build reviews context string
        reviews = biz_data.get("reviews", [])
        rating = biz_data.get("rating", 0)
        reviews_count = biz_data.get("reviews_count", 0)
        street_view_url = biz_data.get("street_view_url", None)

        reviews_block = ""
        if reviews:
            reviews_block = f"\nRECENZII REALE GOOGLE ({rating}⭐ din {reviews_count} recenzii - FOLOSEȘTE-LE ÎN DESIGN):\n"
            for r in reviews:
                stars = "⭐" * int(r.get("rating", 5))
                reviews_block += f'- {stars} "{r["text"]}" — {r["author"]}\n'
            reviews_block += "\nINSTRUCȚIUNE: Incluzi o secțiune TESTIMONIALE cu aceste recenzii reale. Citatul trebuie să fie mare, vizibil, cu stilizare 'quote' elegantă (ghilimele mari, fundal subtil, avatar placeholder cu inițialele autorului).\n"
        else:
            reviews_block = "\nNu există recenzii disponibile, creează 3 testimoniale plauzibile pentru nișa lor.\n"

        street_view_block = ""
        if street_view_url:
            street_view_block = f"\nFOTO FAȚADĂ REALĂ: Include această imagine a intrării afacerii în secțiunea 'Despre noi': {street_view_url}\n"

        prompt = f"""
        Ești un Director Creativ de Top Mondial. Creează un Landing Page de LUX, MOBILE-FIRST și VISUALLY STUNNING pentru:
        Nume Afacere: {biz_data['name']}
        Nișă: {biz_data['category']}
        Locație: {biz_data['address']}
        Tel: {biz_data['phone']}
        Rating Google: {rating}⭐ ({reviews_count} recenzii)
        Partener: WEB? DONE!
        {reviews_block}{street_view_block}
        CERINȚE TEHNICE OBLIGATORII:
        1. FAVICON: Trebuie să incluzi un favicon relevant (emoji sau icon link).
        2. BRANDING "WEB? DONE!" în Footer: "Acest site a fost creat instant de WEB? DONE! --- N-ai site? Ai acum.."
        3. DIVERSITATE CROMATICĂ (FĂRĂ REPETAREA ACESTORA):
           - GRĂDINIȚĂ: Culori pastelate vesele (Soft Cyan, Lemon, Mint). FĂRĂ NEGRU.
           - MEDICAL: Teal, Royal Blue sau Platinum Emerald.
           - RESTAURANT: Deep Burgundy, Slate Gold sau Forest Green.
           - FITNESS: Acid Yellow, Electric Indigo sau High-Contrast Monochrome.
           - GENERAL: Evită combinația de Orange și Black (este prea comună). Caută palete proaspete, premium, care să surprindă utilizatorul.
        4. SECȚIUNI OBLIGATORII:
           - Hero cu rating-ul afacerii ({rating}⭐) vizibil (badge trust).
           - Secțiune TESTIMONIALE cu recenziile reale de mai sus (design premium, fiecare card are avatar cu inițiale, stele, citat și nume autor).
           - Servicii/Features grid.
           - Contact cu buton "Sună Acum" proeminent pentru {biz_data['phone']}.
        5. IMAGINI (OBLIGATORIU 8-10 POZE):
           - Hero Background Cinematic (full width).
           - Cel puțin o poză Unsplash pentru FIECARE serviciu/feature.
           - O secțiune "Galerie" sau "Atmosferă" cu 4-6 imagini grid.
           - Folosește keywords precise în engleză pentru Unsplash.
        6. VISUAL RICHNESS: 
           - Design-ul trebuie să fie VIBRANT, Image-First, cu spații largi între secțiuni.
           - Folosește `object-fit: cover` și `aspect-ratio` moderne.
           - Adaugă overlay-uri subtile de gradient peste imagini pentru contrast.
        7. MOBILE-FIRST absolut.

        COPYWRITING: Română, bazat pe experiența reală din recenzii (dacă clienții menționează "fără durere", "prețuri corecte", "echipă prietenoasă" — folosește asta în headlines și USP-uri!).
        CALITATE: Design de 10.000 EUR. Returnează DOAR codul HTML complet (fără ```html). Începe cu <!DOCTYPE html>.
        """
        
        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                raise ValueError("Response text is empty")
            
            html_content = response.text.strip()
            html_content = re.sub(r'^```html\n?', '', html_content)
            html_content = re.sub(r'\n?```$', '', html_content)

            if "<!DOCTYPE html>" not in html_content and "<html>" not in html_content:
                 raise ValueError("AI response did not provide valid HTML")
            
            return html_content
        except Exception as e:
            print(f"CRITICAL ERROR (Mobile Fix): {e}")
            return f"<!DOCTYPE html><html><body style='padding:20px; font-family:sans-serif;'><h1>{biz_data['name']}</h1><p>Contact: {biz_data['phone']}</p></body></html>"

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

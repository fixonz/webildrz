try:
    from google import genai
except ImportError:
    genai = None

from dotenv import load_dotenv

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

        prompt = f"""
        Ești un Director Creativ de Top Mondial. Creează un Landing Page de LUX, MOBILE-FIRST și VISUALLY STUNNING pentru:
        Nume Afacere: {biz_data['name']}
        Nișă: {biz_data['category']}
        Locație: {biz_data['address']}
        Tel: {biz_data['phone']}
        Rating Google: {rating}⭐ ({reviews_count} recenzii)
        
        CERINȚE TEHNICE OBLIGATORII:
        1. FAVICON: Trebuie să incluzi un favicon relevant.
        2. BRANDING "WEB? DONE!" în Footer.
        3. DIVERSITATE CROMATICĂ: Culori premium, moderne, potrivite nișei.
        4. IMAGINI (OBLIGATORIU 8-10 POZE): 
           - Hero Background Cinematic.
           - Service Cards specific imagery.
           - O secțiune "Galerie" sau "Atmosferă" cu 4-6 imagini.
           - Folosește Unsplash cu termeni de căutare preciși.
        5. VISUAL RICHNESS: 
           - Design VIBRANT, Image-First, cu spații largi între secțiuni.
           - Folosește overlay-uri subtile de gradient peste imagini.
        6. MOBILE-FIRST absolut.

        Returnează DOAR codul HTML complet (fără ```html). Începe cu <!DOCTYPE html>.
        """
        
        try:
            # NEW SDK SYNTAX
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
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

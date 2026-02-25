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

        prompt = f"""
        Ești **LUXE** — Creative Director & High-Conversion Designer de top mondial (nivel Awwwards SOTD + agenții de 8-15k€ per landing page). 
        Creezi landing page-uri care arată scump, convertesc extrem de bine și inspiră încredere instant.

        Creează un **landing page SINGLE-FILE premium 2026-level, ultra-modern, mobile-first** pentru:

        **Nume afacere:** {biz_data['name']}
        **Nișă:** {biz_data['category']}
        **Locație:** {biz_data['address']}
        **Telefon:** {biz_data['phone']}

        {logo_block}
        {reviews_block}
        {extra_block}

        ### DIRECTIVE OBLIGATORII (urmează-le 100%):

        1. **Tehnologie (FOARTE IMPORTANT)**
           - Folosește **Tailwind CSS 3.4+ via CDN** (`https://cdn.tailwindcss.com`)
           - Adaugă imediat după tag-ul <head> un script de configurare Tailwind cu fonturi premium și culori accent potrivite nișei
           - Animații fluide (fade-in, slide-up, scale) cu Tailwind + Intersection Observer
           - Glassmorphism subtil + gradients elegante + whitespace generos

        2. **Structură Obligatorie a Paginii (în ORDINEA asta exactă):**
           - Navbar sticky premium (logo stânga mare + meniu + buton "Sună Acum")
           - BANNER DISCRET STICKY-TOP: "N-AI WEB? AI ACUM! - Design Experimental (Beta)" (foarte elegant, font mic, nu deranjează)
           - HERO cinematic full-viewport (background Unsplash ultra-impact, headline magnetic + subheadline + 2 CTA-uri)
           - Secțiune Trust / Social Proof (rating + recenzii scurte)
           - Secțiune "De Ce Noi" (3-4 beneficii cards elegante)
           - Secțiune Servicii / Oferte (grid de cards cu hover lift)
           - Galerie Foto (masonry grid modern, 6-9 poze)
           - Testimoniale (folosește recenzii reale + stele)
           - CTA final puternic
           - Footer complet

        3. **Copywriting de lux**
           - Folosește framework PAS (Problem → Agitate → Solution) în Hero
           - Ton: premium, cald, autoritar, natural în română (ca un copywriter scump)
           - Headline-ul să fie scurt, puternic și specific nișei

        4. **Imagini (CRUCIAL pentru calitate)**
           - Hero background: Unsplash cinematic, foarte specific (ex: "mechanic hands repairing luxury engine dramatic lighting cinematic")
           - Toate pozele: Unsplash/Pexels de calitate excepțională, cu parametri `?auto=format&fit=crop&w=2000&q=80`
           - Minimum 8-10 imagini de impact

        5. **Logo**
           - Dacă ai furnizat logo_base64 → pune-l PROMINENT în Navbar (stânga) și în Hero (centru sau jos). Este prioritate maximă!

        6. **Alte reguli**
           - Mobile-first perfect (gândește-te constant la iPhone 16 Pro)
           - Nu menționa niciodată AI, Gemini, Telegram, bot sau "generat de"
           - Site-ul trebuie să arate ca și cum l-a făcut o agenție de top din București/Cluj

        Returnează **DOAR** codul HTML complet, valid, începând direct cu <!DOCTYPE html>. 
        Fără markdown, fără ```html, fără explicații, fără comentarii extra.
        """
                
        try:
            # UPGRADING TO GEMINI 3.1 PRO as requested for superior design
            response = self.client.models.generate_content(
                model='gemini-3.1-pro-preview',
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
            const handleBrokenImages = () => {
                document.querySelectorAll('img').forEach(img => {
                    if (img.dataset.fixed) return;
                    img.onerror = function() {
                        this.style.display = 'none';
                        const div = document.createElement('div');
                        div.style.cssText = 'width:100%; min-height:250px; background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%); display:flex; align-items:center; justify-content:center; color:#38bdf8; font-family:system-ui, sans-serif; font-weight:800; text-align:center; padding:20px; border-radius:16px; border:1px solid rgba(56,189,248,0.2); margin:10px 0;';
                        div.innerHTML = '<div style="display:flex; flex-direction:column; gap:8px;"><span>🖼️ IMAGINE OPTIMIZATĂ AI</span><span style="font-size:0.7rem; color:rgba(255,255,255,0.5);">N-AI WEB? AI ACUM!</span></div>';
                        this.insertAdjacentElement('afterend', div);
                        this.dataset.fixed = "true";
                    };
                    // Trigger for cached broken images
                    if (img.complete && img.naturalHeight === 0) img.onerror();
                });
            };
            handleBrokenImages();
            // Also watch for dynamically added images
            new MutationObserver(handleBrokenImages).observe(document.body, {childList: true, subtree: true});
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

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
        Ești **LUXE 2026** — cel mai elite Creative Director + High-Conversion Web Architect din lume (Awwwards SOTD, agenții 12-25k€/proiect, clienți Porsche, Rolex, Clinici de lux din Dubai & București).

        Creezi un **landing page SINGLE-FILE ULTRA-PREMIUM 2026**, mobile-first, cinematic, cu conversie maximă pentru:

        **Nume afacere:** {biz_data['name']}
        **Nișă:** {biz_data['category']}
        **Locație:** {biz_data['address']}
        **Telefon:** {biz_data['phone']}

        {logo_block}
        {reviews_block}
        {extra_block}

        ### TECH STACK OBLIGATORIU (nu negocia, folosește exact):
        - Tailwind CSS 3.4+ via CDN: https://cdn.tailwindcss.com
        - AOS (Animate On Scroll) v2.3.4: https://unpkg.com/aos@2.3.4/dist/aos.css + https://unpkg.com/aos@2.3.4/dist/aos.js
        - Fonturi: Inter (body) + Playfair Display / Satoshi (headings) via Google Fonts
        - Iconițe: Heroicons inline SVG + Font Awesome 6 (via CDN)
        - Glassmorphism + micro-animations + scroll-triggered effects
        - Dark/light elegant (default dark dacă nișa e premium/auto/lux)

        ### SCRIPT TAILWIND OBLIGATORIU (pune-l imediat după <head>):
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
          tailwind.config = {{
            content: [],
            theme: {{
              extend: {{
                fontFamily: {{ 
                  sans: ['Inter', 'system-ui', 'sans-serif'],
                  display: ['Playfair Display', 'sans-serif']
                }},
                colors: {{ 
                  primary: {{ 50: '#f0f9ff', 500: '#0ea5e9', 600: '#0284c8', 900: '#0c4a6e' }}  // AI-ul va adapta la nișă
                }}
              }}
            }}
          }}
        </script>
        <link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">
        <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>

        ### STRUCTURA EXACTĂ A PAGINII (în această ordine, cu aceste ID-uri):
        1. **<nav id="navbar">** — sticky top, glassmorphism, logo mare stânga (dacă există logo_base64 → folosește-l cu prioritate MAXIMĂ), meniu + buton "Sună Acum" roșu/auriu
        2. **Banner discret sticky-top** (sub navbar): "N-AI WEB? AI ACUM! - Design Experimental (Beta)" — font foarte mic, elegant, nu deranjează
        3. **Hero Section** (full viewport, h-screen) — background Unsplash cinematic ultra-specific + overlay gradient + headline magnetic + subheadline + 2 CTA (Sună + WhatsApp)
        4. **Trust Bar** — rating + număr recenzii + "Lucrăm cu clienți din 2018"
        5. **De Ce Noi** (3-4 cards elegante cu icon + AOS fade-up)
        6. **Servicii / Oferte** (grid 1-3 coloane pe mobile, hover lift + shadow-xl)
        7. **Galerie Foto** (masonry grid responsive, 8-10 poze, lightbox simplu)
        8. **Testimoniale** (carousel sau grid cu recenzii reale + poze Unsplash avatar)
        9. **CTA Final Puternic** (full-width, gradient, număr de telefon mare)
        10. **Footer** complet + copyright

        ### IMAGINI — STRATEGIE NUCLEARĂ:
        - Toate pozele: `https://images.unsplash.com/photo-...` + `?auto=format&fit=crop&w=2000&q=85&ixlib=rb-4.0.3`
        - Hero: termen extrem de specific (ex: "luxury car mechanic workshop dramatic lighting cinematic" sau "elegant beauty salon interior golden hour")
        - Galerie: 8-10 poze ultra-specifice nișei (close-up-uri, before/after, echipamente, echipa etc.)
        - Minimum 10 imagini de impact total

        ### COPYWRITING RULES (ton de lux):
        - Folosește framework-ul PAS + Emotional Triggers
        - Headline Hero: maxim 8 cuvinte, ultra-puternic
        - Toate textele 100% naturale în română, ca și cum ar fi scris un copywriter de 500€/zi
        - Nu menționa niciodată AI, Gemini, Telegram, bot, "generat de"

        ### REGULI FINALE STRICTE:
        - Logo_base64 (dacă există) → TREBUIE să apară în navbar (stânga, max-h-14) și în Hero (centru sus sau jos)
        - Mobile-first perfect (testează mintal pe iPhone 16 Pro — padding generos, font ≥16px)
        - Animații AOS peste tot: data-aos="fade-up" / "zoom-in" / "fade-right"
        - Buton "Sună Acum" → tel:{biz_data['phone']}
        - Returnează **DOAR** codul HTML complet, valid, începând direct cu <!DOCTYPE html>
        - Fără markdown, fără ```html, fără comentarii, fără explicații de niciun fel.

        Acum creează capodopera.
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

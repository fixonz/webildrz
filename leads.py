import os
import requests
from dotenv import load_dotenv
load_dotenv()

class LeadGenerator:
    """
    Finds local businesses in Romania that do not have a website.
    Uses SerpApi (Google Maps) for reliable data retrieval.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SERP_API_KEY")
        self.base_url = "https://serpapi.com/search"

    def find_leads(self, location="Bucuresti, Romania", query="service auto", limit=10):
        """
        Searches for businesses without websites, then enriches each with reviews + street view.
        """
        if not self.api_key:
            print("Warning: No SERP_API_KEY found. Returning mock data.")
            return self._get_mock_leads()

        leads = []
        start = 0
        
        while len(leads) < limit and start < 60:
            params = {
                "engine": "google_maps",
                "q": query,
                "location": location,
                "type": "search",
                "api_key": self.api_key,
                "start": start
            }

            try:
                response = requests.get(self.base_url, params=params)
                data = response.json()
                results = data.get("local_results", [])
                
                if not results:
                    break

                for biz in results:
                    if biz.get("phone") and not biz.get("website"):
                        place_id = biz.get("place_id", "")
                        lead = {
                            "name": biz.get("title"),
                            "phone": biz.get("phone"),
                            "address": biz.get("address"),
                            "category": biz.get("type", query),
                            "rating": biz.get("rating"),
                            "reviews_count": biz.get("reviews"),
                            "place_id": place_id,
                            "reviews": [],
                            "street_view_url": self._get_street_view_url(biz.get("address", ""))
                        }
                        # Enrich with reviews if place_id exists
                        if place_id:
                            lead["reviews"] = self._fetch_reviews(place_id)
                        leads.append(lead)
                        if len(leads) >= limit:
                            break
                
                start += 20
            except Exception as e:
                print(f"Error fetching leads at start={start}: {e}")
                break
                
        return leads

    def _get_street_view_url(self, address, size="800x400"):
        """Returns a Google Street View Static API URL for the business address."""
        if not address:
            return None
        encoded = requests.utils.quote(f"{address}, Romania")
        # Uses Google Street View Static API (free tier: 25k/month)
        key = os.getenv("GOOGLE_MAPS_KEY", "")
        if key:
            return f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={encoded}&key={key}"
        # Fallback: use a Unsplash street-level photo relevant to the niche
        return None

    def _fetch_reviews(self, place_id, max_reviews=3):
        """Fetches top Google reviews for a business via SerpApi."""
        try:
            params = {
                "engine": "google_maps_reviews",
                "place_id": place_id,
                "api_key": self.api_key,
                "hl": "ro",
                "sort_by": "qualityScore"
            }
            response = requests.get(self.base_url, params=params, timeout=8)
            data = response.json()
            raw_reviews = data.get("reviews", [])
            reviews = []
            for r in raw_reviews[:max_reviews]:
                snippet = r.get("snippet") or r.get("text", "")
                if snippet and len(snippet) > 30:
                    reviews.append({
                        "author": r.get("user", {}).get("name", "Client"),
                        "rating": r.get("rating", 5),
                        "text": snippet[:300]  # Cap length
                    })
            return reviews
        except Exception:
            return []


    def _get_mock_leads(self):
        """Mock data with rich reviews for varied Romanian businesses."""
        return [
            {"name": "Dentist Elite București", "phone": "+40 711 222 333", "address": "Sector 1, București", "category": "Cabinet Stomatologic", "rating": 4.9, "reviews": [
                {"author": "Maria P.", "rating": 5, "text": "Cel mai bun cabinet stomatologic din București! Medicii sunt extraordinari, clinica arată impecabil și nu am simțit absolut nicio durere."},
                {"author": "Andrei M.", "rating": 5, "text": "Am venit cu frică și am plecat zâmbind. Aparatele sunt ultra-moderne și personalul este extrem de calduros și profesionist."},
                {"author": "Elena T.", "rating": 5, "text": "Am făcut implant dentar aici și rezultatul e perfect. Prețuri corecte, comunicare excelentă, recomand cu mare drag!"}
            ], "street_view_url": None, "place_id": None, "reviews_count": 342},
            {"name": "Avocat Popescu & Asociații", "phone": "+40 722 333 444", "address": "Sector 2, București", "category": "Cabinet Avocatură", "rating": 4.7, "reviews": [
                {"author": "Bogdan I.", "rating": 5, "text": "Profesionalism desăvârșit. Avocatul meu a rezolvat un caz complicat de proprietate în timp record. M-am simțit protejat și informat pe tot parcursul."},
                {"author": "Carmen S.", "rating": 5, "text": "Îmi recomand familia cu toată încrederea. Sfaturi clare, onorarii transparente și o echipă pe care te poți baza 100%."},
                {"author": "Dan R.", "rating": 4, "text": "Servicii de calitate superioară. Au câștigat pentru noi un process dificil. Singurul downside e că sunt foarte căutați și uneori greu de prins."}
            ], "street_view_url": None, "place_id": None, "reviews_count": 178},
            {"name": "Grădinița Prichindeii Veseli", "phone": "+40 733 444 555", "address": "Sector 3, București", "category": "Grădiniță Particulară", "rating": 4.8, "reviews": [
                {"author": "Ioana V.", "rating": 5, "text": "Fetița mea plânge când nu vrea să plece de la grădiniță! Educatoarele sunt incredbile, mediul e sigur și curat, iar programele creative sunt excelente."},
                {"author": "Mihai C.", "rating": 5, "text": "Cel mai bun loc din Sector 3 pentru copiii de 3-6 ani. Curățenie impecabilă, mâncare gătită zilnic și un program echilibrat."},
                {"author": "Laura O.", "rating": 5, "text": "Fiul nostru a crescut atât de mult în 6 luni! Vorbește engleza, desenează, cântă. Îi mulțumim din suflet doamnei educatoare!"}
            ], "street_view_url": None, "place_id": None, "reviews_count": 215},
            {"name": "Bio-Clinic Medical Center", "phone": "+40 744 555 666", "address": "Sector 4, București", "category": "Clinică Medicală", "rating": 4.6, "reviews": [
                {"author": "Radu N.", "rating": 5, "text": "Am evitat cozile de la stat venind aici. Analizele au ieșit în câteva ore, medicul a explicat totul clar. O clinică serioasă!"},
                {"author": "Simona G.", "rating": 4, "text": "Dotare excelentă și medici competenți. Prețuri accesibile față de alte clinici private. Am venit cu toată familia."},
                {"author": "Vlad A.", "rating": 5, "text": "Eco și analize de sânge în aceeași zi. Personal prietenos, timp de așteptare minim. Recomand!"}
            ], "street_view_url": None, "place_id": None, "reviews_count": 289},
            {"name": "Urban Cafe & Bistro", "phone": "+40 755 666 777", "address": "Sector 5, București", "category": "Restaurant", "rating": 4.4, "reviews": [
                {"author": "Ana M.", "rating": 5, "text": "Locul perfect pentru brunch! Cafeaua e divină, avocado toast perfect, și atmosfera e super relaxantă. Mă întorc în fiecare weekend."},
                {"author": "Cristian B.", "rating": 4, "text": "Meniu variat, prețuri rezonabile pentru zona centrală. Personalul e tânăr și zâmbitor. Muzica ambientală e pe gustul meu."},
                {"author": "Diana F.", "rating": 5, "text": "Am organizat un mic eveniment de business aici și a fost totul perfect. Sunt flexibili și mâncarea e mereu proaspătă și delicioasă!"}
            ], "street_view_url": None, "place_id": None, "reviews_count": 156},
            {"name": "Sky Gym Fitness Sector 6", "phone": "+40 766 777 888", "address": "Sector 6, București", "category": "Sală Fitness", "rating": 4.5, "reviews": [
                {"author": "Alex P.", "rating": 5, "text": "Echipamente de ultimă generație, antrenori super motivați și o atmosferă de campion. Cele mai bune rezultate pe care le-am obținut vreodată!"},
                {"author": "Ioana C.", "rating": 5, "text": "Am slăbit 15 kg în 4 luni cu ajutorul antrenorilor de aici. Sunt ca o familie, te susțin la fiecare pas. 100% recomand!"},
                {"author": "Marius T.", "rating": 4, "text": "Cea mai bine dotată sală din Sector 6. Vestiare curate, muzică bună și program lung. Singurul minus e că se aglomerează seara."}
            ], "street_view_url": None, "place_id": None, "reviews_count": 201},
            {"name": "Royal Spa & Beauty", "phone": "+40 777 888 999", "address": "Sector 1, București", "category": "Salon Înfrumusețare", "rating": 4.9, "reviews": [
                {"author": "Raluca D.", "rating": 5, "text": "Am ieșit de la Royal Spa transformată complet! Terapia cu pietre calde și masajul cu argan oil au fost de neuitat. Locul de vis!"},
                {"author": "Monica S.", "rating": 5, "text": "Servicii de 5 stele la prețuri corecte. Personalul e instruit impecabil și simți că ești cu adevărat în centrul atenției. Revin mereu!"},
                {"author": "Elena B.", "rating": 5, "text": "Cel mai bun loc pentru o evadare de la rutina zilnică. Aromele, muzica, totul e gândit perfect. Giftcard-ul primit de ziua mea a fost cel mai tare cadou!"}
            ], "street_view_url": None, "place_id": None, "reviews_count": 412},
            {"name": "Construct Pro Solutions", "phone": "+40 788 999 000", "address": "Ilfov, București", "category": "Servicii Construcții", "rating": 4.3, "reviews": [
                {"author": "Gheorghe A.", "rating": 4, "text": "Am renovat complet bucătăria și baia cu echipa lor. Lucrare finalizată la timp, prețuri negociate corect și finisaje de calitate bună."},
                {"author": "Florin M.", "rating": 5, "text": "Profesioniști adevărați! Am ridicat un garaj și m-au sfătuit la fiecare pas. Comunicare excelentă și materiale de calitate."},
                {"author": "Adriana C.", "rating": 4, "text": "Recomand pentru renovări interioare. Echipa vine la timp, e curată și respectă spațiul. Am primit și garanție pe lucrare."}
            ], "street_view_url": None, "place_id": None, "reviews_count": 98}
        ]

if __name__ == "__main__":
    # Quick test
    gen = LeadGenerator()
    leads = gen.find_leads()
    print(f"Found {len(leads)} leads without websites:")
    for l in leads:
        print(f"- {l['name']} ({l['phone']})")

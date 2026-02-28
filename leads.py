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
            print("Warning: No SERP_API_KEY found.")
            return []

        leads = []
        start = 0
        
        while len(leads) < limit and start < 60:
            params = {
                "engine": "google_maps",
                "q": f"{query} in {location}",
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
            for r in raw_reviews:
                rating = r.get("rating", 5)
                # Only include positive reviews (4 or 5 stars)
                if rating >= 4:
                    snippet = r.get("snippet") or r.get("text", "")
                    if snippet and len(snippet) > 30:
                        reviews.append({
                            "author": r.get("user", {}).get("name", "Client"),
                            "rating": rating,
                            "text": snippet[:300]  # Cap length
                        })
                        if len(reviews) >= max_reviews:
                            break
            return reviews
        except Exception:
            return []

if __name__ == "__main__":
    # Quick test
    gen = LeadGenerator()
    leads = gen.find_leads()
    print(f"Found {len(leads)} leads without websites:")
    for l in leads:
        print(f"- {l['name']} ({l['phone']})")

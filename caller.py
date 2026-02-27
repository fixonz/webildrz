import os
import requests
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    genai = None

load_dotenv()

class ColdCaller:
    """
    Handles automated sales calls in Romanian using Retell AI + Gemini.
    Optimized for presenting a pre-built website using a short ID.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("RETELL_API_KEY")
        self.base_url = "https://api.retellai.com"
        self.agent_id = os.getenv("RETELL_AGENT_ID")
        self.view_url_base = os.getenv("VIEW_URL", "http://localhost:5000/view")
        
        # Initialize Gemini for pre-call strategic planning
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key and genai:
            self.gemini_client = genai.Client(api_key=gemini_api_key)
        else:
            self.gemini_client = None

    def _generate_smart_pitch(self, biz_name, category):
        """Uses Gemini to craft a hyper-personalized hook for the AI Caller."""
        if not self.gemini_client:
            return f"Salutare, te sunăm de la Web Done. Am creat un site gratuit pentru {biz_name}. Vrei să îl vezi?"
            
        prompt = f"""
        Ești un expert în vânzări B2B (Cold Calling).
        Generează 'Gheața' (The Hook) de 2 propoziții scurte pentru un apel telefonic către afacerea: '{biz_name}' din domeniul '{category}'.
        
        Context: Deja am construit un site web Premium, gratis, demonstrativ, special pentru ei.
        Nu folosi limbaj de lemn sau robotic. Fii amical, românesc (folosește 'tu' sau 'dumneavoastră' în funcție de domeniu, ex: 'tu' la curățenie/construcții, 'dumneavoastră' la clinică medicală).
        
        Exemplu bun: "Salutare! Am observat afacerea ta și mi-a plăcut mult ce faceți. Fiindcă la Web Done testăm niște designuri noi, echipa mea ți-a construit deja un site complet, gratuit, să vezi cum arată."
        Exemplu bun 2: "Bună ziua, vă deranjez un minut. Am văzut {biz_name} online și am decis să vă fac o surpriză: v-am creat un site web modern, luxos, cu imagini gata puse, ca o demonstrație."
        
        Returnează DOAR pitch-ul, fără ghilimele, fără alte explicații.
        """
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except:
            return f"Salutare, te sunăm de la Web Done. Am creat un site gratuit pentru {biz_name}. Vrei să îl vezi?"

    def place_call(self, biz_name, phone, site_id, category="Afacere"):
        """Initiates a custom-crafted call to the business."""
        
        # Generate the brain layer of the call
        print(f"🧠 [AI] Generating psychological sales pitch for {biz_name}...")
        custom_pitch = self._generate_smart_pitch(biz_name, category)
        print(f"📝 [PITCH]: {custom_pitch}")
        
        if not self.api_key or not self.agent_id:
            print(f"\n--- DRY RUN (Missing API Keys) ---")
            print(f"Calling: {biz_name} at {phone} ({category})")
            print(f"Goal: Tell them to enter code [{site_id}] on {self.view_url_base}")
            return {"status": "dry_run", "site_id": site_id, "pitch": custom_pitch}

        # Optimized payload for presenting the site
        demo_link = f"{self.view_url_base}?id={site_id}"
        
        payload = {
            "from_number": os.getenv("RETELL_PHONE_NUMBER"),
            "to_number": phone,
            "agent_id": self.agent_id,
            "retell_llm_dynamic_variables": {
                "customer_name": biz_name,
                "site_id": site_id,
                "demo_url": demo_link,
                "view_base_url": self.view_url_base,
                "category": category,
                "custom_pitch": custom_pitch  # Retell AI will read this exact hook!
            }
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"🚀 [CALL] Presenting website to {biz_name}...")
            response = requests.post(
                f"{self.base_url}/v2/create-phone-call",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ [SUCCESS] Call active! ID: {result.get('call_id')}")
                print(f"🔗 [INFO] They will be directed to: {demo_link}")
                return result
            else:
                print(f"❌ [ERROR] Retell failed: {response.status_code} - {response.text}")
                return {"status": "error", "message": response.text}
        except Exception as e:
            print(f"⚠️ [CRITICAL] Connection error: {e}")
            return {"status": "exception", "error": str(e)}

if __name__ == "__main__":
    # EASY INSERTION FOR PREVIEW/TESTING
    print("\n--- WEB? DONE! Quick Caller ---")
    
    # You can quickly change these for testing
    TEST_BIZ = "Auto Ionescu"
    TEST_PHONE = "+407XXXXXXXX" # Fill in for real test
    TEST_CODE = "ABCD1234"      # Paste your generated site ID here
    
    # Prompt for input if running interactively
    try:
        choice = input(f"Press Enter to call '{TEST_BIZ}' with code '{TEST_CODE}' or type 'new' to enter manually: ").strip()
        if choice.lower() == 'new':
            TEST_BIZ = input("Business Name: ")
            TEST_PHONE = input("Phone (e.g. +407...): ")
            TEST_CODE = input("Site ID (8 chars): ")
    except EOFError:
        pass

    caller = ColdCaller()
    caller.place_call(TEST_BIZ, TEST_PHONE, TEST_CODE)

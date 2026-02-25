import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ColdCaller:
    """
    Handles automated sales calls in Romanian using Retell AI.
    Optimized for presenting a pre-built website using a short ID.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("RETELL_API_KEY")
        self.base_url = "https://api.retellai.com"
        self.agent_id = os.getenv("RETELL_AGENT_ID")
        # Base URL where users can enter their code
        self.view_url_base = os.getenv("VIEW_URL", "http://localhost:5000/view")

    def place_call(self, biz_name, phone, site_id):
        """Initiates a call to the business to present their New Website."""
        if not self.api_key or not self.agent_id:
            print(f"\n--- DRY RUN (Missing API Keys) ---")
            print(f"Calling: {biz_name} at {phone}")
            print(f"Goal: Tell them to enter code [{site_id}] on {self.view_url_base}")
            return {"status": "dry_run", "site_id": site_id}

        # Optimized payload for presenting the site
        # We tell the AI the site_id so it can tell the customer
        demo_link = f"{self.view_url_base}?id={site_id}"
        
        payload = {
            "from_number": os.getenv("RETELL_PHONE_NUMBER"),
            "to_number": phone,
            "agent_id": self.agent_id,
            "retell_llm_dynamic_variables": {
                "customer_name": biz_name,
                "site_id": site_id,
                "demo_url": demo_link,
                "view_base_url": self.view_url_base
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

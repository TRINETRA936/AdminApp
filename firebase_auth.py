import httpx
from api import apikey
FIREBASE_API_KEY = apikey

async def verify_firebase_token(id_token: str):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"idToken": id_token})
            if response.status_code == 200:
                return response.json()["users"][0]
            else:
                return None
    except:
        return None

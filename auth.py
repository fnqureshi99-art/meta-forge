import requests

def verify_license_key(product_permalink, license_key):
    # Dev Bypass
    if license_key == "METAFORGE-DEV-KEY":
        return True, "Developer Access Granted."

    url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_permalink": product_permalink,
        "license_key": license_key
    }
    
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        if data.get("success"):
            return True, "Access Granted."
        else:
            return False, "Invalid License Key."
    except:
        return False, "Connection Error."

import requests

def get_ip_config() -> str:
    
    try:
        response = requests.get("https://4.ifconfig.me/ip")
        response.raise_for_status()
        ip_v4 = response.text.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    return ip_v4
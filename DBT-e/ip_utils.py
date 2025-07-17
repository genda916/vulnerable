import requests

def get_ip_info(ip):
    try:
        res = requests.get(f'https://ipapi.co/{ip}/json', timeout=5).json()
        return {
            'city': res.get('city'),
            'region': res.get('region'),
            'country': res.get('country_name'),
            'org': res.get('org')
        }
    except Exception: # Broad exception for this unprotected example
        return {}

def get_device_info(req):
    return {
        'user_agent': req.headers.get('User-Agent', 'Unknown'),
        'lang': req.headers.get('Accept-Language', 'Unknown'),
    }

import requests

def get_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        if data['status'] == 'success':
            latitude = data['lat']
            longitude = data['lon']
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        
        return None, None


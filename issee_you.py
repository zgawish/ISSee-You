from math import cos, asin, sqrt, pi
import requests
"""
Outline
-------
1) get user location from inout using gmap_api
2) get location of iss using iss_api
3) calc distance between user and iss
4) add distance to database
5) get location of iss on Earth
6) graph previous distances over time

Things we need in database:
- distance table
- distance between user and iss column
- datetime column
"""

def get_ISS_json():
    iss_url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(iss_url)
    data = response.json()
    print(data)
    return data

def foo():
    pass

def extract_ISS_datapoints(json_response):
    json_data = get_ISS_json()
    print(json_data)
    counter = 0
    for key, value in json_data.items():
        print(key)
        print(value)
        counter += 1
        if counter == 2:
            break
    

# example url for gmap
# api_key = {}
# gmap_url = https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=YOUR_API_KEY
# gmap reference: https://developers.google.com/maps/documentation/places/web-service/search


# Formula to calculate distance between to Lat & Lon Points
#def distance_btw(lat1, lat2, lon1, lon2):
#    R = 6373 # Radius of the earth
#    
#    d_lon = lon2 - lon1
#    d_lat = lat2 - lat1
#    
#    a = sin(d_lat / 2) ** 2 + cos(lat1)* cos(lat2) * sin(dlon / 2) ** 2
#    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#    distance = R * c
#    return distance

if __name__ == "__main__":
    data = get_ISS_json()
    extract_ISS_datapoints(data)
    
    

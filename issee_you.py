from math import cos, asin, sqrt, pi, sin, atan2
import requests
import datetime
import time
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import keyboard
import plotly.graph_objects as go
"""
Outline
-------
1) get user location from inout using gmap_api 
2) get location of iss using iss_api 
3) calc distance between user and iss 
4) add distance to database*
5) get location of iss on Earth 
6) graph previous distances over time*
7) make interactive?

Things we need in database:
- distance table
- distance between user and iss column
- datetime column
"""
USER_LOC = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={zip_code}&inputtype=textquery&fields=formatted_address,name,geometry&key={API_KEY}'
ISS_LOC = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={location}&key={API_KEY}' #ex: 40.714224,-73.961452
API_KEY = 'AIzaSyAER1V2Xb7ldCTDB5jdIo0x1H0VkDZMjuw'

engine = create_engine('mysql://root:codio@localhost/issee_you')


def add_to_table(data):
    # - time - lat - lng - distance from user
    dataf = pd.DataFrame(data, index=[0])
    dataf.to_sql('iss_data', con=engine, if_exists='append', index=False)


def clear_table():
    with engine.connect() as connect:
        connect.execute("DELETE FROM iss_data")


def keyboard_listener():
    while True:
        if keyboard.is_pressed('a'):
            print("Hello world")
            break
        else:
            print("Bollo Morld")
            break


def get_ISS_json():
    iss_url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(iss_url)
    data = response.json()
    try:
        if data['message'] == 'success':
            return data
        return {}
    except Exceptions:
        print("Error with api")
        return {}


def extract_ISS_datapoints(json_response):
    print(json_response)
    latitude = json_response['iss_position'].get('latitude')
    longitude = json_response['iss_position'].get('longitude')
    time_stamp = json_response['timestamp']


def convert_timestamp(unix_time):
    time = datetime.datetime.fromtimestamp(int(str(unix_time))).strftime('%H:%M:%S')
#     print(time)
#     print(type(time))
    return str(time)


#Formula to calculate distance between to Lat & Lon Points
def distance_btw(lat1, lat2, lon1, lon2):
    R = 6373 # Radius of the earth
    
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    
    a = sin(d_lat / 2) ** 2 + cos(lat1)* cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def get_user_loc():
    zip_code = input("Please enter your zip code: ")
    request = USER_LOC.format(zip_code=zip_code, API_KEY=API_KEY)
    response = requests.get(request)
    user_loc = response.json()
    if user_loc['status'] == 'OK':
        return user_loc['candidates'][0]
    else:
        return {}

    
# gets iss location on Earth
def get_iss_earth(iss_lat, iss_lng):
    location = "{lat},{lng}".format(lat=iss_lat, lng=iss_lng)
    request = ISS_LOC.format(location=location, API_KEY=API_KEY)
    response = requests.get(request)
    iss_earth = response.json()
    if iss_earth['status'] == 'OK':
        return iss_earth['results'][0]
    else:
        return {}


def get_updates(user_lat, user_lng):
    iss_loc = get_ISS_json()
    if len(iss_loc) == 0:
        print('error')
        return

    iss_lat = iss_loc['iss_position']['latitude']
    iss_lng = iss_loc['iss_position']['longitude']
    
    iss_earth = get_iss_earth(iss_lat, iss_lng)
    if len(iss_earth) != 0:
        loc_on_earth = iss_earth['formatted_address']
        print('ISS is currently over: ' + loc_on_earth)
    else:
        print('ISS is currently over: ' + "lat: " + str(iss_lat) + ", long: " + str(iss_lng))


    distance = distance_btw(float(user_lat), float(iss_lat), float(user_lng), float(iss_lng))
    time_stamp = convert_timestamp(iss_loc['timestamp'])
    data = {'time': time_stamp,'latitude': iss_lat, 'longitude': iss_lng, 'distance': distance}
    add_to_table(data)
    graph_data()
    print('Distance between ISS and you is ' + str(distance) + ' kilometers')
    print('To exit, press CRTL + C')
    print('---------------')


def graph_data():
    data = pd.read_sql_query("SELECT * FROM iss_data ORDER BY time DESC LIMIT 10", con=engine)
    time = [str(data['time'][i]) for i in range(len(data['time']) - 1, -1, -1)]
    distance = [data['distance'][i] for i in range(len(data['distance']) - 1, -1, -1)]

    fig = go.Figure(data=go.Scatter(x=time,
                                y=distance,
                                mode='lines+markers',
                                marker_color='red',
                                text=("latitude: " + data['latitude'][::-1] + ", longitude: " + data['longitude'][::-1]))) # hover text goes here

    fig.update_layout(title='Distance from ISS')
    fig.write_html('distance.html')
    fig.show()
    

def welcome():
    print("Welcome to ISSee You")
    print("--------------------")
    print("Using the Google Places and Reverse Geocoding APIs,")
    print("along with a live ISS API, this program displays")
    print("live ISS location related to your position on Earth! \n")
    if input("Press Enter to continue or any key followed by enter to cancel: ") == '':
        return True
    else:
        return False

    
    
def main():
    if welcome() is False:
        return
    clear_table()
    user_loc = get_user_loc()
    print(user_loc['formatted_address'])
    if len(user_loc) == 0:
        print('error')
        return
    user_lat = user_loc['geometry']['location']['lat']
    user_lng = user_loc['geometry']['location']['lng']

    while True:
        get_updates(user_lat, user_lng)
        time.sleep(5)


if __name__ == "__main__":
    main()

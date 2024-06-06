#https://project-osrm.org/docs/v5.22.0/api/#requests
import requests
def distance_duration_calculation(startcoords,endcoords):  #(lng,lat),(lng,lat)
    response=requests.get(f"https://router.project-osrm.org/route/v1/driving/{startcoords};{endcoords}?alternatives=false&steps=false&overview=false&generate_hints=false").json()

    # in second and meter
    return response['routes'][0]['duration'] , response['routes'][0]['distance']







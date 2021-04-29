from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .models import Locations
from .forms import LocationsModelForm
from geopy.geocoders import Photon
# from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address, popup_box
import folium
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api
import json
from profiles.models import Profile


def calculate_distance_view(request):
    # initial values
    nominatim = Nominatim()

    global castle_ide
    #areaId = nominatim.query('poland').areaId()

    overpass = Overpass()
    api = Api()
    name = None
    review = None
    state = None

    country = nominatim.query('germany')

    locator = Photon()  # (user_agent='martin_jr8')
    areaId = country.areaId()
    names_query = country.toJSON()
    country_details = names_query[0]
    country_coor_lat = country_details["lat"]
    country_coor_lon = country_details["lon"]

    # castles location query
    castle_query = overpassQueryBuilder(area=areaId, elementType='node', selector='castle_type', out='body')
    castle_objects = overpass.query(castle_query)
    castle_list = castle_objects.elements()

    # castle_infos = []
    # for castle in castle_list:
    #     castle_infos.append(castle.tags())

    # initail folium map
    m = folium.Map(location=[country_coor_lat, country_coor_lon], zoom_start=6)

    for castle_loc in castle_list:
        info_dict = castle_loc.tags()
        castle_id = castle_loc.id()
        castle_name = info_dict.get('name')
        if castle_name == None:
            continue
        else:
            folium.Marker([castle_loc.lat(), castle_loc.lon()], tooltip=castle_name,
                          popup=folium.Popup(popup_box(info_dict.get('name'), castle_id), max_width=500),
                          icon=folium.Icon(color='purple', icon='fort-awesome', prefix='fa')).add_to(m)

    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        loc = user.location
        location = locator.geocode(loc)
        l_lat = location.latitude
        l_lon = location.longitude
        loc_point = (l_lat, l_lon)

        folium.Marker([l_lat, l_lon], tooltip='Your Location', popup=location,
                      icon=folium.Icon(color='blue', icon='home', prefix='fa')).add_to(m)

    if request.method == 'GET' and request.is_ajax():
        castle_ide = request.GET.get('castle_id')
        castle_data = api.query(f'node/{castle_ide}')
        castle_details = castle_data.tags()

        # if request.user.is_authenticated and user.location != None:
        #     castle_lat = castle_data.lat()
        #     castle_lon = castle_data.lon()
        #     castle_point = (castle_lat, castle_lon)
        #     distance = round(geodesic(loc_point, castle_point).km, 2)
        #     castle_details["distance"] = distance

        # line = folium.PolyLine(locations=[loc_point, castle_point], weight=2, color='blue')
        # m.add_child(line)
        # m = m._repr_html_()

        return HttpResponse(json.dumps(castle_details), content_type="application/json")

    if request.user.is_authenticated and request.method == 'POST' and request.is_ajax():
        castleName = request.POST.get('castleName')
        review = request.POST.get('review')
        state = request.POST.get('state')
        user = request.user
        ide = castle_ide
        form = LocationsModelForm()
        form.save(user, castleName, review, state, ide)

        folium.Marker([52.352, 6.22], tooltip='Your Location', popup=location,
                      icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(m)
        messages.info(request, 'success. Review saved')

        # m = m._repr_html_()  

        # return redirect('/')

        # return HttpResponseRedirect('measurements/main.html')     

        # return render(request, 'measurements/main.html', {'map': m})

        # return render(request, 'measurements/main.html')  

        # return HttpResponse(request) 

    m = m._repr_html_()

    context = {
        # 'name': name,
        # 'review': review,
        # 'state': state,
        # 'map': m,
        # 'castles': country_coor_lat,
        # 'ops' : border_objects
        # 'name': requested_id
    }

    return render(request, 'measurements/main.html', {'map': m})

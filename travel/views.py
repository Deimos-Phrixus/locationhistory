from django.shortcuts import render
from .models import *
import datetime 
from django.core.files.storage import FileSystemStorage
import zipfile
from django.conf import settings
import os
import json
import pytz
# Create your views here.

def format_latlng(latlng):
    f = latlng/1e7
    # print(f)
    return f

def get_first_travel(request):
    rest_points = []
    utc=pytz.UTC
    travel = Travel.objects.filter(start_time__gte=(datetime.date.today() + datetime.timedelta(-41)))
    print(Travel.objects.all().count())
    print(travel.count())
    waypoints = TravelWayPoints.objects.filter(travel=travel)
    transits = TravelTransit.objects.filter(travel=travel)
    travels = []
    for each in Travel.objects.filter(start_time__gte=(datetime.date.today() + datetime.timedelta(-41))):
        j = {}
        j['travel'] = each
        j['waypoints'] = TravelWayPoints.objects.filter(travel=each)
        j['transits'] = TravelTransit.objects.filter(travel=each)
        travels.append(j)
    if (request.method=="POST"):
        l = request.FILES["travelzip"]
        fs = FileSystemStorage(location="travel_zip")
        fs_url = fs.url(fs.save(l.name, l))
        with zipfile.ZipFile(os.path.join(settings.BASE_DIR, "travel_zip", fs_url), "r") as zip_file:
            zip_file.extractall("travel_zip")
        final_files = os.listdir(os.path.join(settings.BASE_DIR, "travel_zip", "Takeout/Location History/Semantic Location History/2020"))
        for each in final_files:
            travel_data = json.load(open(os.path.join(settings.BASE_DIR, "travel_zip", "Takeout/Location History/Semantic Location History/2020", each)))['timelineObjects']
            for td in travel_data:
                if ('activitySegment' in td.keys()):
                    start_time = datetime.datetime.utcfromtimestamp(int(td['activitySegment']['duration']['startTimestampMs'])/1000.0)
                    end_time = datetime.datetime.utcfromtimestamp(int(td['activitySegment']['duration']['endTimestampMs'])/1000.0)
                    
                    start_location = td['activitySegment']['startLocation']
                    start_lat = format_latlng(start_location['latitudeE7'])
                    start_lng = format_latlng(start_location['longitudeE7'])
                    end_location = td['activitySegment']['endLocation']
                    end_lat = format_latlng(end_location['latitudeE7'])
                    end_lng = format_latlng(end_location['longitudeE7'])
                    
                    activity_type_1 = td['activitySegment']['activities'][0]['activityType']
                    activity_type_2 = td['activitySegment']['activities'][1]['activityType']
                    try:
                        waypoints = []
                        wps = td['activitySegment']['waypointPath']['waypoints']
                        for www in wps:
                            j = {'latE7': format_latlng(www['latE7']), 'lngE7': format_latlng(www['lngE7'])}
                            waypoints.append(j)
                        try:
                            transits = td['activitySegment']['transitPath']['transitStops']
                            for tw in transits:
                                j = {'latE7': format_latlng(www['latitudeE7']), 'lngE7': format_latlng(www['longitudeE7'])}
                                waypoints.append(j)
                        except:
                            pass
                    except:
                        waypoints = []
                    if (start_time > (datetime.datetime.now() + datetime.timedelta(-41))):
                        travel_check = []
                        for each in travel:
                            if ((start_time.replace(tzinfo=utc) > each.start_time.replace(tzinfo=utc) and start_time.replace(tzinfo=utc) < each.end_time.replace(tzinfo=utc)) or (end_time.replace(tzinfo=utc) > each.start_time.replace(tzinfo=utc) and end_time.replace(tzinfo=utc) < each.end_time.replace(tzinfo=utc))):
                                if (activity_type_1 == each.travel_type_1):
                                    travel_check.append(each)
                                    
                        rest_points.append({'start': {'lat': start_lat, 'lng': start_lng, 'time': start_time}, 'end': {'lat': end_lat, 'lng': end_lng, 'time': end_time}, 'waypoints': waypoints,
                        'travel_type':{'type1': activity_type_1, 'type2': activity_type_2}, 'travel_check': travel_check})
        print(fs_url)
    # print(len(rest_points))
    return render(request, "index.html", {"travels": travels, "rest_points": rest_points})
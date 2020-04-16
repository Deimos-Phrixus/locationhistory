from django.core.management.base import BaseCommand, CommandError
from travel.models import *
from django.conf import settings
import os
import json
from datetime import datetime
import warnings
warnings.simplefilter("ignore")

def format_latlng(latlng):
    f = latlng/1e7
    # print(f)
    return f

class Command(BaseCommand):
    help = "Load data from json into sqlite3. WARNING: will create duplicates if db already exists"
    
    th_folder =  "Timeline History"
    th_candidates = ["Ninad"]


    def handle(self, *args, **options):
        travels = []
        files = []
        travel_count = 0
        for each in self.th_candidates:
            files += list(map(lambda x: os.path.join(settings.BASE_DIR, self.th_folder, each, x), os.listdir(os.path.join(settings.BASE_DIR, self.th_folder, each))))
        for each in files:
            print("Loading", each)
            travel_data = json.load(open(each))['timelineObjects']
            for td in travel_data:
                if ('activitySegment' in td.keys()):
                    start_time = datetime.utcfromtimestamp(int(td['activitySegment']['duration']['startTimestampMs'])/1000.0)
                    end_time = datetime.utcfromtimestamp(int(td['activitySegment']['duration']['endTimestampMs'])/1000.0)
                    start_location = td['activitySegment']['startLocation']
                    start_lat = format_latlng(start_location['latitudeE7'])
                    start_lng = format_latlng(start_location['longitudeE7'])
                    end_location = td['activitySegment']['endLocation']
                    end_lat = format_latlng(end_location['latitudeE7'])
                    end_lng = format_latlng(end_location['longitudeE7'])

                    activity_type_1 = td['activitySegment']['activities'][0]['activityType']
                    activity_type_2 = td['activitySegment']['activities'][1]['activityType']

                    travel = Travel.objects.create(start_time=start_time, end_time=end_time, 
                                                   start_lat=start_lat, start_lng=start_lng, 
                                                   end_lat=end_lat, end_lng=end_lng,
                                                   travel_type_1=activity_type_1, travel_type_2=activity_type_2)
                    travel_count += 1
                    if ('waypointPath' in td["activitySegment"].keys()):
                        for wp in td["activitySegment"]["waypointPath"]["waypoints"]:
                            wp_lat = format_latlng(wp['latE7'])
                            wp_lng = format_latlng(wp['lngE7'])
                            TravelWayPoints.objects.create(travel=travel, lat=wp_lat, lng=wp_lng)
                    
                    if ('transitPath' in td["activitySegment"].keys()):
                        for wp in td["activitySegment"]["transitPath"]["transitStops"]:
                            wp_lat = format_latlng(wp['latitudeE7'])
                            wp_lng = format_latlng(wp['longitudeE7'])
                            TravelTransit.objects.create(travel=travel, lat=wp_lat, lng=wp_lng)
            print("Loaded", travel_count, " from", each)
            print("")


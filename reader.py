import json
from datetime import datetime

class Location():
	def __init__(self, lattitude, longitude):
		self.lattitude = lattitude
		self.longitude = longitude

class Travel():
	def __init__(self, start_location, end_location, start_time, end_time, waypoints):
		self.start_location = start_location
		self.end_location = end_location
		self.start_time = start_time
		self.end_time = end_time
		self.waypoints = waypoints


travels = []
json_file = json.loads(open("./Timeline History/Ridhwanul/2019/2019_NOVEMBER.json", "r").read().decode('utf-8'))
timeline_objects = json_file['timelineObjects']
numTravelDays = 0
days = []
typeOfobjects = {}
for each in timeline_objects:
	if ('activitySegment' in each.keys()):
		start_time = datetime.utcfromtimestamp(int(each['activitySegment']['duration']['startTimestampMs'])/1000.0)
		end_time = datetime.utcfromtimestamp(int(each['activitySegment']['duration']['endTimestampMs'])/1000.0)
		if start_time.date() not in days:
			numTravelDays += 1
			print(start_time.date())
			days.append(start_time.date())

		start_location = each['activitySegment']['startLocation']
		start_location = Location(start_location['latitudeE7'], start_location['longitudeE7'])
		end_location = each['activitySegment']['endLocation']
		end_location = Location(end_location['latitudeE7'], end_location['longitudeE7'])
		waypoints = []
		if ('waypointPath' in each["activitySegment"].keys()):
			for wp in each["activitySegment"]["waypointPath"]["waypoints"]:
				waypoints.append(Location(wp['latE7'], wp['lngE7']))
		if ('transitPath' in each["activitySegment"].keys()):
			for wp in each["activitySegment"]["transitPath"]["transitStops"]:
				waypoints.append(Location(wp['latitudeE7'], wp['longitudeE7']))
		travels.append(Travel(start_location, end_location, start_time, end_time, waypoints))
	
	for k in each.keys():
		try:
			typeOfobjects[k] += 1
		except:
			typeOfobjects[k] = 1

print(typeOfobjects)
print(timeline_objects[0]['activitySegment']['duration'].keys())
print(len(travels))
print(numTravelDays)

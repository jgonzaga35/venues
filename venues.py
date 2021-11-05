import json
import csv
import math
from sys import argv

RADIUS_OF_EARTH = 6371.0

def getClosestXvenues(latitude, longitude, limit=10):
    """
    Returns a list of categories and the venues under those 
    categories that are closest to the lat and long coordinates provided.
    """

    if limit <= 0:
        print("limit value must be greater than 0")
        return

    venues = []
    origin = latitude,longitude
    

    # Open CSV file
    with open('venues.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            target = float(row['latitude']),float(row['longitude'])
            venue = {'name': row['name'], 
                     'address': row['address'],
                     'categories': row['categories'],
                     'distance': calculateDistance(origin, target)}
            venues.append(venue)
    
    # Sort venues and pick the X closest venues
    venues.sort(key=lambda d: d['distance'], reverse=False)
    venues = venues[:limit]

    # Create a list containing all categories
    # present in the X closest venues
    total_categories = []
    for venue in venues:
        categories = venue['categories']
        categories = categories.split(",")
        for category in categories:
            total_categories.append(category) if category not in total_categories else total_categories
    
    # Assign all X closest venues to the categories
    output = assignVenuesToCategories(total_categories,venues)
    return output


def calculateDistance(origin,target):
    """
    Given the longitude and latitude of two points, return the distance between them.
    """
    lat1, long1 = origin
    lat2, long2 = target

    lat_diff = math.radians(lat2 - lat1)
    long_diff = math.radians(long2 - long1)
    a = (math.sin(lat_diff / 2) * math.sin(lat_diff / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(long_diff / 2) * math.sin(long_diff / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = RADIUS_OF_EARTH * c

    return distance

def getVenuesWithCategory(category, venues):
    """
    Return a list of all venues that contain the specified category.
    """

    total_venues = []
    for venue in venues:
        venue_categories = venue['categories'].split(",")
        if category in venue_categories:
            total_venues.append(venue)

    return total_venues

def assignVenuesToCategories(categories, venues):
    """
    Assigns each venue to each category.
    """
    
    output = []

    for category in categories:
        dct = {}
        dct['category'] = category
        dct['venues'] = getVenuesWithCategory(category, venues)
        output.append(dct)

    # Sort output by number of venues (descending), then by category (ascending)
    output.sort(key=lambda d: (-len(d['venues']), d['category'].lower()))

    # Sort venues by distance (ascending)
    for out in output:
        out.get('venues').sort(key=lambda d: d['distance'])

    # Remove unnecessary keys
    for row in output:
        for venue in row.get('venues'):
            venue.pop('categories',None)
            venue.pop('distance',None)

    # Print the output
    print(json.dumps(output,sort_keys=False,indent=4))

    return output


if __name__ == '__main__':
    if len(argv) not in [3, 4]:
        print("Usage: python3 venues.py latitude longitude [limit=10]")
    else:
        getClosestXvenues(float(argv[1]), float(argv[2]), 10 if len(argv) == 3 else int(argv[3]))

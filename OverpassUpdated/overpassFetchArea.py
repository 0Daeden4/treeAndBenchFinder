import requests
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.ops import transform
import pyproj

def fetch_osm_data(overpassQuery):
    overpassURL = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpassURL, params={'data': overpassQuery})
    response.raise_for_status()  #HTTP error
    return response.json()

def calculate_area(geometry):
    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:32633')  # Use an appropriate UTM zone for your area

    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
    projected_geometry = transform(project, geometry)
    return projected_geometry.area

def calculate_length(geometry):
    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:32633')  # Use an appropriate UTM zone for your area

    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
    projected_geometry = transform(project, geometry)
    return projected_geometry.length

#chatgpt until this point since i am lazy


def reformatCoord(input):
    lines = input.strip().split('\n')
    coords= []
    for line in lines:
        lon, lat = map(float, line.split(','))
        coords.append((lon, lat))
    reformatted_coords = " ".join(f"{lat} {lon}" for lon, lat in coords)
    #print(reformatted_coords)
    return reformatted_coords

def exportData(data):
    f = open("outputJSON.txt", "w") #txt format for better readability
    f.write(str(data))
    f.close()



def customInput(polygonCoords):
    polygonCoords = reformatCoord(polygonCoords)
    overpassQuery = f"""
    [out:json][timeout:25];
        (
            way(poly:"{polygonCoords}");
        )->.polyArea;

        (
          wr["landuse"="grass"](area.polyArea);
          wr["leisure"="garden"](area.polyArea);
          wr["natural"="wood"](area.polyArea);
          wr["natural"="grassland"](area.polyArea);
          wr["natural"="tree_row"](area.polyArea);
         );
    out geom;
    """

    osmJSONData = fetch_osm_data(overpassQuery)
    

    elements = osmJSONData['elements']
    
    ways = [el for el in elements if el['type'] == 'way']
    relations = [el for el in elements if el['type'] == 'relation']

    greeneryArea = 0

    for relation in relations:
        area = calcRelationArea(relation)
        #print(f"Relation ID: {relation['id']}, Area: {area} square meters")
        greeneryArea+=area

    for way in ways:
        coords = fetchNodesOfWay(way)
        line = LineString(coords)
        length = calculate_length(line) #assuming that the width is 1 meter wide
        #print(f"Way ID: {way['id']}, Length: {length} meters")
        greeneryArea+=length

    #print("Square Meters: %.4f m2\nSquare Kilometers: %.4f km2" %(greeneryArea , greeneryArea/1e+6))
    return "Square Meters: %.4f m2\nSquare Kilometers: %.4f km2"%(greeneryArea , greeneryArea/1e+6)

def fetchNodesOfWay(way):
    return [(singularNode['lon'], singularNode['lat']) for singularNode in way['geometry']]

def calcRelationArea(relation):
    # get coords of each node in a way inside a relation
    def getPolygonCoords( member):
        return [(singularNode['lon'], singularNode['lat']) for singularNode in member['geometry']]

    outerPolygons = []
    innerPolygons = []
    
    for member in relation['members']:
        if member['type'] == 'way':
            coords = getPolygonCoords(member)
            #print(coords)
            polygon = Polygon(coords)
            if member['role'] == 'outer':
                outerPolygons.append(polygon)
            elif member['role'] == 'inner':
                innerPolygons.append(polygon)

    #assemble multipolygon chatGPT helped here
    multipolygon = MultiPolygon(outerPolygons)
    for innerPolygon in innerPolygons:
        for i, outerPolygon in enumerate(outerPolygons):
            if outerPolygon.contains(innerPolygon):
                outerPolygons[i] = Polygon(outerPolygon.exterior.coords, [innerPolygon.exterior.coords])
                multipolygon = MultiPolygon(outerPolygons)


    area = calculate_area(multipolygon)
    return area

def main():
    customInput("")
    


if __name__ == "__main__":
    main()

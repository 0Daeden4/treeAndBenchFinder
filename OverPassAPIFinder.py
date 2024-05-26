import webbrowser
import requests
import folium

def fetch_osm_data(overpass_query):
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={'data': overpass_query})
    response.raise_for_status()  #HTTP Error exept
    return response.json()

def parse_osm_data(data):
    if data is None:
        return []

    elements = data['elements']
    nodes = [el for el in elements if el['type'] == 'node' and 'tags' in el]
    return nodes

def create_map(nodes):
    #zoom map
    avg_lat = sum([nodez['lat'] for nodez in nodes]) / len(nodes)
    avg_lon = sum([nodez['lon'] for nodez in nodes]) / len(nodes)
    map_ = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)

    #add markers
    for nodez in nodes:
        type = nodez['tags'].get('type', 'unknown type')
        lat = nodez['lat']
        lon = nodez['lon']
        folium.Marker([lat, lon], popup=type).add_to(map_)

    return map_

def reformatCoord(input):
    lines = input.strip().split('\n')
    coords= []
    for line in lines:
        lon, lat = map(float, line.split(','))
        coords.append((lon, lat))
    reformatted_coords = " ".join(f"{lat} {lon}" for lon, lat in coords)
    print(reformatted_coords)
    return reformatted_coords

def query(coords):
    overpass_query = f"""
    [out:json];
    node
      (poly:"{coords}");
    out body;
    >;
    out skel qt;
    """
    print(overpass_query)
    return overpass_query

def treeCounter(data):
    if data is None:
        return []

    elements = data['elements']
    nodes = [el for el in elements if el['type'] == 'node' 
             and 'tags' in el and 'natural' in el['tags'] and el['tags']['natural'] == 'tree']
    treeCount = len(nodes)
    return treeCount , nodes

def benchCounter(data):
    if data is None:
        return []

    elements = data['elements']
    nodes = [el for el in elements if el['type'] == 'node' 
         and 'tags' in el and 'amenity' in el['tags'] and el['tags']['amenity'] == 'bench']
    benchCount = len(nodes)
    return benchCount , nodes



def customInput( mapName , unorganizedCoords , func):
    #these are reversed because i am to lazy to fix the rest
    query_out = query(reformatCoord(unorganizedCoords))
    osm_data = fetch_osm_data(query_out)
    count, parsed_data = func(osm_data)
    if not parsed_data:
        print("No data found or an error occurred.")
        return

    
    map_ = create_map(parsed_data)
    savedMap = str(mapName) + '.html'
    map_.save(savedMap)
    webbrowser.open(savedMap)
    print("Map has been created and saved as " + savedMap + ".")
    return count




def main():
    print("Main Method")


if __name__ == "__main__":
    main()

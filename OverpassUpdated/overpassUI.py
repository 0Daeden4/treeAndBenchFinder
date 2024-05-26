import webbrowser
import tkinter as tk
from tkinter import Frame, messagebox
import overpassFetchArea #ignore error

def getArea():
    polyCoords = polyCoordsEntry.get()
    if polyCoords == "":
        areOutputString.set("Enter Valid Coordinates!")
    else:
        area = overpassFetchArea.customInput(polyCoords)
        updateOutputString = area
        areOutputString.set(updateOutputString)

def displayMap():
    polyCoords = polyCoordsEntry.get()
    if polyCoords == "":
        areOutputString.set("Enter Valid Coordinates!")
    else:
        coords = overpassFetchArea.reformatCoord(polyCoords)

        overpassQuery = f"""
        [out:json][timeout:25];
            (
                way(poly:"{coords}");
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
        webbrowser.open("https://overpass-turbo.eu/?Q="+overpassQuery)

# Create the main application window
root = tk.Tk()
root.title("Greenery Calculator")
root.config(bg="black")
webbrowser.open("https://www.keene.edu/campus/maps/tool/")

frame = Frame(root)
frame.grid(row= 3 , column = 1, padx=10, pady = 5)

areOutputString = tk.StringVar()
areOutputString.set("")

polyCoordsLabel = tk.Label(frame, text="Enter Polygon Coords")
polyCoordsLabel.grid(row=0, column = 0, padx=5, pady=10)


polyCoordsEntry = tk.Entry(frame)
polyCoordsEntry.grid(row=1, column = 0, padx=5, pady=10)


calcAreaButton = tk.Button(frame, text="Calculate Area" , command=getArea)
calcAreaButton.grid(row=2, column = 0, padx=5, pady=10)

displayQueryButton = tk.Button(frame, text="Display Map On Overpass Turbo" , command=displayMap)
displayQueryButton.grid(row=3, column = 0, padx=5, pady=10)


areaOutputLabel = tk.Label(frame, textvariable=areOutputString)
areaOutputLabel.grid(row=2, column = 1, padx=5, pady=10)


root.mainloop()


import webbrowser
import tkinter as tk
from tkinter import Frame, messagebox
import OverPassAPIFinder #ignore error

def getTreeCount():
    mapName = mapNameEntry.get()
    polyCoords = polyCoordsEntry.get()
    if polyCoords == "":
        treeCountString.set("Enter Valid Coordinates!")
    else:
        func = OverPassAPIFinder.treeCounter
        count  = OverPassAPIFinder.customInput(mapName, polyCoords, func)
        updateOutputString = "Tree Count: " + str(count)
        treeCountString.set(updateOutputString)
def getBenchCount():
    mapName = mapNameEntry.get()
    polyCoords = polyCoordsEntry.get()
    if polyCoords == "":
        benchCountString.set("Enter Valid Coordinates!")
    else:
        func = OverPassAPIFinder.benchCounter
        count = OverPassAPIFinder.customInput(mapName, polyCoords, func)
        updateOutputString = "Bench Count: " + str(count)
        benchCountString.set(updateOutputString)

# Create the main application window
root = tk.Tk()
root.title("Square Calculator")
root.config(bg="black")
webbrowser.open("https://www.keene.edu/campus/maps/tool/")

frame = Frame(root)
frame.grid(row= 4 , column = 1, padx=10, pady = 5)

treeCountString = tk.StringVar()
treeCountString.set("")

benchCountString = tk.StringVar()
benchCountString.set("")

mapNameLabel = tk.Label(frame, text="Enter Map Name:")
mapNameLabel.grid(row=0, column = 0, padx=10, pady=10)


polyCoordsLabel = tk.Label(frame, text="Enter Polygon Coords")
polyCoordsLabel.grid(row=0, column = 1, padx=5, pady=10)

mapNameEntry = tk.Entry(frame)
mapNameEntry.grid(row=1, column = 0, padx=5, pady=10)

polyCoordsEntry = tk.Entry(frame)
polyCoordsEntry.grid(row=1, column = 1, padx=5, pady=10)


treeCountButton = tk.Button(frame, text="Get Tree Count" , command=getTreeCount)
treeCountButton.grid(row=3, column = 0, padx=5, pady=10)

benchCountButton = tk.Button(frame, text="Get Bench Count" , command=getBenchCount)
benchCountButton.grid(row=4, column = 0, padx=5, pady=10)


treeCountLabel = tk.Label(frame, textvariable=treeCountString)
treeCountLabel.grid(row=3, column = 1, padx=5, pady=10)

benchCountLabel= tk.Label(frame, textvariable=benchCountString)
benchCountLabel.grid(row=4, column = 1, padx=5, pady=10)

root.mainloop()


import folium
import pandas as pd
import json

start_coords = (35.158533, 129.160889)
m = folium.Map(location=start_coord, zoom_start=14)
m.save("./templates/folium.html")
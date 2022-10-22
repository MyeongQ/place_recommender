from flask import Flask, render_template, jsonify, request
import folium

app = Flask(__name__)

@app.route("/")
def index():
    start_coords = (35.158533, 129.160889)
    folium_map = folium.Map(location=start_coords, zoom_start=16)
    return folium_map._repr_html_()

@app.route("/data", methods=['GET'])
def hello_request():
    data = request.args.get('data')
    return jsonify(data)

if __name__ == "__main__":
    app.run()
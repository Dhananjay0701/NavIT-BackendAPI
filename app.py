from flask import Flask, jsonify, request, render_template
import io
import base64
import numpy as np
from PIL import Image
import json

# Custom func
from routing import route as route
from routing import pathApprox as pathApprox
from Navigation import TrilaterationGeo as trilateration
from Firebase import firebase as firebase

app = Flask(__name__)
app.config["DEBUG"] = True




########################################################################################## FIREBASE

# return all map names from firebase
@app.route('/mapAll', methods=['GET'])
def mapAll():
    ans = firebase.getBuildings()
    return jsonify({'result' : ans})

# return all floor in a map from firebase
@app.route('/floorAll/<building>', methods=['GET'])
def floorAll(building):
    ans = firebase.getFloors(building)
    return jsonify({'result' : ans})

# return all rooms in a map, floor from firebase
@app.route('/roomAll/<building>/<floor>', methods=['GET'])
def roomAll(building, floor):
    roomDict = firebase.getRooms(building, floor)
    ans = list(roomDict.keys())
    return jsonify({'result' : ans})

# return x, y of map, floor, room from firebase
@app.route('/room/<building>/<floor>/<room>', methods=['GET'])
def room(building, floor, room):
    ans = firebase.getXY(building, floor, room)
    return jsonify({'result' : ans})





########################################################################################## TRILATERATION

# return trilaterated -> pixel
# params => signal[POST/JSON],  building[GET]
@app.route('/locate/<building>', methods=['POST'])
def locate(building):
    json = request.get_json()
    routerAll = firebase.getRouter(building)
    pos = firebase.getLatlong(building)

    signal = []
    routerpos = []
    for MAC in json['router'].keys():
        signal.append(json['router'][MAC])
        routerpos.append(routerAll[MAC])

    print('DEBUG', routerpos)
    ans = trilateration.main(signal, routerpos, pos)
    
    if(ans):
        return jsonify({'result' : ans})

    else:
        return 'Error!!! Contact Admin. Error Code : NO_TLAT'




########################################################################################## IMAGE

# return floor map img
# param => building Name, floor Number
@app.route('/map/<building>/<floor>', methods=['GET'])
def map(building, floor):
    if(not(building or floor)):
        data = 'Bad Request.' 
        return data, 400

    else:
        #get store from database
        # pick map from central server
        path = f'resources/maps/{building}/{floor}/map.jpg'

        # convert img to byte stream
        with Image.open(path) as map:
            data = map.copy()

        imgByteArr = io.BytesIO()
        data.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        encoded_img = base64.b64encode(imgByteArr).decode('UTF-8')

        return jsonify({'result' : encoded_img})

    return 'Error!!! Contact Admin. Error Code : NO_MAPJPG'


# return route img
@app.route('/route/<building>/<floor>', methods=['POST'])
def routeC(building, floor):
    json = request.get_json()
    origin = firebase.getXY(building, floor, json['origin'])
    destination = firebase.getXY(building, floor, json['destination'])

    print(origin)

    mapFile = f'./resources/maps/{building}/{floor}/pathonly.jpg'

    # Approx orig and dest to closest path
    origin = pathApprox.approx(mapFile, origin)
    destination = pathApprox.approx(mapFile, destination)

    # request data valdiation
    if(not(mapFile and origin and destination)):
        result = 'Bad Request.'
        return result, 400

    encoded_img = route.route(mapFile, origin, destination)

    if not(encoded_img):
        return 'Error!!! Contact Admin. Error Code : NO_PATH'
    
    return jsonify({'result' : encoded_img})

# return route img, for inverted x, y corr
@app.route('/routeRev/<building>/<floor>', methods=['POST'])
def routeRevC(building, floor):
    json = request.get_json()
    origin = firebase.getXY(building, floor, json['origin'])[::-1]
    destination = firebase.getXY(building, floor, json['destination'])[::-1]

    print(origin)

    mapFile = f'./resources/maps/{building}/{floor}/pathonly.jpg'

    # Approx orig and dest to closest path
    origin = pathApprox.approx(mapFile, origin)
    destination = pathApprox.approx(mapFile, destination)

    # request data valdiation
    if(not(mapFile and origin and destination)):
        result = 'Bad Request.'
        return result, 400

    encoded_img = route.route(mapFile, origin, destination)

    if not(encoded_img):
        return 'Error!!! Contact Admin. Error Code : NO_PATH'
    
    return jsonify({'result' : encoded_img})


########################################################################################## Docs

# return index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# return help.html
@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

########################################################################################## END

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


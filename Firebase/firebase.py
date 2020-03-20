import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Loads Credentials and Connects with Firebase Database
cred = credentials.Certificate('./Firebase/cred/firebaseCred.json')
firebase_admin.initialize_app(cred, {
    # Add firebase URL
    'databaseURL' : ''
})


 # Returns All Available Buildings
def getBuildings():
    root = db.reference('Buildings')
    result = root.get().keys()
    return list(result)

# Returns All Available Floor of building
def getFloors(building):
    root = db.reference(f'Buildings/{building}')
    result = root.get().keys()
    return list(result)

# Returns All Available room of building, floor
def getRooms(building, floor):
    root = db.reference(f'Buildings/{building}/{floor}')
    result = root.get()
    
    roomKeys = list(result.keys())
    roomNames = []
    for key in roomKeys:
        roomNames.append(result[key]['name'])
        
    return dict(zip(roomNames, roomKeys))

# Returns XYpx of building, floor, room
def getXY(building, floor, room):
    roomDict = getRooms(building, floor)
    roomID = roomDict[room]
    
    root = db.reference(f'Buildings/{building}/{floor}/{roomID}')
    result = root.get()
    
    return (result['pixelx'], result['pixely'])

# Return Router Database
def getRouter(building):
    root = db.reference(f'router/{building}')
    result = root.get()
    
    return result

# Return LatLong of building
def getLatlong(building):
    root = db.reference(f'Buildings/{building}/latlong')
    result = root.get()
    
    return result

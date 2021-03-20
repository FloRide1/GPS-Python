
def convert_frame_to_KML(frame):
    try:
        typeOfFrame = frame['type']
        if (typeOfFrame == "GGA"):
            return convert_GGA_to_KML(frame)
        else:
            print("[ERROR] This frame format isn't handle: " + typeOfFrame)
            return -2
    except:
        print("[ERROR] An error occured during conversion in KML format")
        return -1



def convert_GGA_to_KML(gga_frame):
    try:
        if (gga_frame['type'] == "GGA"):

            longitude_GGA = str(gga_frame['longitude'])
            latitude_GGA  = str(gga_frame['latitude'])

            longitude = int(longitude_GGA[0:2]) + float(longitude_GGA[2:]) / 60 
            latitude  = int(latitude_GGA[0:2])  + float(latitude_GGA[2:])  / 60 

            kml_frame = {
                'longitude' : longitude,
                'latitude'  : latitude,
                'altitude'  : gga_frame['altitude']
            }
            return kml_frame

        else:
            print("[ERROR] This is not an GGA frame")
            return -1
    except:
        print("[ERROR] The conversion betweem this GGA frame and KML is Impossible")
        return -1

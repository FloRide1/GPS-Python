
def convert_frame_to_KML(frame):
    try:
        typeOfFrame = frame['type']
        if (typeOfFrame == "GGA"):
            if frame['quality'] != 0:
                return convert_GGA_to_KML(frame)
            else:
                return -2
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

            coeff_latitude = (-1,1) [gga_frame['north_south'] == "N"]
            coeff_longitude = (-1,1) [gga_frame['est_west']    == "E"]

            longitude_split = longitude_GGA.split(".")
            latitude_split  = latitude_GGA.split(".")

            longitude_degree = int(longitude_split[0][:-2])
            latitude_degree = int(latitude_split[0][:-2])

            longitude_minute = float(longitude_split[0][-2:] + "." + longitude_split[1])
            latitude_minute = float(latitude_split[0][-2:] + "." + latitude_split[1])

            longitude = (longitude_degree + longitude_minute / 60) * coeff_longitude
            latitude  = (latitude_degree + latitude_minute  / 60) * coeff_latitude

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

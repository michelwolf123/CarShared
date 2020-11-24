import glob
import sys
import os

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
    print("try worked")
except IndexError:
    print("Error occurd while importing")
    pass
print(sys.version_info.major)
print(sys.version_info.minor)
print(os.name)

import carla
print(dir(carla))
'''
#read the OSM(OpenStreetMap) Data
f = open("C:/Users/Michel/Carla/map.osm", 'r')
osm_data = f.read()
f.close()

#Define the conversion settings, in this case default
settings = carla.Osm2OdrSettings()
xodr_data = carla.Osm2Odr.convert(osm_data, settings)

#save file
f = open("C:/Users/Michel/Carla", 'w')
f.write(xodr_data)
f.close()
'''


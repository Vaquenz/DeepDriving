# Example scenario for usage with example.py (run this first)
from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy import setup_logging

import time
import sys
import fileinput

setup_logging()

bng = BeamNGpy('localhost', 64256)

scenario = Scenario('smallgrid', 'small_test')

vehicle = Vehicle('egovehicle', model='etk800', licence='313')

scenario.add_vehicle(vehicle, pos=(-1.5,-1,0), rot=(0,0,0))

nodes = [
	(0,0,0,6),
    (0,-20,0,6),
	(0,-100,0,6),
    (-25,-200,0,6),
    (25,-300,0,6)
]

road = Road(material='a_asphalt_01_a', rid='main_road', looped=False, texture_length=10)
road.nodes.extend(nodes)
scenario.add_road(road)

scenario.make(bng)

for i, line in enumerate(fileinput.input(scenario.get_prefab_path(), inplace=1)):
	sys.stdout.write(line.replace('overObjects = "0";', 'overObjects = "1";'))

bng.open()
bng.load_scenario(scenario)
bng.start_scenario()
bng.set_deterministic()
bng.pause()
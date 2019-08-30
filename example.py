# Example application of DDController.py
import numpy
import cv2
import math

from beamngpy import BeamNGpy, Scenario, Vehicle, setup_logging
from beamngpy.sensors import Camera, GForces, Electrics, Damage

from DDController import Controller

# The Image needs to be preprocessed
def preprocess(img, brightness):

    pil_image = img.convert('RGB')
    open_cv_image = numpy.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    hsv = cv2.cvtColor(cv2.resize(open_cv_image, (280, 210)), cv2.COLOR_BGR2HSV)
    hsv[..., 2] = hsv[..., 2] * brightness
    preprocessed = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return preprocessed

brightness = 0.4
vehicle = Vehicle('egovehicle')
# Settings for the camera - should not be changed
resolution = (280, 210)
pos = (-0.5, 1.8, 0.6)
direction = (0,1,0)
fov = 50
# Simulation settings
MAX_FPS = 60
SIMULATION_STEP = 1

# Create controller and set desired max speed (>25 not recommended)
MAX_SPEED = 25
controller = Controller(MAX_SPEED)
setup_logging()

front_camera = Camera(pos, direction, fov, resolution, near_far=(0.5,300), colour=True, depth=True, annotation=True)
electrics = Electrics()
vehicle.attach_sensor('front_cam', front_camera)
vehicle.attach_sensor('electrics', electrics)
beamng = BeamNGpy('localhost', 64256)
bng = beamng.open(launch=False)
bng.set_deterministic()
bng.set_steps_per_second(MAX_FPS)
bng.connect_vehicle(vehicle)
bng.pause()

while True:
    bng.step(SIMULATION_STEP)
    sensors = bng.poll_sensors(vehicle)
    speed = math.sqrt(vehicle.state['vel'][0] * vehicle.state['vel'][0] + vehicle.state['vel'][1] * vehicle.state['vel'][1])
    # Retrieve image and preprocess it
    imageData = preprocess(sensors['front_cam']['colour'], brightness)
    
    # Retrieve controls based on camera-image
    controls = controller.getControl(imageData, speed)
    
    # Apply controls
    vehicle.control(throttle=controls.throttle, steering=controls.steering)
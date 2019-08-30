import deep_driving.model as model
import deep_learning as dl
import dd
import misc
import math
import numpy

class CInferenceSettings(misc.settings.CSettings):
  _Dict = {
  'Data': {
    'ImageWidth': 280,
    'ImageHeight': 210
  },
  'Inference': {
    'CheckpointPath':   'trained',
    'Epoch': None,
  },
  'PreProcessing':
  {
    'MeanFile': 'image-mean.tfrecord'
  },
  }

class Controls:
    steering = 0.0
    throttle = 0.0
  
class Controller:

    _Model = None
    _Inference = None
    _Indicators = None
    _MaxSpeed = None
    
    def __init__(self, MaxSpeed):
    
        SettingFile = "inference.cfg"
        self._MaxSpeed = MaxSpeed

        Settings = CInferenceSettings(SettingFile)
        self._Model = dl.CModel(model.CAlexNet)
        self._Inference = self._Model.createInference(model.CInference, model.CInferenceReader, Settings)
        self._Inference.restore()

        self._Indicators = dd.Indicators_t()
    
    def getControl(self, Image, Speed):
        # Infer the angle of the car to the road 
        self._Indicators = self._Inference.run([Image])
        
        steering = self._Indicators.Angle
        sign = numpy.sign(steering)
        # Invert the given angle and use square root in order to modulate
        # steering angle according to extremeness of the angle to road
        steering = math.sqrt(abs(steering)) * sign * -1
        
        # Basic speed limiter
        throttle = 0.1
        if Speed * 3.6 > self._MaxSpeed:
            throttle = 0.0
        
        controls = Controls()
        controls.steering = steering
        controls.throttle = throttle
        
        return controls
        
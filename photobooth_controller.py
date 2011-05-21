import photo_session
import photo_taker
import photo_printer
import logging

class PhotoboothController:

    def __init__(self, configuration, printer_manager, camera_manager):
        self.logger = logging.getLogger('photobooth.controller')
            
        self._apply_configuration(configuration)
        self.printerManager = printer_manager
        self.cameraManager = camera_manager
        self.photoPrinter = photo_printer.PhotoPrinter(self.printerManager, self._printer_name)
        self.photoTaker = photo_taker.PhotoTaker(self.cameraManager)

    def _apply_configuration(self,configuration):
        def check_for_parameter(param):
            if not param in configuration:
                raise exception('required configuration paramater (%s) not found' % param)
            value = configuration[param]
            self.logger.debug('configuration: %s=%s' % (param, str(value)))
            return value
            
        self._session_root_path = check_for_parameter('output-directory')
        self._number_of_photos = check_for_parameter('number-of-photos')
        self._time_delay = check_for_parameter('time-delay')
        self._printer_name = check_for_parameter('printer')

    def setViewFinder(self,viewFinder):
        self.cameraManager.setViewFinder(viewFinder)

    def isCameraEnabled(self):
        return self.cameraManager.isCameraEnabled()

    def enableCamera(self):
        self.cameraManager.enableCamera()

    def disableCamera(self):
        self.cameraManager.disableCamera()

    def takePictures(self,event_callback = lambda e : None ):
        self.logger.debug('creating session')
        session = photo_session.PhotoSession(self._session_root_path, self._number_of_photos)
        self.logger.info('Taking pictures for %s' % session)        
        self.photoTaker.takePictures(self._time_delay, session, event_callback)
        self.logger.info('Printing pictures')        
        self.photoPrinter.printSession(session,event_callback)

    

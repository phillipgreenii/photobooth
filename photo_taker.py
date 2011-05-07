import math
import time
import logging

class PhotoTaker:
    def __init__(self,camera,session,numberOfPictures, finished_callback=lambda : None):
        self.logger = logging.getLogger('photo.taker')
        self.camera = camera
        self.session = session
        self.numberOfPictures = numberOfPictures
        self.counter = 0
        self.started = False
        self.done = False
        self.finished_callback = finished_callback

    def start(self):
        if self.started:
            raise exception('already started')
        self.started = True
        self.logger.debug('starting to take pictures')
        self.camera.connect("image-done",self._handlePicture)
        self._takeNextPicture()

    def _takeNextPicture(self):
        self.logger.info('taking picture: %02d' % self.counter)
        self.counter += 1
        picture_filename = '%012d' % math.floor(time.time()) + ".jpg"
        self.camera.set_property("filename", picture_filename)
        self.camera.emit("capture-start")
        

    def _handlePicture(self, c, filename):
        self.logger.debug('handling picture: %s' % filename)
        self.session.addPhoto(filename)
        if self.counter < self.numberOfPictures-1:
            self.logger.debug('delay before next picture')
            time.sleep(2) #TODO don't hardcode delay
            self._takeNextPicture()
        else:
            self.logger.debug('finished taking pictures')
            self.done = True
            self.finished_callback()

    def isDone(self):
        return self.done

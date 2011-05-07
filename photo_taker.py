import math
import time
import logging

class PhotoTaker:
    def __init__(self,camera,session,numberOfPictures, event_callback=lambda e : None):
        self.logger = logging.getLogger('photo.taker')
        self.camera = camera
        self.session = session
        self.numberOfPictures = numberOfPictures
        self.counter = 0
        self.started = False
        self.done = False
        self.event_callback = event_callback
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(repr(self))

    def start(self):
        if self.started:
            raise exception('already started')
        self.started = True
        self.logger.debug('starting to take pictures')
        self.camera.connect("image-done",self._handlePicture)
        self.event_callback({'type':'START'})
        self._takeNextPicture()

    def _takeNextPicture(self):
        self.logger.info('taking picture: %02d' % self.counter)
        self.counter += 1
        picture_filename = '%012d' % math.floor(time.time()) + ".jpg"
        self.camera.set_property("filename", picture_filename)
        self.event_callback({'type':'TAKE_PICTURE', 'current_picture':self.counter, 'total_pictures':self.numberOfPictures})
        self.camera.emit("capture-start")
        

    def _handlePicture(self, c, filename):
        self.logger.debug('handling picture: %s' % filename)
        self.session.addPhoto(filename)
        self.event_callback({'type':'TOOK_PICTURE', 'current_picture':self.counter, 'total_pictures':self.numberOfPictures})

        if self.counter < self.numberOfPictures:
            self.logger.debug('delay before next picture')
            time.sleep(2) #TODO don't hardcode delay
            self._takeNextPicture()
        else:
            self.logger.debug('finished taking pictures')
            self.done = True
            self.event_callback({'type':'DONE'})

    def isDone(self):
        return self.done

    def __repr__(self):
        return "%s(camera=%s,session=%s,numberOfPictures=%d,counter=%d,started=%s,done=%s,event_callback=%s)" % \
               (self.__class__,self.camera, self.session, self.numberOfPictures, self.counter, self.started, self.done, self.event_callback)

    def __str__(self):
        return "%s(%d/%d of %s)" % (self.__class__,self.counter, self.numberOfPictures, self.session)

import math
import time
import logging

class PhotoTaker:
    def __init__(self,camera, session, delayBetweenPhotos,  event_callback=lambda e : None):
        self.logger = logging.getLogger('photo.taker')
        self.camera = camera
        self.delay_between_photos = delayBetweenPhotos
        self.session = session
        self.event_callback = event_callback
        self.started = False
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(repr(self))

    def start(self):
        if self.started:
            raise exception('already started!')
        self.started = True
        numberOfPictures = self.session.total_photos_to_take()
                
        self.logger.debug('starting to take pictures')
        self.event_callback({'type':'START'})
        self.handler_id = self.camera.connect("image-done",self._handlePicture)
        try:
            for i in range(numberOfPictures): 
                self._delayForNextPicture(self.delay_between_photos)
                self._takeNextPicture(i,numberOfPictures)
            self.event_callback({'type':'DONE'})
        except:
            #TODO log error
            self.event_callback({'type':'ERROR'})
            self._cleanup()
            raise
            
    def _delayForNextPicture(self, seconds):
        self.logger.debug('delay before next picture')
        for timeLeft in xrange(seconds,0,-1): 
            self.event_callback({'type':'COUNT_DOWN_UPDATE', 'time_until_picture': timeLeft})
            time.sleep(1) 
        self.event_callback({'type':'COUNT_DOWN_UPDATE', 'time_until_picture': 0})

    def _takeNextPicture(self, counter, numberOfPictures):
        self.logger.info('taking picture: %02d' % counter)        
        picture_filename = '%012d' % math.floor(time.time()) + ".jpg"
        self.camera.set_property("filename", picture_filename)
        self.event_callback({'type':'TAKE_PICTURE', 'current_picture':counter, 'total_pictures':numberOfPictures})
        self.camera.set_property('block-after-capture', True)
        self.camera.emit("capture-start")
        self.logger.debug('pausing')
        time.sleep(1)
        self.camera.set_property('block-after-capture', False)

    def _handlePicture(self,c,filename):
        self.logger.debug('handling picture: %s' % filename)
        self.session.addPhoto(filename)
        if self.session.is_complete():
            self._cleanup()


    def _cleanup(self):
        self.logger.debug('cleaning up (%s)' % str(self.handler_id))
        if self.handler_id is not None:
            self.camera.disconnect(self.handler_id)

    def __repr__(self):
        return "%s(camera=%s,event_callback=%s,delay_between_photos=%d)" % \
               (self.__class__,self.camera, self.event_callback, self.delay_between_photos)

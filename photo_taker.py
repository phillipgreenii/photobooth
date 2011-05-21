import math
import time
import logging

class PhotoTaker:
    def __init__(self,camera):
        self.logger = logging.getLogger('photo.taker')
        self.camera = camera
        self.started = False

    def takePictures(self, delay_between_photos, session, event_callback=lambda e : None):
        if self.started:
            raise exception('already started!')
        self.started = True
        numberOfPictures = session.total_photos_to_take()

        def delayForNextPicture(seconds):
            self.logger.debug('delay before next picture')
            for timeLeft in xrange(seconds,0,-1): 
                event_callback({'type':'COUNT_DOWN_UPDATE', 'time_until_picture': timeLeft})
                time.sleep(1) 
            event_callback({'type':'COUNT_DOWN_UPDATE', 'time_until_picture': 0})

        def takeNextPicture(counter):
            self.logger.info('taking picture: %02d' % counter)        
            picture_filename = '%012d' % math.floor(time.time()) + ".jpg"
            self.camera.set_property("filename", picture_filename)
            event_callback({'type':'TAKE_PICTURE', 'current_picture':counter, 'total_pictures':numberOfPictures})
            self.camera.set_property('block-after-capture', True)
            self.camera.emit("capture-start")
            self.logger.debug('pausing')
            time.sleep(1)
            self.camera.set_property('block-after-capture', False)

        def handlePicture(c,filename):
                self.logger.debug('handling picture: %s' % filename)
                session.addPhoto(filename)
                if session.is_complete():
                        self._cleanup()
                
        self.logger.debug('starting to take pictures')
        event_callback({'type':'START'})
        self.handler_id = self.camera.connect("image-done",handlePicture)
        try:
            for i in range(numberOfPictures): 
                delayForNextPicture(delay_between_photos)
                takeNextPicture(i+1)
            event_callback({'type':'DONE'})
            time.sleep(2)#FIXME there needs to be a pause so pictures aren't printed before they are finished    
        except:
            #TODO log error
            event_callback({'type':'ERROR'})
            self._cleanup()
            raise
        finally:
            self.started = False

    def _cleanup(self):
        self.logger.debug('cleaning up (%s)' % str(self.handler_id))
        if self.handler_id is not None:
            self.camera.disconnect(self.handler_id)

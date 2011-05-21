import math
import time
import logging

class PhotoTaker:
    def __init__(self,camera_manager):
        self.logger = logging.getLogger('photo.taker')
        self.camera_manager = camera_manager
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
            event_callback({'type':'TAKE_PICTURE', 'current_picture':counter, 'total_pictures':numberOfPictures})
            self.camera_manager.take_photo()

        def handlePicture(filename):
            self.logger.debug('handling picture: %s' % filename)
            session.addPhoto(filename)
            if session.is_complete():
                pass
                
        self.logger.debug('starting to take pictures')
        event_callback({'type':'START'})
        self.camera_manager.set_photo_handler(handlePicture)
        try:
            for i in range(numberOfPictures): 
                delayForNextPicture(delay_between_photos)
                takeNextPicture(i+1)
            event_callback({'type':'DONE'})
            time.sleep(2)#FIXME there needs to be a pause so pictures aren't printed before they are finished    
        except Exception as ex:
            self.logger.error(ex)
            event_callback({'type':'ERROR'})
            raise
        finally:
            self.started = False

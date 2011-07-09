import math
import time
import logging

class PhotoTaker:
    def __init__(self,camera_manager, collage_generator, printer_manager):
        self.logger = logging.getLogger('photo.taker')
        self.camera_manager = camera_manager
        self.collage_generator = collage_generator
        self.printer_manager = printer_manager
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
            session.addPhoto(self.camera_manager.take_photo())

        def printPictures():
            self.logger.info('generating collage')
            event_callback({'type':'GENERATING_COLLAGE'})
            collage = self.collage_generator.generateCollage(session)
            session.setCollage(collage)       
            event_callback({'type':'PRINTING'})
            self.printer_manager.printFile(session.get_collage())#TODO get printer from configuration
            event_callback({'type':'PRINTED'})
    
        self.logger.debug('starting to take pictures')
        event_callback({'type':'START'})
        try:
            for i in range(numberOfPictures): 
                delayForNextPicture(delay_between_photos)
                takeNextPicture(i+1)
            printPictures()
            self.started=False
            event_callback({'type':'DONE'})
        except Exception as ex:
            self.logger.error(ex)
            event_callback({'type':'ERROR'})
            self.started = False
            raise

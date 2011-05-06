import math
import time

class PhotoTaker:
    def __init__(self,camera,session,numberOfPictures, finished_callback=lambda : None):
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
        print "Taking a Picture"
        self.camera.connect("image-done",self._handlePicture)
        self._takeNextPicture()

    def _takeNextPicture(self):
        print "Taking a Picture %02d" % self.counter
        self.counter += 1
        picture_filename = '%012d' % math.floor(time.time()) + ".jpg"
        self.camera.set_property("filename", picture_filename)
        self.camera.emit("capture-start")
        

    def _handlePicture(self, c, filename):
        self.session.addPhoto(filename)
        if self.counter < self.numberOfPictures-1:
            time.sleep(2) #TODO don't hardcode delay
            self._takeNextPicture()
        else:
            self.done = True
            self.finished_callback()

    def isDone(self):
        return self.done
